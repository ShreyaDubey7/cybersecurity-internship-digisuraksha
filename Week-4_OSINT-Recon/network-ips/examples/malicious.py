from scapy.all import IP, ICMP, TCP, Raw, wrpcap

packets = []

# ICMP flood (lots of pings)
for i in range(50):
    packets.append(IP(src="10.0.0.5", dst="10.0.0.1")/ICMP()/b"flood")

# SYN flood (many SYNs without completing handshake)
for i in range(60, 80):
    packets.append(IP(src="10.0.0.6", dst="10.0.0.1")/TCP(sport=10000+i, dport=80, flags="S", seq=1234+i))

# Port scan (SYNs to many different ports)
for port in range(1000, 1035):
    packets.append(IP(src="10.0.0.7", dst="10.0.0.1")/TCP(sport=40000, dport=port, flags="S", seq=4000+port))

# HTTP SQL injection attempt
sqli_payload = b"GET /search?q=' or 1=1 -- HTTP/1.1\r\nHost: victim\r\n\r\n"
packets.append(
    IP(src="10.0.0.8", dst="10.0.0.1")/TCP(sport=1234, dport=80, flags="PA", seq=5555, ack=6666)/Raw(sqli_payload)
)

# Write to file
wrpcap("examples/malicious.pcap", packets)
print("✅ malicious.pcap created")
