import unittest
from flowguard.model import MadAnomalyDetector
ROWS=[{"duration_s":1,"bytes_sent":100,"packets":10},{"duration_s":2,"bytes_sent":110,"packets":12},{"duration_s":3,"bytes_sent":90,"packets":11}]
class DetectorTests(unittest.TestCase):
    def test_benign_like_flow_is_not_flagged(self):
        detector=MadAnomalyDetector().fit(ROWS,["duration_s","bytes_sent","packets"])
        self.assertFalse(detector.score({"duration_s":2,"bytes_sent":104,"packets":11})["anomalous"])
    def test_large_outlier_is_flagged(self):
        detector=MadAnomalyDetector().fit(ROWS,["duration_s","bytes_sent","packets"])
        result=detector.score({"duration_s":2,"bytes_sent":100000,"packets":11})
        self.assertTrue(result["anomalous"]); self.assertEqual(result["top_features"][0][0],"bytes_sent")
if __name__ == "__main__": unittest.main()
