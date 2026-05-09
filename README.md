# network-sniffer

**Project Link:** https://security-dashboard-40.preview.emergentagent.com/

## **Network Sniffer - Theory**

### **What is a Network Sniffer?**
A network sniffer (also called a packet analyzer or packet sniffer) is a tool that captures and inspects data packets traveling across a network in real-time.

### **How Network Sniffing Works:**

1. **Packet Capture:** 
   - Network interface card (NIC) operates in promiscuous mode
   - Captures all data packets passing through the network segment
   - Not just packets destined for that machine

2. **Packet Structure:**
   - **Header:** Contains metadata (source/destination IP, protocol type, port numbers)
   - **Payload:** Actual data being transmitted
   - **Trailer:** Error-checking information (CRC)

3. **OSI Model Layers Involved:**
   - **Layer 2 (Data Link):** MAC addresses, frame structure
   - **Layer 3 (Network):** IP addresses, routing
   - **Layer 4 (Transport):** TCP/UDP ports, connection info
   - **Layer 7 (Application):** Actual data content

### **Common Protocols Analyzed:**
- **TCP/IP:** Connection-oriented communication
- **UDP:** Connectionless communication
- **HTTP/HTTPS:** Web traffic
- **DNS:** Domain name resolution
- **ICMP:** Network diagnostics (ping)

### **Use Cases:**
- Network troubleshooting and diagnosis
- Security monitoring and intrusion detection
- Performance analysis
- Protocol learning and education
- Network forensics

### **Key Libraries Used:**
- **Scapy:** Python packet manipulation and crafting
- **Socket:** Low-level network interface
- **Pcap:** Packet capture framework

### **Advantages:**
- Real-time network visibility
- Protocol understanding
- Network security analysis
- Educational learning tool

### **Limitations:**
- Requires administrator/root privileges
- Cannot capture encrypted traffic (HTTPS)
- High network traffic can overwhelm the sniffer
- Privacy and legal concerns
