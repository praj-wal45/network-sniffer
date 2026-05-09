from scapy.all import sniff

def packet_callback(packet):
    print(packet.summary())

# Note: Run this script with administrator privileges
# Sniff 10 packets on the default interface
sniff(prn=packet_callback, count=10)