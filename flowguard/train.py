from __future__ import annotations
import argparse, csv, json
from pathlib import Path
from .model import MadAnomalyDetector
FEATURES=["duration_s","bytes_sent","bytes_received","packets","dst_port","failed_logins"]
def load_rows(path: Path) -> list[dict[str, float | str]]:
    with path.open(newline="",encoding="utf-8") as handle: return list(csv.DictReader(handle))
def main() -> None:
    parser=argparse.ArgumentParser(); parser.add_argument("--input",type=Path,required=True); parser.add_argument("--model",type=Path,required=True); parser.add_argument("--threshold",type=float,default=4.0); args=parser.parse_args()
    benign=[row for row in load_rows(args.input) if row["label"]=="benign"]
    detector=MadAnomalyDetector(args.threshold).fit(benign,FEATURES); args.model.write_text(json.dumps(detector.to_dict(),indent=2),encoding="utf-8"); print(f"trained on {len(benign)} benign flows -> {args.model}")
if __name__ == "__main__": main()
