#!/usr/bin/env python3
# main.py - small CLI wrapper (student style)
# You can run "python main.py analyze --pcap path" or "python main.py live --iface interface"

import argparse, sys, os

# allow running from anywhere by adding project root to path (practical for students)
ROOT = os.path.dirname(__file__)
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

def analyze_cmd(args):
    # lazy import to keep startup fast
    try:
        from nids.detector import DetectionEngine
        from scapy.all import rdpcap
    except Exception as e:
        print("Missing dependency (scapy). Install it: pip install scapy")
        sys.exit(1)
    engine = DetectionEngine()
    print(f"[INFO] Reading PCAP: {args.pcap}")
    pkts = rdpcap(args.pcap)
    for p in pkts:
        engine.detect_packet(p)
    print("[INFO] Alerts:")
    for a in engine.alerts:
        print(a)

def live_cmd(args):
    try:
        from nids.detector import DetectionEngine
        from scapy.all import sniff
    except Exception:
        print("Live capture requires scapy. pip install scapy")
        sys.exit(1)
    engine = DetectionEngine()
    print(f"[INFO] Starting live capture on {args.iface} (Ctrl-C to stop)")
    sniff(iface=args.iface, prn=engine.detect_packet, store=False)

def main():
    parser = argparse.ArgumentParser(description="Student NIDS main")
    sub = parser.add_subparsers(dest="cmd")
    p1 = sub.add_parser("analyze")
    p1.add_argument("--pcap", required=True)
    p2 = sub.add_parser("live")
    p2.add_argument("--iface", required=True)
    args = parser.parse_args()
    if args.cmd == "analyze":
        analyze_cmd(args)
    elif args.cmd == "live":
        live_cmd(args)
    else:
        parser.print_help()

if __name__ == '__main__':
    main()
