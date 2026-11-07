"""Generate deterministic synthetic flow records for demos and tests."""
from __future__ import annotations
import argparse, csv, random
from pathlib import Path
FIELDS = ["duration_s", "bytes_sent", "bytes_received", "packets", "dst_port", "failed_logins", "label"]
def generate_row(rng: random.Random, anomaly: bool) -> dict[str, float | str]:
    if not anomaly:
        return {"duration_s": round(rng.uniform(0.2,12),3), "bytes_sent": rng.randint(200,8000), "bytes_received": rng.randint(300,16000), "packets": rng.randint(4,90), "dst_port": rng.choice([53,80,443,123]), "failed_logins": 0, "label": "benign"}
    kind = rng.choice(["scan", "exfiltration", "bruteforce"]); row = generate_row(rng, False); row["label"] = kind
    if kind == "scan": row.update({"duration_s":round(rng.uniform(.01,.15),3), "packets":rng.randint(250,900), "dst_port":rng.randint(1024,65535)})
    elif kind == "exfiltration": row.update({"duration_s":round(rng.uniform(100,900),3), "bytes_sent":rng.randint(2_000_000,20_000_000), "packets":rng.randint(2000,10000)})
    else: row.update({"failed_logins":rng.randint(10,80), "packets":rng.randint(100,600)})
    return row
def main() -> None:
    parser=argparse.ArgumentParser(); parser.add_argument("--output",type=Path,required=True); parser.add_argument("--rows",type=int,default=1000); parser.add_argument("--anomaly-rate",type=float,default=.08); parser.add_argument("--seed",type=int,default=42); args=parser.parse_args()
    args.output.parent.mkdir(parents=True,exist_ok=True); rng=random.Random(args.seed)
    with args.output.open("w",newline="",encoding="utf-8") as handle:
        writer=csv.DictWriter(handle,fieldnames=FIELDS); writer.writeheader()
        for _ in range(args.rows): writer.writerow(generate_row(rng,rng.random()<args.anomaly_rate))
if __name__ == "__main__": main()
