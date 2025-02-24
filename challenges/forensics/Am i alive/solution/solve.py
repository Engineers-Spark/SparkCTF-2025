from scapy.all import *

def extract_flag(pcap_file):
    packets = rdpcap(pcap_file)
    flag_chars = []

    # Extract packets only from the expected source IP
    valid_packets = [pkt for pkt in packets if IP in pkt and ICMP in pkt and pkt[IP].src == "10.0.0.1"]

    # Sort packets based on their capture time to reconstruct the correct order
    valid_packets.sort(key=lambda pkt: pkt.time)

    for packet in valid_packets:
        ttl_value = packet[IP].ttl
        if 32 <= ttl_value <= 126:  # Printable ASCII range
            flag_chars.append(chr(ttl_value))

    flag = "".join(flag_chars)
    print(f"Extracted Flag: {flag}")
    return flag

# Solve the challenge
extract_flag("challenge.pcap")