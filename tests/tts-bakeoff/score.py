#!/usr/bin/env python3
"""Objective scores for bake-off renders: WER via faster-whisper, duration variance across -1/-2/-3 renders, timestamp sanity.
  python3 score.py out/eleven-v4 out/kokoro-af_heart …     (each dir: narration.wav + narration.json)
pip install faster-whisper jiwer"""
import sys, os, json, re, statistics
from faster_whisper import WhisperModel
import jiwer
script = re.sub(r"^#.*$", "", open(os.path.join(os.path.dirname(__file__), "script.txt")).read(), flags=re.M)
norm = lambda s: re.sub(r"[^a-z0-9 ]", "", s.lower().replace("—", " ")).split()
ref = " ".join(norm(script))
asr = WhisperModel("medium.en", device="cpu", compute_type="int8")
import glob
dirs = [d for a in sys.argv[1:] for d in (sorted(glob.glob(a)) or [a])]   # PowerShell/cmd don't expand globs
rows = []
for d in dirs:
    j = json.load(open(os.path.join(d, "narration.json")))
    segs, _ = asr.transcribe(os.path.join(d, "narration.wav"))
    hyp = " ".join(norm(" ".join(s.text for s in segs)))
    wer = jiwer.wer(ref, hyp)
    ws = j.get("words") or []
    mono = all(ws[i]["s"] <= ws[i + 1]["s"] for i in range(len(ws) - 1))
    gaps = [ws[i + 1]["s"] - ws[i]["e"] for i in range(len(ws) - 1)]
    rows.append((d, j.get("provider"), j.get("model"), j.get("voice"), round(j["duration"], 1), round(wer * 100, 1), len(ws), mono, round(max(gaps) if gaps else 0, 2)))
print(f"{'dir':32} {'provider':12} {'model':22} {'voice':14} {'dur':>6} {'WER%':>6} {'words':>6} {'mono':>5} {'maxgap':>7}")
for r in rows: print(f"{r[0]:32} {str(r[1]):12} {str(r[2]):22} {str(r[3]):14} {r[4]:>6} {r[5]:>6} {r[6]:>6} {str(r[7]):>5} {r[8]:>7}")
# consistency: group dirs ending in -1/-2/-3
groups = {}
for r in rows: groups.setdefault(re.sub(r"-\d$", "", r[0]), []).append(r[4])
for g, ds in groups.items():
    if len(ds) > 1: print(f"consistency {g}: durations {ds} → stdev {statistics.stdev(ds):.2f}s")
