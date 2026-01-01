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
```

### Method 2: Manual Installation
```bash
# Clone the repository
git clone https://github.com/yourusername/advanced-recon-tool.git
cd advanced-recon-tool

# Install Python dependencies
pip3 install -r requirements.txt

# Install Go tools
go install github.com/tomnomnom/assetfinder@latest
go install github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest
go install github.com/tomnomnom/anew@latest
go install github.com/samogod/samoscout@latest
go install github.com/projectdiscovery/httpx/cmd/httpx@latest

# Add Go binaries to PATH (add to ~/.bashrc or ~/.zshrc)
export PATH=$PATH:$(go env GOPATH)/bin

# Make the tool executable
chmod +x advanced_recon.py
```

## 📖 Usage

### Basic Usage
```bash
./advanced_recon.py
```

### Example Run
```bash
$ ./advanced_recon.py

╔════════════════════════════════════════════════════════════╗
║                                                            ║
  TARGET WILDCARD (e.g., target.com)
║                                                            ║
╚════════════════════════════════════════════════════════════╝

[?] Domain: example.com

[*] Checking tools...
[✓] All tools available!
[*] Initializing...
```

### Workflow

1-)Enter Target Domain: Provide the target domain (e.g., example.com)

2-)Subdomain Enumeration: Tool gathers subdomains from multiple sources

3-)Result Merging: Combines and deduplicates all subdomains

4-)Live Checking: Optional HTTPX scan to find live subdomains

5-)Status Code Analysis: Categorizes results by HTTP status codes

6-)Organization: Creates organized directory structure

### Output Structure
```bash
recon_example.com_20231215_143022/
├── all_subs.txt              # All discovered subdomains
├── httpx_results.json        # Detailed HTTPX results (JSON)
├── live_subs.txt            # Live subdomains
└── status_codes/            # Organized by status code
    ├── sc200.txt           # URLs with 200 OK
    ├── sc301.txt           # URLs with 301 Moved Permanently
    ├── sc302.txt           # URLs with 302 Found
    ├── sc401.txt           # URLs with 401 Unauthorized
    ├── sc403.txt           # URLs with 403 Forbidden
    ├── sc404.txt           # URLs with 404 Not Found
    └── interestingsc.txt   # Other interesting status codes
```
### Tool Options

The tool runs automatically through all stages:

  1-)AssetFinder: Subdomain enumeration

  2-)SubFinder: Comprehensive subdomain discovery

  3-)Samoscout: Additional subdomain source

  4-)CRT.sh: Certificate transparency logs

  5-)HTTPX: Live subdomain checking and analysis

###  Status Code Analysis

The tool automatically analyzes HTTPX JSON output and organizes URLs:

  1-)200 OK: Working websites

  2-)301/302: Redirects

  3-)401: Authentication required

  4-)403: Access forbidden

  5-)404: Not found

  6-)Others: Interesting status codes (500, 503, etc.)

### Troubleshooting

1-)Command not found" for Go tools
```bash
export PATH=$PATH:$(go env GOPATH)/bin
# Add to ~/.bashrc or ~/.zshrc
```

2-)Python dependencies error
```bash
pip3 install --upgrade pip
pip3 install colorama
```

3-)Permission denied
```bash
chmod +x advanced_recon.py
chmod +x install.sh
```

4-)JSON parsing errors
    - Ensure jq is installed: sudo apt install jq or brew install jq

## License

## Author
La'Rhen - Advanced Recon Tool
