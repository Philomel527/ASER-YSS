import copy
import importlib.util
from pathlib import Path
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("resource_catalog", ROOT / "tools/query_resource_catalog.py")
catalog_tool = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(catalog_tool)


class ResourceCatalogTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.catalog = catalog_tool.load_catalog()

    def test_user_aliases_resolve_to_original_resources(self):
        cases = [("霜星", "characterTachies", "char_1505_frstar_1"),
                 ("霜星2", "characterTachies", "avg_1505_frstar_1"),
                 ("罗德岛餐厅", "backgrounds", "bg_canteen"),
                 ("温馨", "musics", "m_avg_siestacity"),
                 ("脚步", "soundEffects", "d_avg_wtchkgopenftstp"),
                 ("渐变白屏", "visualEffects", "avg_062_white_02")]
        for alias, kind, expected in cases:
            with self.subTest(alias=alias):
                matches = catalog_tool.query_resources(self.catalog, alias, kind, exact=True)
                self.assertEqual([entry["raw_name"] for entry in matches], [expected])

    def test_raw_name_and_alias_return_same_record(self):
        by_alias = catalog_tool.query_resources(self.catalog, "博士", exact=True)[0]
        by_raw = catalog_tool.query_resources(self.catalog, "avg_doc_1", exact=True)[0]
        self.assertEqual(by_alias["asset_bundle"], by_raw["asset_bundle"])
        self.assertEqual(by_alias["character_config"]["variationNames"], {"#0$1": "常规"})

    def test_conflicting_name_keeps_both_candidates(self):
        matches = catalog_tool.query_resources(self.catalog, "35_i10", "backgrounds", exact=True)
        self.assertEqual({entry["raw_name"] for entry in matches}, {"35_i10", "36_g4_redleafcliff"})
        audit = catalog_tool.audit_catalog(self.catalog)
        self.assertIn({"kind": "backgrounds", "name": "35_i10", "raw_names": ["35_i10", "36_g4_redleafcliff"]}, audit["name_collisions"])

    def test_no_unprovided_variation_names_are_invented(self):
        entry = catalog_tool.query_resources(self.catalog, "Mon3tr", "characterTachies", exact=True)[0]
        self.assertEqual(entry["raw_name"], "avg_4179_monstr_1")
        self.assertIsNone(entry["character_config"])

    def test_renamed_alias_is_reported_by_comparison(self):
        changed = copy.deepcopy(self.catalog)
        changed["aliases"]["musics"]["m_avg_normal"] = "日常新版"
        result = catalog_tool.compare_catalogs(self.catalog, changed)
        self.assertEqual(result["aliases"]["musics"]["changed"], {"m_avg_normal": {"before": "平常", "after": "日常新版"}})
        self.assertEqual(self.catalog["aliases"]["musics"]["m_avg_normal"], "平常")

    def test_stale_alias_and_config_are_detected(self):
        changed = copy.deepcopy(self.catalog)
        del changed["collections"]["characterTachies"]["avg_doc_1"]
        result = catalog_tool.audit_catalog(changed)
        self.assertIn({"kind": "characterTachies", "raw_name": "avg_doc_1", "alias": "博士"}, result["aliases_missing_from_collections"])
        self.assertIn({"kind": "characterTachies", "raw_name": "avg_doc_1"}, result["configs_missing_from_collections"])

    def test_duplicate_json_keys_are_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "officialAssets_collections.json"
            path.write_text('{"backgrounds": {}, "backgrounds": {}}', encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "键重复"):
                catalog_tool.load_catalog(directory)

    def test_no_match_is_not_guessed(self):
        self.assertEqual(catalog_tool.query_resources(self.catalog, "不存在的资源名", exact=True), [])


if __name__ == "__main__":
    unittest.main()
