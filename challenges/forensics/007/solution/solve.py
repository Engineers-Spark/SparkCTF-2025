from scapy.all import *
import re

def extract_flag_from_pcap(pcap_file):
    packets = rdpcap(pcap_file)
    flag_parts = []
    
    # Common OS substrings to filter out junk User-Agent values
    os_signatures = ["Windows NT", "Macintosh", "Linux", "Android"]
    
    for packet in packets:
        if packet.haslayer(Raw):
            payload = packet[Raw].load.decode(errors="ignore")
            match = re.search(r'User-Agent: Mozilla/5.0 \((.*?)\)', payload)
            if match:
                user_agent_part = match.group(1)
                # Only keep User-Agent values that are not common OS signatures
                if not any(os in user_agent_part for os in os_signatures):
                    flag_parts.append((packet.time, user_agent_part))  # Store timestamp for ordering
    
    # Sort by timestamp to maintain correct order
    flag_parts.sort()
    flag = "".join(part[1] for part in flag_parts)
    
    print(f"Extracted Flag: {flag}")
    return flag

# Run the extractor
pcap_file = "../challenge/007.pcap"  # Update if needed
extract_flag_from_pcap(pcap_file)