
# Network NIDS (Human-style Project)
A small Network Intrusion Detection System (NIDS) 
It detects simple things: ICMP pings/floods, SYN scans, NULL/FIN scans.

## What I included
- `main.py` — run this to analyze a PCAP or do a live capture (simple CLI).
- `nids/` — package containing the detector and a tiny utils file.
- `generate_pcaps.py` — helper to create `pcap_examples/` for testing (requires scapy).
- `config.json` — easy-to-edit thresholds.
- `tests/` — a couple of unit tests using dict-based packets.
- `report.md` — short report.

## Quick start (Windows + VS Code)
1. Open the folder in VS Code.
2. Terminal:
   ```powershell
   python -m venv venv
   Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
   venv\Scripts\activate
   pip install -r requirements.txt
   pip install scapy
   python .\generate_pcaps.py
   ```
3. Run the project:
   ```powershell
   # analyze example malicious PCAP
   python main.py analyze --pcap pcap_examples\malicious_traffic.pcap

   # analyze normal
   python main.py analyze --pcap pcap_examples\normal_traffic.pcap
   ```

## Tests
From project root:
```powershell
pytest -q
```

## Notes / limitations (be honest as a student)
- This is educational — not production ready.
- Thresholds are static (edit `config.json`).
- Live capture requires admin and scapy.
- You might see `WARNING: No libpcap provider available ! pcap won't be used` — that's ok on Windows.

