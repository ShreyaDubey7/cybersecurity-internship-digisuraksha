from scapy.all import IP, ICMP, TCP, Raw, wrpcap

packets = []

# Normal ICMP echo and reply
packets.append(IP(src="192.168.1.10", dst="192.168.1.1")/ICMP()/b"hello")
packets.append(IP(src="192.168.1.1", dst="192.168.1.10")/ICMP()/b"hello")

# Normal TCP handshake + HTTP GET
syn = IP(src="192.168.1.10", dst="192.168.1.20")/TCP(sport=12345, dport=80, flags="S", seq=1000)
synack = IP(src="192.168.1.20", dst="192.168.1.10")/TCP(sport=80, dport=12345, flags="SA", seq=2000, ack=1001)
ack = IP(src="192.168.1.10", dst="192.168.1.20")/TCP(sport=12345, dport=80, flags="A", seq=1001, ack=2001)
http = IP(src="192.168.1.10", dst="192.168.1.20")/TCP(sport=12345, dport=80, flags="PA", seq=1001, ack=2001)/Raw(
    b"GET /index.html HTTP/1.1\r\nHost: test\r\n\r\n"
)

packets += [syn, synack, ack, http]

# Write to file
wrpcap("examples/normal.pcap", packets)
print("✅ normal.pcap created")
