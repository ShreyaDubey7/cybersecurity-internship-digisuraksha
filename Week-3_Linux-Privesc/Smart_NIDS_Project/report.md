
Network IDS — Student Project Report
===================================

Objective
---------
Simple NIDS to detect ICMP pings/floods, TCP connection attempts, simple scans (SYN/NULL/FIN), and suspicious behaviors.

Design & Approach
-----------------
- Packet parsing done via Scapy when available; unit tests use simple dicts.
- Detection uses short time-window counters to reduce noise.
- Configurable thresholds via `config.json`.

Limitations & Future Work
-------------------------
- Stateful TCP tracking can be improved.
- Logging/alert persistence needed for real deployments.
- False positives must be tuned per network baseline.
