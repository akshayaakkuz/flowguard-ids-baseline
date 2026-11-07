from __future__ import annotations
import argparse, csv, json
from pathlib import Path
from .model import MadAnomalyDetector
def main() -> None:
    parser=argparse.ArgumentParser(); parser.add_argument("--model",type=Path,required=True); parser.add_argument("--input",type=Path,required=True); parser.add_argument("--limit",type=int,default=20); args=parser.parse_args()
    detector=MadAnomalyDetector.from_dict(json.loads(args.model.read_text(encoding="utf-8")))
    with args.input.open(newline="",encoding="utf-8") as handle:
        for index,row in enumerate(csv.DictReader(handle)):
            if index>=args.limit: break
            print(json.dumps({"row":index,"label":row["label"],**detector.score(row)}))
if __name__ == "__main__": main()
