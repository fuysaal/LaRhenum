# La'Rhen Reconnaissance Tool

![Banner](https://img.shields.io/badge/Advanced-Recon_Tool-red)
![Python](https://img.shields.io/badge/Python-3.6+-blue)
![Go](https://img.shields.io/badge/Go-1.16+-green)
![License](https://img.shields.io/badge/License-MIT-yellow)

An automated reconnaissance tool for bug bounty hunters and penetration testers that gathers subdomains from multiple sources and performs HTTP analysis.

##  Features

- **Multi-source subdomain enumeration**: AssetFinder, SubFinder, Samoscout, CRT.sh
- **HTTP Analysis**: Live subdomain checking with status codes
- **JSON Output**: Detailed results in JSON format
- **Status Code Organization**: Automatically categorizes URLs by HTTP status codes
- **Beautiful Interface**: Colorful, animated command-line interface
- **Progress Indicators**: Real-time progress animations

##  Requirements

### System Requirements
- Linux, macOS, or WSL (Windows Subsystem for Linux)
- Python 3.6+
- Go 1.16+
- curl, jq, git

### Go Tools Required
- [assetfinder](https://github.com/tomnomnom/assetfinder)
- [subfinder](https://github.com/projectdiscovery/subfinder)
- [anew](https://github.com/tomnomnom/anew)
- [samoscout](https://github.com/samogod/samoscout)
- [httpx](https://github.com/projectdiscovery/httpx)

##  Quick Installation

### Method 1: Using Install Script (Recommended)

```bash
# Clone the repository
git clone https://github.com/yourusername/advanced-recon-tool.git
cd advanced-recon-tool

# Make install script executable
chmod +x install.sh

# Run the installer
./install.sh
