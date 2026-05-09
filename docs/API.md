# Network Sniffer - API Documentation

## Base URL
```
http://localhost:5000/api
```

## Authentication
Currently, no authentication is required. For production, implement JWT or API keys.

---

## Endpoints

### 1. Health Check

Check if the API server is running and healthy.

**Endpoint:** `GET /api/health`

**Response:**
```json
{
  "status": "healthy",
  "message": "Network Sniffer API is running"
}
```

**Status Code:** 200 OK

---

### 2. Start Sniffer

Start capturing network packets.

**Endpoint:** `POST /api/sniffer/start`

**Request Body:**
```json
{
  "packet_count": 0
}
```

**Parameters:**
- `packet_count` (optional, int): Number of packets to capture. 0 = infinite

**Response:**
```json
{
  "success": true,
  "message": "Packet sniffing started",
  "packet_count": 0
}
```

**Status Codes:** 
- 200 OK - Successfully started
- 400 Bad Request - Already running
- 500 Internal Server Error

---

### 3. Stop Sniffer

Stop capturing network packets.

**Endpoint:** `POST /api/sniffer/stop`

**Response:**
```json
{
  "success": true,
  "message": "Packet sniffing stopped",
  "packets_captured": 1234
}
```

**Status Codes:**
- 200 OK - Successfully stopped
- 400 Bad Request - Not running
- 500 Internal Server Error

---

### 4. Get Sniffer Status

Get current status of the packet sniffer.

**Endpoint:** `GET /api/sniffer/status`

**Response:**
```json
{
  "is_running": true,
  "packets_captured": 1234,
  "status": "running"
}
```

**Status Code:** 200 OK

---

### 5. Get Packets

Retrieve captured packets with pagination.

**Endpoint:** `GET /api/packets`

**Query Parameters:**
- `limit` (optional, int, default=50, max=500): Number of packets per page
- `offset` (optional, int, default=0): Starting position

**Example Request:**
```
GET /api/packets?limit=50&offset=0
```

**Response:**
```json
{
  "success": true,
  "data": [
    {
      "timestamp": "2026-05-09T10:30:45.123456",
      "src_ip": "192.168.1.100",
      "dest_ip": "8.8.8.8",
      "protocol": "UDP",
      "protocol_num": 17,
      "ttl": 64,
      "size": 512,
      "header_length": 20,
      "flags": ["DF"],
      "raw_data": "45000200..."
    }
  ],
  "pagination": {
    "limit": 50,
    "offset": 0,
    "total": 5000
  }
}
```

**Status Code:** 200 OK

---

### 6. Filter Packets

Filter captured packets by criteria.

**Endpoint:** `GET /api/packets/filter`

**Query Parameters:**
- `src_ip` (optional, string): Filter by source IP
- `dest_ip` (optional, string): Filter by destination IP
- `protocol` (optional, string): Filter by protocol (TCP, UDP, ICMP, etc.)

**Example Request:**
```
GET /api/packets/filter?src_ip=192.168.1.100&protocol=TCP
```

**Response:**
```json
{
  "success": true,
  "data": [
    {
      "timestamp": "2026-05-09T10:30:45.123456",
      "src_ip": "192.168.1.100",
      "dest_ip": "8.8.8.8",
      "protocol": "TCP",
      ...
    }
  ],
  "count": 523
}
```

**Status Code:** 200 OK

---

### 7. Search Packets

Search packets by IP address or protocol.

**Endpoint:** `GET /api/packets/search`

**Query Parameters:**
- `q` (required, string): Search query (IP or protocol name)

**Example Request:**
```
GET /api/packets/search?q=192.168.1.100
```

**Response:**
```json
{
  "success": true,
  "data": [
    {
      "timestamp": "2026-05-09T10:30:45.123456",
      "src_ip": "192.168.1.100",
      "dest_ip": "8.8.8.8",
      "protocol": "TCP",
      ...
    }
  ],
  "count": 156
}
```

**Status Codes:**
- 200 OK - Search successful
- 400 Bad Request - Missing search query

---

