# generate_pcaps.py - quick script to create example PCAPs (requires scapy)
try:
    from scapy.all import IP, TCP, ICMP, wrpcap
except Exception:
    print("ERROR: scapy not installed. pip install scapy")
    raise SystemExit(1)

import os

pcap_dir = "pcap_examples"
os.makedirs(pcap_dir, exist_ok=True)

# normal
normal = [
    IP(dst="192.168.1.10", src="192.168.1.5")/TCP(dport=80, sport=12345, flags="S"),
    IP(dst="192.168.1.10", src="192.168.1.5")/TCP(dport=80, sport=12345, flags="SA"),
    IP(dst="192.168.1.10", src="192.168.1.5")/TCP(dport=80, sport=12345, flags="A"),
]
wrpcap(os.path.join(pcap_dir, "normal_traffic.pcap"), normal)

# malicious
mal = []
for _ in range(25):
    mal.append(IP(dst="192.168.1.10", src="10.0.0.1")/ICMP(type=8))
for p in range(1000, 1012):
    mal.append(IP(dst="192.168.1.20", src="10.0.0.2")/TCP(dport=p, sport=40000+p, flags="S"))
mal.append(IP(dst="192.168.1.30", src="10.0.0.3")/TCP(dport=22, sport=50000, flags=0))
mal.append(IP(dst="192.168.1.40", src="10.0.0.4")/TCP(dport=23, sport=50001, flags="F"))
wrpcap(os.path.join(pcap_dir, "malicious_traffic.pcap"), mal)

print("PCAPs created in pcap_examples/")
