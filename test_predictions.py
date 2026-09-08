import unittest
import json
import re

class TestWosPredictions(unittest.TestCase):
    def setUp(self):
        # Load EXACT_LEVELS from exact_levels.js
        with open("exact_levels.js", "r", encoding="utf-8") as f:
            content = f.read()
            match = re.search(r"const EXACT_LEVELS = (\{.*?\});", content, re.DOTALL)
            if not match:
                self.fail("Could not find EXACT_LEVELS in exact_levels.js")
            self.exact_levels = json.loads(match.group(1))

    def test_regression_level_29_confirmed_fit(self):
        """
        Regression Test:
        Damage 846,529,318 must resolve to Level 29 at ~56.0% using the Confirmed Fit.
        This checks the integrity of the Huber regression data anchoring.
        """
        target_damage = 846529318
        expected_level = 29
        expected_pct = 0.56  # 56.0%
        
        found_lvl = None
        found_pct = None
        
        # Exact same logic used in the UI
        for lvl_str in sorted(self.exact_levels.keys(), key=int):
            lvl = int(lvl_str)
            data = self.exact_levels[lvl_str]
            start = data["start"]
            end = start + data["window"]
            
            if start <= target_damage <= end:
                found_lvl = lvl
                found_pct = (target_damage - start) / data["window"]
                break
                
        self.assertIsNotNone(found_lvl, "Damage did not fall into any known level tier.")
        self.assertEqual(found_lvl, expected_level, f"Expected Level {expected_level}, but got {found_lvl}")
        self.assertAlmostEqual(found_pct, expected_pct, places=2, msg=f"Expected {expected_pct*100}%, but got {found_pct*100:.2f}%")

if __name__ == "__main__":
    unittest.main()
