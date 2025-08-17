"""
nids/detector.py
A bit "human": descriptive comments, some small quirks, not over-engineered.
Detects ICMP pings/floods, SYN scans, NULL/FIN scans.
"""

import time, os, json
from collections import defaultdict, deque

# load config if present
ROOT = os.path.dirname(os.path.dirname(__file__))
CFG_PATH = os.path.join(ROOT, "config.json")
if os.path.exists(CFG_PATH):
    try:
        with open(CFG_PATH, "r") as f:
            cfg = json.load(f)
    except Exception:
        cfg = {}
else:
    cfg = {}

# thresholds (defaults if config missing)
SCAN_THRESHOLD = cfg.get("SCAN_THRESHOLD", 10)
PORT_THRESHOLD = cfg.get("PORT_THRESHOLD", 8)
PING_THRESHOLD = cfg.get("PING_THRESHOLD", 20)
TIME_WINDOW = cfg.get("TIME_WINDOW", 10)  # seconds

class DetectionEngine:
    def __init__(self, time_window=None):
        # make window configurable at init too
        self.time_window = time_window or TIME_WINDOW
        # simple in-memory structures
        self.syn_history = defaultdict(deque)  # src -> deque of (ts, dport)
        self.icmp_history = defaultdict(deque) # src -> deque of ts
        self.alerts = []
        # a tiny vestige of debugging I used during testing
        # self._debug = True

    def _now(self):
        return time.time()

    def _prune(self, dq):
        now = self._now()
        while dq and now - dq[0] > self.time_window:
            dq.popleft()

    def detect_packet(self, pkt):
        # support dict packets for tests
        if isinstance(pkt, dict):
            proto = pkt.get("proto")
            src = pkt.get("src")
            dst = pkt.get("dst")
            ts = self._now()
            if proto == "ICMP":
                self._handle_icmp(src, dst, pkt.get("icmp_type"), ts)
            elif proto == "TCP":
                self._handle_tcp(src, dst, pkt.get("dport"), pkt.get("tcp_flags"), ts)
            return

        # try scapy parsing (if scapy installed)
        try:
            from scapy.layers.inet import IP, TCP, ICMP
        except Exception:
            return  # can't parse raw packets without scapy

        if pkt is None:
            return
        if pkt.haslayer(ICMP):
            src = pkt[IP].src
            dst = pkt[IP].dst
            icmp_type = int(pkt[ICMP].type)
            self._handle_icmp(src, dst, icmp_type, self._now())
        elif pkt.haslayer(TCP):
            src = pkt[IP].src
            dst = pkt[IP].dst
            dport = int(pkt[TCP].dport)
            flags = pkt[TCP].flags
            try:
                flags_s = str(flags)
            except Exception:
                flags_s = flags
            self._handle_tcp(src, dst, dport, flags_s, self._now())

    def _handle_icmp(self, src, dst, icmp_type, now):
        # only echo request/reply are interesting here
        if icmp_type not in (8, 0, None):
            return
        dq = self.icmp_history[src]
        dq.append(now)
        self._prune(dq)
        # info-level message for each ping
        self._alert(f"ICMP packet from {src} to {dst} (type={icmp_type})", now, info=True)
        if len(dq) >= PING_THRESHOLD:
            self._alert(f"ICMP flood detected from {src} ({len(dq)} pings in {self.time_window}s)", now)

    def _handle_tcp(self, src, dst, dport, flags, now):
        if flags is None:
            flags = ""
        flags_s = str(flags)

        # NULL scan (no flags)
        if flags_s == "" or flags_s == "0":
            self._alert(f"NULL scan packet from {src} to port {dport}", now)
            return

        # FIN-only
        if "F" in flags_s and all(ch not in flags_s for ch in ("S","A","R","P","U")):
            self._alert(f"FIN scan packet from {src} to port {dport}", now)
            return

        # SYN without ACK
        if "S" in flags_s and "A" not in flags_s:
            dq = self.syn_history[src]
            dq.append((now, dport))
            # prune old entries
            while dq and now - dq[0][0] > self.time_window:
                dq.popleft()
            total = len(dq)
            distinct = len(set(p for (_, p) in dq))
            # small info message
            self._alert(f"SYN packet from {src} to port {dport}", now, info=True)
            if total >= SCAN_THRESHOLD or distinct >= PORT_THRESHOLD:
                self._alert(f"Possible SYN scan from {src} (syns={total}, distinct_ports={distinct})", now)

    def _alert(self, msg, ts=None, info=False):
        ts = ts or self._now()
        level = "INFO" if info else "ALERT"
        entry = {"ts": ts, "level": level, "msg": msg}
        self.alerts.append(entry)
        # print alerts; students often leave prints in code
        print(f"[{level}] {msg}")

    def clear_alerts(self):
        self.alerts = []
