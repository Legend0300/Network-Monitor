﻿# Cybersecurity Tools & Network Analysis Suite

A comprehensive collection of Python-based cybersecurity tools for network analysis, vulnerability scanning, process monitoring, and security testing.

## 🛠️ Tools Overview

### 1. Network Dashboard (`network_dashboard.py`)
A real-time web-based dashboard for monitoring and controlling network-connected processes.

**Features:**
- 🌐 Monitor all applications using internet connections
- 🚫 Suspend/resume processes (network blocking simulation)
- 📊 Real-time CPU and memory usage monitoring
- ⏱️ Auto-resume blocked processes after 5 seconds
- 🎯 Kill processes directly from the web interface

**Usage:**
```bash
python3 network_dashboard.py
```
Access at: http://localhost:5000

### 2. Network Test Process (`test_network_process.py`)
A test application that generates continuous network activity to demonstrate blocking behavior.

**Features:**
- 🔄 Continuous HTTP requests to multiple endpoints
- 🔗 TCP connection attempts to various servers
- 📈 Real-time status reporting every 10 seconds
- 🚨 Automatic detection of network blocking
- 📊 Success rate tracking and failure analysis

**Usage:**
```bash
python3 test_network_process.py
```
## 🚀 Quick Start

### Prerequisites
- Python 3.7+
- Linux environment (tested on Kali Linux)
- sudo privileges (for network blocking features)

### Installation

1. **Install Python dependencies:**
```bash
pip3 install flask psutil requests python-nmap
```

2. **Make scripts executable:**
```bash
chmod +x block_network.sh
chmod +x install_deps.sh
```

3. **Start the main dashboard:**
```bash
python3 network_dashboard.py
```

4. **In another terminal, start the test process:**
```bash
python3 test_network_process.py
```

5. **Open your browser and navigate to:**
```
http://localhost:5000
```

## 🔧 Configuration

### Network Dashboard
- **Port:** 5000 (configurable in source)
- **Auto-unblock timeout:** 5 seconds
- **Process monitoring:** Real-time via psutil

### Test Network Process
- **HTTP request interval:** 1.5 seconds
- **TCP connection interval:** 2 seconds
- **Status report interval:** 10 seconds

## 🛡️ Security Features

### Process Control
- **Suspend/Resume:** Safely pause network processes
- **Kill Process:** Terminate misbehaving applications
- **Auto-recovery:** Automatic process resumption after timeout

### Network Monitoring
- **Real-time tracking:** Monitor all internet-connected processes
- **Resource usage:** CPU and memory monitoring
- **Connection analysis:** Track active network connections

### System-level Blocking
- **iptables integration:** System-wide traffic control
- **Selective blocking:** Target specific processes or global blocking
- **Rule management:** Automatic cleanup and restoration

## 📊 Use Cases

### 1. Malware Analysis
- Monitor suspicious process network activity
- Block/unblock processes to analyze behavior
- Track resource consumption patterns

### 2. Network Security Testing
- Test application behavior under network restrictions
- Simulate network outages and connectivity issues
- Analyze application resilience

### 3. Penetration Testing
- Network reconnaissance and port scanning
- Service enumeration and version detection
- Exploit mapping and vulnerability analysis

### 4. System Administration
- Monitor and control network-heavy applications
- Troubleshoot network connectivity issues
- Manage bandwidth usage by process

## 🔍 Monitoring Capabilities

### Real-time Metrics
- Active network connections per process
- CPU usage percentage
- Memory consumption (MB)
- Process status (running, suspended, etc.)

### Network Analysis
- Local vs remote connection detection
- Protocol analysis (TCP/UDP)
- Port and service identification
- Traffic volume monitoring

## ⚠️ Important Notes

### Permissions
- Network dashboard requires standard user privileges
- System-wide blocking (`block_network.sh`) requires sudo
- Some monitoring features may need elevated privileges

### Compatibility
- Designed for Linux environments
- Tested on Kali Linux
- iptables required for system-wide blocking features

### Safety
- Auto-unblock feature prevents permanent process suspension
- Graceful error handling for missing processes
- Safe process termination procedures

## 🤝 Contributing

This toolkit is designed for educational and legitimate security testing purposes. When contributing:

1. Follow secure coding practices
2. Add appropriate error handling
3. Document new features thoroughly
4. Test on multiple Linux distributions

## 📝 License

This project is intended for educational and authorized security testing purposes only. Users are responsible for compliance with applicable laws and regulations.

---

**⚡ Quick Test:**
1. Run `python3 network_dashboard.py`
2. Run `python3 test_network_process.py` in another terminal
3. Open http://localhost:5000
4. Try blocking/unblocking the test process
5. Watch the real-time behavior in both the web interface and terminal

**🎯 Perfect for:** Security researchers, penetration testers, system administrators, and cybersecurity students learning about network monitoring and process control.