### 8. Get Statistics

Get aggregated traffic statistics.

**Endpoint:** `GET /api/statistics`

**Response:**
```json
{
  "success": true,
  "data": {
    "total_packets": 5000,
    "protocols": {
      "TCP": 2500,
      "UDP": 1800,
      "ICMP": 700
    },
    "top_sources": [
      {
        "ip": "192.168.1.100",
        "count": 800
      },
      {
        "ip": "192.168.1.101",
        "count": 650
      }
    ],
    "top_destinations": [
      {
        "ip": "8.8.8.8",
        "count": 1200
      },
      {
        "ip": "1.1.1.1",
        "count": 950
      }
    ]
  }
}
```

**Status Code:** 200 OK

---

### 9. Clear Packets

Clear all captured packets from buffer.

**Endpoint:** `POST /api/packets/clear`

**Response:**
```json
{
  "success": true,
  "message": "Packet buffer cleared"
}
```

**Status Codes:**
- 200 OK - Successfully cleared
- 500 Internal Server Error

---

### 10. Export Packets

Export captured packets as JSON.

**Endpoint:** `GET /api/packets/export`

**Query Parameters:**
- `format` (optional, string, default="json"): Export format

**Response:**
```json
{
  "success": true,
  "format": "json",
  "count": 5000,
  "data": [
    {
      "timestamp": "2026-05-09T10:30:45.123456",
      "src_ip": "192.168.1.100",
      "dest_ip": "8.8.8.8",
      "protocol": "TCP",
      ...
    }
  ]
}
```

**Status Code:** 200 OK

---

## Data Models

### Packet Object

```typescript
{
  timestamp: string;        // ISO 8601 timestamp
  src_ip: string;          // Source IP address
  dest_ip: string;         // Destination IP address
  protocol: string;        // Protocol name (TCP, UDP, ICMP, etc.)
  protocol_num: number;    // Protocol number
  ttl: number;             // Time To Live
  size: number;            // Packet size in bytes
  header_length: number;   // IP header length
  flags: string[];         // Packet flags (DF, MF, etc.)
  raw_data: string;        // First 100 chars of hex data
}
```

### Statistics Object

```typescript
{
  total_packets: number;
  protocols: Record<string, number>;
  top_sources: Array<{ip: string, count: number}>;
  top_destinations: Array<{ip: string, count: number}>;
}
```

---

## Error Responses

### 400 Bad Request
```json
{
  "success": false,
  "message": "Invalid request parameters"
}
```

### 404 Not Found
```json
{
  "success": false,
  "message": "Endpoint not found"
}
```

### 500 Internal Server Error
```json
{
  "success": false,
  "message": "Internal server error"
}
```

---

## Rate Limiting

Currently no rate limiting is implemented. 

**Recommended limits for production:**
- 100 requests per minute per IP
- Maximum 1000 packets per export request

---

## Examples

### cURL Examples

#### Start sniffing:
```bash
curl -X POST http://localhost:5000/api/sniffer/start
```

#### Get packets:
```bash
curl http://localhost:5000/api/packets?limit=10&offset=0
```

#### Filter by source IP:
```bash
curl "http://localhost:5000/api/packets/filter?src_ip=192.168.1.100"
```

#### Search packets:
```bash
curl "http://localhost:5000/api/packets/search?q=TCP"
```

#### Get statistics:
```bash
curl http://localhost:5000/api/statistics
```

#### Export packets:
```bash
curl http://localhost:5000/api/packets/export > packets.json
```

### Python Example

```python
import requests

BASE_URL = "http://localhost:5000/api"

# Start sniffer
response = requests.post(f"{BASE_URL}/sniffer/start")
print(response.json())

# Get packets
response = requests.get(f"{BASE_URL}/packets", params={"limit": 50})
packets = response.json()["data"]

# Get statistics
response = requests.get(f"{BASE_URL}/statistics")
stats = response.json()["data"]
print(f"Total packets: {stats['total_packets']}")
```

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2026-05-09 | Initial API release |

---

**Last Updated:** 2026-05-09
