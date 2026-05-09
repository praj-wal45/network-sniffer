# network-sniffer

🌐 **A Python-based real-time network packet capture and analysis tool**

**Project Link:** https://github.com/praj-wal45/network-sniffer

---

## 📋 Overview

Network Sniffer is a comprehensive Python application that captures and analyzes network traffic packets in real-time. It provides both a RESTful API backend and an interactive web-based dashboard for monitoring network traffic, understanding packet structures, and analyzing network protocols.

### Key Features

✅ **Real-Time Packet Capture** - Capture IPv4 packets with protocol detection  
✅ **REST API** - 10+ endpoints for programmatic access  
✅ **Interactive Dashboard** - Beautiful Streamlit web interface  
✅ **Advanced Filtering** - Search and filter by IP, protocol, and more  
✅ **Traffic Analytics** - Real-time statistics and charts  
✅ **Protocol Analysis** - TCP, UDP, ICMP, and more  
✅ **Data Export** - Export packets as JSON for further analysis  
✅ **Thread-Safe** - Multi-threaded packet capture and processing  

---

## 🏗️ Architecture

### System Design

```
┌─────────────────────────────────────────────────────────┐
│                    Frontend (Streamlit)                 │
│  - Dashboard with real-time stats                       │
│  - Packet viewer with pagination                        │
│  - Search & filter interface                            │
│  - Analytics & visualization                            │
└──────────────────────┬──────────────────────────────────┘
                       │ HTTP Requests
                       ↓
┌─────────────────────────────────────────────────────────┐
│                 API Backend (Flask)                      │
│  - RESTful endpoints                                     │
│  - Request validation                                   │
│  - Response formatting                                  │
│  - Error handling                                       │
└──────────────────────┬──────────────────────────────────┘
                       │
                       ↓
┌─────────────────────────────────────────────────────────┐
│              Packet Sniffer (Core Engine)               │
│  - Raw socket packet capture                            │
│  - IPv4 packet parsing                                  │
│  - Protocol detection                                   │
│  - Thread-safe buffering                                │
└──────────────────────┬──────────────────────────────────┘
                       │
                       ↓ (Requires Root/Admin)
┌─────────────────────────────────────────────────────────┐
│              Network Interface (OS Level)               │
│  - Linux: Raw socket AF_PACKET                          │
│  - Windows: Raw socket AF_INET                          │
│  - macOS: Raw socket AF_INET                            │
└─────────────────────────────────────────────────────────┘
```

---

## 📁 Project Structure

```
network-sniffer/
│
├── backend/                    # Backend services
│   ├── sniffer.py             # Core packet sniffer class (400+ lines)
│   └── api_server.py          # Flask REST API server (350+ lines)
│
├── frontend/                   # Frontend application
│   └── app.py                 # Streamlit dashboard (500+ lines)
│
├── utils/                      # Utilities & configuration
│   ├── config.py              # Configuration management
│   ├── logger.py              # Logging setup
│   └── requirements.txt        # Python dependencies
│
├── docs/                       # Documentation
│   ├── SETUP.md               # Installation & troubleshooting
│   └── API.md                 # API reference documentation
│
└── README.md                   # Project overview (this file)
```

---

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Root/Administrator privileges (for packet capture)
- 100MB free disk space

### Installation

```bash
# 1. Clone repository
git clone https://github.com/praj-wal45/network-sniffer.git
cd network-sniffer

# 2. Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r utils/requirements.txt
```

### Running

#### Terminal 1: Start Backend (needs sudo/admin)
```bash
sudo python backend/api_server.py
# Or on Windows (run as Administrator):
python backend\api_server.py
```

#### Terminal 2: Start Frontend
```bash
streamlit run frontend/app.py
```

**Access the dashboard:** http://localhost:8501

---

## 📚 Technology Stack

| Component | Technology | Version |
|-----------|-----------|---------|
| **Backend** | Flask | 2.3.0 |
| **Frontend** | Streamlit | 1.28.0 |
| **HTTP Client** | Requests | 2.31.0 |
| **Data Processing** | Pandas | 2.0.0 |
| **Visualization** | Plotly | 5.17.0 |
| **Packet Parsing** | Scapy | 2.5.0 |
| **Configuration** | python-dotenv | 1.0.0 |
| **Python** | Python | 3.8+ |

---

## 🔌 API Endpoints

### Sniffer Control
- `POST /api/sniffer/start` - Start packet capture
- `POST /api/sniffer/stop` - Stop packet capture
- `GET /api/sniffer/status` - Get sniffer status

### Packet Retrieval
- `GET /api/packets` - Get packets with pagination
- `GET /api/packets/filter` - Filter packets by criteria
- `GET /api/packets/search` - Search packets

### Analytics
- `GET /api/statistics` - Get traffic statistics

### Data Management
- `POST /api/packets/clear` - Clear packet buffer
- `GET /api/packets/export` - Export packets as JSON

### Health
- `GET /api/health` - Check API health

**Full documentation:** See [docs/API.md](docs/API.md)

---

## 💻 Frontend Features

### 📊 Dashboard Tab
- Real-time packet count and status
- Protocol distribution pie chart
- Top source and destination IPs
- Live metrics

### 📦 Packets Tab
- Paginated packet list (configurable limit)
- Sortable columns
- Display: Timestamp, Source IP, Destination IP, Protocol, TTL, Size
- Real-time updates

### 🔍 Search & Filter Tab
- **Search**: Find packets by IP address or protocol name
- **Filter**: Advanced filtering by source, destination, and protocol
- Support for multiple filters simultaneously

