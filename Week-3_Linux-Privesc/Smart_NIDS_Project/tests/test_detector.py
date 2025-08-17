# tests/test_detector.py - unit tests using simple dicts
from nids.detector import DetectionEngine

def test_icmp_flood():
    e = DetectionEngine(time_window=2)
    e.clear_alerts()
    for _ in range(22):
        e.detect_packet({'proto':'ICMP','src':'10.0.0.1','dst':'192.168.1.10','icmp_type':8})
    assert any('ICMP flood' in a['msg'] for a in e.alerts)

def test_syn_scan():
    e = DetectionEngine(time_window=2)
    e.clear_alerts()
    for p in range(1000,1000+12):
        e.detect_packet({'proto':'TCP','src':'10.0.0.2','dst':'192.168.1.20','dport':p,'tcp_flags':'S'})
    assert any('Possible SYN scan' in a['msg'] for a in e.alerts)