### 📈 Analytics Tab
- Protocol distribution statistics
- Traffic flow analysis
- Top 10 source and destination IPs
- Interactive charts

### ⚙️ Tools Tab
- Clear captured packets
- Export packets as JSON
- API health check
- Configuration guide

---

## 📊 Example Usage

### Via Web Dashboard
1. Open http://localhost:8501
2. Click **"Start Capture"**
3. Watch real-time packet statistics
4. Use Search/Filter to find specific packets
5. Export packets for analysis

### Via REST API

```bash
# Start capturing
curl -X POST http://localhost:5000/api/sniffer/start

# Get packets
curl http://localhost:5000/api/packets?limit=50&offset=0

# Search for specific IP
curl "http://localhost:5000/api/packets/search?q=192.168.1.1"

# Get statistics
curl http://localhost:5000/api/statistics

# Export all packets
curl http://localhost:5000/api/packets/export > packets.json

# Stop capturing
curl -X POST http://localhost:5000/api/sniffer/stop
```

### Via Python Client

```python
import requests

BASE_URL = "http://localhost:5000/api"

# Start sniffer
requests.post(f"{BASE_URL}/sniffer/start")

# Get packets
response = requests.get(f"{BASE_URL}/packets?limit=100")
packets = response.json()['data']

# Get statistics
stats = requests.get(f"{BASE_URL}/statistics").json()['data']
print(f"Total packets: {stats['total_packets']}")
print(f"Protocols: {stats['protocols']}")
```

---

## 🔧 Configuration

Create `.env` file in project root:

```env
# API Server
API_HOST=0.0.0.0
API_PORT=5000
DEBUG_MODE=False

# Packet Capture
PACKET_BUFFER_SIZE=5000
MAX_PACKET_DISPLAY=50

# Logging
LOG_LEVEL=INFO
LOG_FILE=network_sniffer.log

# Features
ENABLE_EXPORT=True
ENABLE_SEARCH=True
ENABLE_FILTER=True
```

---

## ⚠️ Requirements & Limitations

### System Requirements
- **OS**: Linux, macOS, Windows 10+
- **Python**: 3.8 or higher
- **RAM**: Minimum 512MB, Recommended 2GB+
- **Disk**: 100MB+ free space

### Privilege Requirements
- **Linux/macOS**: Root privileges (sudo)
- **Windows**: Administrator privileges (run as admin)
- Required for raw socket access to network interface

### Limitations
- Captures IPv4 packets only (IPv6 support in future versions)
- Limited by available system memory (default 5000 packets)
- Performance depends on network traffic volume
- Requires dedicated network interface (cannot capture on loopback)

---

## 🐛 Troubleshooting

### Common Issues

#### 1. Permission Denied
```
PermissionError: [Errno 1] Operation not permitted
```
**Solution**: Run with root/admin privileges
```bash
sudo python backend/api_server.py
```

#### 2. Port Already in Use
```
Address already in use
```
**Solution**: Change port in `.env` or kill existing process
```bash
# Kill process on port 5000
sudo lsof -i :5000 | grep LISTEN | awk '{print $2}' | xargs kill -9
```

#### 3. API Connection Error
**Solution**: Ensure API server is running and accessible
```bash
# Check if API is responding
curl http://localhost:5000/api/health
```

#### 4. No Packets Being Captured
**Solution**: Check network activity and permissions
```bash
# Verify network interface
ip link show        # Linux
ifconfig           # macOS
ipconfig          # Windows
```

**See [docs/SETUP.md](docs/SETUP.md) for more troubleshooting**

---

## 🔒 Security Notes

⚠️ **This is a development/educational tool. For production use:**

- [ ] Add authentication (JWT/API Keys)
- [ ] Enable HTTPS/TLS
- [ ] Restrict CORS to trusted origins
- [ ] Add rate limiting
- [ ] Implement access logs
- [ ] Use firewall rules to restrict access
- [ ] Run in isolated network environment
- [ ] Keep dependencies updated

---

## 📈 Performance Tips

1. **Optimize Buffer Size**: Adjust `PACKET_BUFFER_SIZE` based on available memory
2. **Use Filtering**: Filter packets before analysis for faster processing
3. **Export Regularly**: Export and clear packets to free memory
4. **Dedicated Interface**: Use separate network interface if available
5. **Monitor Resources**: Use system monitor to track CPU and memory usage

---

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

---

## 📝 License

This project is licensed under the MIT License - see LICENSE file for details.

---

## 🙏 Acknowledgments

- Built with Flask, Streamlit, and Scapy
- Inspired by network analysis tools like Wireshark
- Community feedback and contributions

---

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/praj-wal45/network-sniffer/issues)
- **Documentation**: [docs/](docs/)
- **API Reference**: [docs/API.md](docs/API.md)
- **Setup Guide**: [docs/SETUP.md](docs/SETUP.md)

---

## 🗓️ Roadmap

- [ ] IPv6 packet support
- [ ] DNS query analysis
- [ ] TLS/SSL certificate inspection
- [ ] Packet flow visualization
- [ ] Historical data analysis
- [ ] Real-time alerting
- [ ] Docker support
- [ ] Web-based configuration UI
- [ ] Unit and integration tests
- [ ] Performance optimization

---

**Made with ❤️ by [praj-wal45](https://github.com/praj-wal45)**

**Last Updated**: 2026-05-09  
**Version**: 1.0.0
