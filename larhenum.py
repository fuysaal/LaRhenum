#!/usr/bin/env python3

import os
import sys
import json
import time
import shutil
import subprocess
import threading
from datetime import datetime
from colorama import init, Fore, Style, Back

init(autoreset=True)

class Larhenum:
    def __init__(self):
        self.target = ""
        self.recon_dir = ""
        self.stop_event = threading.Event()
        self.user_home = os.path.expanduser("~")
        self.tools_dir = os.path.join(self.user_home, "Larhen_Tools")
        
    def clear_screen(self):
        os.system('clear' if os.name != 'nt' else 'cls')
    
    def print_banner(self):
        banner = f"""{Fore.RED}
        
        
	$$\              $$\ $$$$$$$\  $$\                                                                                                     
	$$ |             $  |$$  __$$\ $$ |                                                                                                    
	$$ |      $$$$$$\\_/ $$ |  $$ |$$$$$$$\   $$$$$$\  $$$$$$$\  $$\   $$\ $$$$$$\$$$$\                                                    
	$$ |      \____$$\   $$$$$$$  |$$  __$$\ $$  __$$\ $$  __$$\ $$ |  $$ |$$  _$$  _$$\                                                   
	$$ |      $$$$$$$ |  $$  __$$< $$ |  $$ |$$$$$$$$ |$$ |  $$ |$$ |  $$ |$$ / $$ / $$ |                                                  
	$$ |     $$  __$$ |  $$ |  $$ |$$ |  $$ |$$   ____|$$ |  $$ |$$ |  $$ |$$ | $$ | $$ |                                                  
	$$$$$$$$\\$$$$$$$ |  $$ |  $$ |$$ |  $$ |\$$$$$$$\ $$ |  $$ |\$$$$$$  |$$ | $$ | $$ |                                                  
	\________|\_______|  \__|  \__|\__|  \__| \_______|\__|  \__| \______/ \__| \__| \__|                                                  
                                                                                                                                                                                                                                                                              
                                                                                                                                                                                                                                                                                                                                                                                                                     
{Style.RESET_ALL}{Fore.YELLOW}
╔══════════════════════════════════════════╗
║         Advanced Reconnaissance Tool     ║
╚══════════════════════════════════════════╝{Style.RESET_ALL}
"""
        print(banner)
        print(f"{Fore.CYAN}Version: 1.0.0{Style.RESET_ALL}")
        print(f"{Fore.CYAN}Author: La'Rhen{Style.RESET_ALL}")
        print("=" * 45)
        print()
    
    def animate_progress(self, message, completed=False):
        if completed:
            sys.stdout.write(f'\r{Fore.GREEN}[■■■■■■■■■■]{Style.RESET_ALL} {message}')
            sys.stdout.flush()
            time.sleep(0.3)
            return
        
        frames = ["[■□□□□□□□□□]", "[■■□□□□□□□□]", "[■■■□□□□□□□]",
                 "[■■■■□□□□□□]", "[■■■■■□□□□□]", "[■■■■■■□□□□]",
                 "[■■■■■■■□□□]", "[■■■■■■■■□□]", "[■■■■■■■■■□]"]
        
        i = 0
        while not self.stop_event.is_set():
            frame_idx = i % len(frames)
            color = Fore.GREEN if i % 2 == 0 else Fore.YELLOW
            sys.stdout.write(f'\r{color}{frames[frame_idx]}{Style.RESET_ALL} {message}')
            sys.stdout.flush()
            time.sleep(0.1)
            i += 1
    
    def run_tool_with_progress(self, cmd, tool_name, show_cmd=True):
        if show_cmd:
            print(f"\n{Fore.YELLOW}╔══════════════════[{tool_name}]══════════════════╗{Style.RESET_ALL}")
            clean_cmd = cmd.split('>')[0].strip() if '>' in cmd else cmd
            print(f"{Fore.WHITE}{clean_cmd}{Style.RESET_ALL}")
        else:
            print(f"\n{Fore.YELLOW}╔══════════════════[{tool_name}]══════════════════╗{Style.RESET_ALL}")
        
        self.stop_event.clear()
        anim_thread = threading.Thread(
            target=self.animate_progress,
            args=(f"Running {tool_name}",)
        )
        anim_thread.start()
        
        try:
            process = subprocess.Popen(
                cmd,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            stdout, stderr = process.communicate(timeout=900)
            
            self.stop_event.set()
            anim_thread.join()
            
            self.animate_progress(f"{tool_name} completed", completed=True)
            print()
            
            if process.returncode == 0:
                return True, stdout
            else:
                return False, stderr
                
        except subprocess.TimeoutExpired:
            process.kill()
            self.stop_event.set()
            anim_thread.join()
            print(f"\r{Fore.RED}[✗]{Style.RESET_ALL} {tool_name} timeout")
            return False, "Timeout"
        except Exception as e:
            self.stop_event.set()
            anim_thread.join()
            print(f"\r{Fore.RED}[✗]{Style.RESET_ALL} {tool_name} error")
            return False, str(e)
    
    def create_dirs(self):
        print(f"\n{Fore.BLUE}[*]{Style.RESET_ALL} Creating directory structure...")
        
        dirs = [
            "httpx",
            "status_codes", 
            "Cors_Misconfiguration",
            "links_urls",
            "js_analyst",
            "API_Endpoints"
        ]
        
        for dir_name in dirs:
            dir_path = os.path.join(self.recon_dir, dir_name)
            os.makedirs(dir_path, exist_ok=True)
    
    def get_target(self):
        print(f"\n{Fore.YELLOW}[?]{Style.RESET_ALL} Enter target domain (e.g., target.com): ", end="")
        self.target = input().strip()
        
        if not self.target:
            print(f"{Fore.RED}[✗]{Style.RESET_ALL} Target domain is required")
            sys.exit(1)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M")
        self.recon_dir = f"recon_{self.target}_{timestamp}"
        
        print(f"\n{Fore.CYAN}[*]{Style.RESET_ALL} Target: {self.target}")
        print(f"{Fore.CYAN}[*]{Style.RESET_ALL} Directory: {self.recon_dir}")
    
    def collect_subdomains(self):
        print(f"\n{Fore.BLUE}[*]{Style.RESET_ALL} Collecting subdomains...")
        
        tools = [
            (f"assetfinder --subs-only {self.target} > {self.recon_dir}/assetfinder.txt", "assetfinder"),
            (f"subfinder -d {self.target} -all -recursive -silent > {self.recon_dir}/subfinder.txt", "subfinder"),
            (f"samoscout -d {self.target} -silent > {self.recon_dir}/samoscout.txt", "samoscout"),
            (f"curl -s 'https://crt.sh/?q=%25.{self.target}&output=json' | jq -r '.[].name_value' | sed 's/\\*\\.//g' | sort -u > {self.recon_dir}/crtsh.txt", "crt.sh")
        ]
        
        all_subs = set()
        
        for cmd, tool_name in tools:
            success, output = self.run_tool_with_progress(cmd, tool_name)
            if success:
                output_file = f"{self.recon_dir}/{tool_name}.txt"
                if os.path.exists(output_file):
                    with open(output_file, 'r') as f:
                        lines = [line.strip() for line in f if line.strip()]
                    all_subs.update(lines)
                    print(f"   {Fore.GREEN}[✓]{Style.RESET_ALL} {tool_name}: {len(lines)}")
            else:
                print(f"   {Fore.YELLOW}[!]{Style.RESET_ALL} {tool_name}")
        
        all_subs_file = f"{self.recon_dir}/all_subs.txt"
        with open(all_subs_file, 'w') as f:
            f.write('\n'.join(sorted(all_subs)))
        
        for file in ["assetfinder.txt", "subfinder.txt", "samoscout.txt", "crtsh.txt"]:
            file_path = os.path.join(self.recon_dir, file)
            if os.path.exists(file_path):
                os.remove(file_path)
        
        print(f"\n{Fore.GREEN}[✓]{Style.RESET_ALL} Total subdomains: {len(all_subs)}")
        return len(all_subs)
    
    def run_httpx(self):
        print(f"\n{Fore.BLUE}[*]{Style.RESET_ALL} Finding live hosts...")
        
        httpx_dir = os.path.join(self.recon_dir, "httpx")
        subs_file = os.path.join(self.recon_dir, "all_subs.txt")
        
        if not os.path.exists(subs_file):
            print(f"   {Fore.RED}[✗]{Style.RESET_ALL} No subdomains file")
            return
        
        commands = [
            (f"httpx -l {subs_file} -title -status-code -tech-detect -silent -o {httpx_dir}/live_subs.txt", "httpx_live"),
            (f"httpx -l {subs_file} -title -status-code -tech-detect -json -silent -o {httpx_dir}/httpx_results.json", "httpx_json")
        ]
        
        for cmd, tool_name in commands:
            success, output = self.run_tool_with_progress(cmd, tool_name, show_cmd=False)
            if success:
                print(f"   {Fore.GREEN}[✓]{Style.RESET_ALL} {tool_name}")
            else:
                print(f"   {Fore.YELLOW}[!]{Style.RESET_ALL} {tool_name}")
    
    def categorize_status_codes(self):
        print(f"\n{Fore.BLUE}[*]{Style.RESET_ALL} Categorizing by status codes...")
        
        httpx_file = os.path.join(self.recon_dir, "httpx", "httpx_results.json")
        status_dir = os.path.join(self.recon_dir, "status_codes")
        
        if not os.path.exists(httpx_file):
            print(f"   {Fore.YELLOW}[!]{Style.RESET_ALL} No httpx results")
            return
        
        status_codes = {}
        
        with open(httpx_file, 'r') as f:
            for line in f:
                if line.strip():
                    try:
                        data = json.loads(line.strip())
                        url = data.get('url', '')
                        status = str(data.get('status_code', ''))
                        
                        if status not in status_codes:
                            status_codes[status] = []
                        status_codes[status].append(url)
                    except:
                        continue
        
        created_files = []
        for code, urls in status_codes.items():
            if urls:
                file_name = f"sc{code}.txt"
                file_path = os.path.join(status_dir, file_name)
                with open(file_path, 'w') as f:
                    f.write('\n'.join(urls))
                created_files.append((file_name, len(urls)))
        
        interesting_codes = [code for code in status_codes.keys() if code not in ["200", "301", "302", "401", "403", "404"]]
        interesting_urls = []
        for code in interesting_codes:
            interesting_urls.extend([f"{url} [{code}]" for url in status_codes[code]])
        
        if interesting_urls:
            with open(os.path.join(status_dir, "interesting.txt"), 'w') as f:
                f.write('\n'.join(interesting_urls))
            created_files.append(("interesting.txt", len(interesting_urls)))
        
        for file_name, count in created_files:
            print(f"   {Fore.GREEN}[✓]{Style.RESET_ALL} {file_name}: {count}")
    
    def run_cors_analysis(self):
        print(f"\n{Fore.BLUE}[*]{Style.RESET_ALL} Checking CORS misconfigurations...")
        
        httpx_file = os.path.join(self.recon_dir, "httpx", "httpx_results.json")
        cors_dir = os.path.join(self.recon_dir, "Cors_Misconfiguration")
        
        if not os.path.exists(httpx_file):
            print(f"   {Fore.YELLOW}[!]{Style.RESET_ALL} No httpx results")
            return
        
        corsy_path = os.path.join(self.tools_dir, "Corsy", "corsy.py")
        if not os.path.exists(corsy_path):
            print(f"   {Fore.YELLOW}[!]{Style.RESET_ALL} Corsy not found")
            return
        
        urls_file = f"{cors_dir}/urls_for_cors.txt"
        urls = []
        
        with open(httpx_file, 'r') as f:
            for line in f:
                if line.strip():
                    try:
                        data = json.loads(line.strip())
                        url = data.get('url', '')
                        if url:
                            urls.append(url)
                    except:
                        continue
        
        if not urls:
            print(f"   {Fore.YELLOW}[!]{Style.RESET_ALL} No URLs for CORS check")
            return
        
        with open(urls_file, 'w') as f:
            f.write('\n'.join(urls))
        
        cors_cmd = f"python3 {corsy_path} -i {urls_file} -o {cors_dir}/Cors_Results.txt"
        success, output = self.run_tool_with_progress(cors_cmd, "corsy", show_cmd=False)
        
        if success:
            if os.path.exists(f"{cors_dir}/Cors_Results.txt"):
                with open(f"{cors_dir}/Cors_Results.txt", 'r') as f:
                    content = f.read().strip()
                    if content:
                        print(f"   {Fore.GREEN}[✓]{Style.RESET_ALL} CORS analysis completed")
                    else:
                        print(f"   {Fore.CYAN}[✓]{Style.RESET_ALL} No CORS misconfigurations")
    
    def collect_urls(self):
        print(f"\n{Fore.BLUE}[*]{Style.RESET_ALL} Discovering URLs...")
        
        status_dir = os.path.join(self.recon_dir, "status_codes")
        links_dir = os.path.join(self.recon_dir, "links_urls")
        
        status_files = []
        for code in ["200", "401", "403"]:
            file_path = os.path.join(status_dir, f"sc{code}.txt")
            if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
                status_files.append(file_path)
        
        if not status_files:
            print(f"   {Fore.YELLOW}[!]{Style.RESET_ALL} No URLs to process")
            return
        
        temp_urls_file = f"{links_dir}/temp_urls.txt"
        all_urls = set()
        
        with open(temp_urls_file, 'w') as outfile:
            for file_path in status_files:
                with open(file_path, 'r') as infile:
                    content = infile.read()
                    outfile.write(content)
                    all_urls.update([line.strip() for line in content.split('\n') if line.strip()])
        
        if not all_urls:
            os.remove(temp_urls_file)
            print(f"   {Fore.YELLOW}[!]{Style.RESET_ALL} No valid URLs")
            return
        
        tools = [
            (f"katana -list {temp_urls_file} -jc -silent > {links_dir}/katana.txt", "katana"),
            (f"cat {temp_urls_file} | gau --threads 50 --subs > {links_dir}/gau.txt", "gau"),
            (f"cat {temp_urls_file} | waybackurls > {links_dir}/waybackurls.txt", "waybackurls"),
            (f"cat {temp_urls_file} | hakrawler -subs -depth 2 -plain > {links_dir}/hakrawler.txt", "hakrawler")
        ]
        
        discovered_urls = set()
        
        for cmd, tool_name in tools:
            success, output = self.run_tool_with_progress(cmd, tool_name, show_cmd=False)
            if success:
                output_file = f"{links_dir}/{tool_name}.txt"
                if os.path.exists(output_file):
                    with open(output_file, 'r') as f:
                        lines = [line.strip() for line in f if line.strip()]
                    discovered_urls.update(lines)
                print(f"   {Fore.GREEN}[✓]{Style.RESET_ALL} {tool_name}")
        
        all_discovered_file = f"{links_dir}/all_urls.txt"
        with open(all_discovered_file, 'w') as f:
            f.write('\n'.join(sorted(discovered_urls)))
        
        for file in ["temp_urls.txt", "katana.txt", "gau.txt", "waybackurls.txt", "hakrawler.txt"]:
            file_path = os.path.join(links_dir, file)
            if os.path.exists(file_path):
                os.remove(file_path)
        
        print(f"   {Fore.GREEN}[✓]{Style.RESET_ALL} Total URLs: {len(discovered_urls)}")
    
    def analyze_js(self):
        print(f"\n{Fore.BLUE}[*]{Style.RESET_ALL} Analyzing JavaScript files...")
        
        links_dir = os.path.join(self.recon_dir, "links_urls")
        js_dir = os.path.join(self.recon_dir, "js_analyst")
        
        urls_file = os.path.join(links_dir, "all_urls.txt")
        
        if not os.path.exists(urls_file):
            print(f"   {Fore.YELLOW}[!]{Style.RESET_ALL} No URLs file found")
            return
        
        js_files = []
        with open(urls_file, 'r') as f:
            for line in f:
                url = line.strip()
                if '.js' in url.lower():
                    js_files.append(url)
        
        if not js_files:
            print(f"   {Fore.CYAN}[✓]{Style.RESET_ALL} No JavaScript files found")
            return
        
        js_files_path = os.path.join(js_dir, "js_files.txt")
        with open(js_files_path, 'w') as f:
            f.write('\n'.join(js_files))
        
        print(f"   {Fore.GREEN}[✓]{Style.RESET_ALL} JS files: {len(js_files)}")
        
        tools = [
            (f"cat {js_files_path} | mantra -silent > {js_dir}/mantra_results.txt", "mantra")
        ]
        
        linkfinder_path = os.path.expanduser("~/Larhen_Tools/LinkFinder/linkfinder.py")
        if os.path.exists(linkfinder_path):
            tools.append((f"cat {js_files_path} | xargs -I % python3 {linkfinder_path} -i % -o cli 2>/dev/null > {js_dir}/linkfinder_results.txt", 
                         "linkfinder"))
        
        secretfinder_path = os.path.expanduser("~/Larhen_Tools/SecretFinder/secretfinder.py")
        if os.path.exists(secretfinder_path):
            tools.append((f"cat {js_files_path} | xargs -I % python3 {secretfinder_path} -i % -o cli 2>/dev/null > {js_dir}/secretfinder_results.txt", 
                         "secretfinder"))
        
        for cmd, tool_name in tools:
            success, output = self.run_tool_with_progress(cmd, tool_name, show_cmd=False)
            if success:
                print(f"   {Fore.GREEN}[✓]{Style.RESET_ALL} {tool_name}")
    
    def extract_api_urls(self):
        print(f"\n{Fore.BLUE}[*]{Style.RESET_ALL} Extracting API URLs...")
        
        httpx_file = os.path.join(self.recon_dir, "httpx", "httpx_results.json")
        api_dir = os.path.join(self.recon_dir, "API_Endpoints")
        
        if not os.path.exists(httpx_file):
            print(f"   {Fore.YELLOW}[!]{Style.RESET_ALL} No httpx results")
            return []
        
        api_keywords = ["api", "v1", "v2", "v3", "rest", "graphql", "json", "xml", "soap", "endpoint", "swagger", "openapi"]
        
        api_urls = set()
        
        with open(httpx_file, 'r') as f:
            for line in f:
                if line.strip():
                    try:
                        data = json.loads(line.strip())
                        url = data.get('url', '')
                        if url:
                            url_lower = url.lower()
                            for keyword in api_keywords:
                                if keyword in url_lower:
                                    if ':' in url and '[' not in url and url.count(':') > 1:
                                        continue
                                    api_urls.add(url)
                                    break
                    except:
                        continue
        
        try:
            jq_cmd = f"jq -r '.url' {httpx_file} 2>/dev/null"
            result = subprocess.run(jq_cmd, shell=True, capture_output=True, text=True)
            if result.returncode == 0:
                urls_from_jq = [url.strip() for url in result.stdout.split('\n') if url.strip()]
                for url in urls_from_jq:
                    url_lower = url.lower()
                    for keyword in api_keywords:
                        if keyword in url_lower:
                            if ':' in url and '[' not in url and url.count(':') > 1:
                                continue
                            api_urls.add(url)
                            break
        except:
            pass
        
        if api_urls:
            api_urls_file = os.path.join(api_dir, "api_urls.txt")
            with open(api_urls_file, 'w') as f:
                f.write('\n'.join(sorted(api_urls)))
            
            print(f"   {Fore.GREEN}[✓]{Style.RESET_ALL} API URLs found: {len(api_urls)}")
            
            print(f"   {Fore.CYAN}[*]{Style.RESET_ALL} Sample API URLs:")
            for i, url in enumerate(list(api_urls)[:5]):
                print(f"   {Fore.CYAN}    {i+1}. {url}{Style.RESET_ALL}")
            if len(api_urls) > 5:
                print(f"   {Fore.CYAN}    ... and {len(api_urls)-5} more{Style.RESET_ALL}")
            
            return list(api_urls)
        else:
            print(f"   {Fore.CYAN}[✓]{Style.RESET_ALL} No API URLs found")
            return []
    
    def run_arjun(self, api_urls):
        print(f"\n{Fore.BLUE}[*]{Style.RESET_ALL} Running Arjun for parameter discovery...")
        
        api_dir = os.path.join(self.recon_dir, "API_Endpoints")
        
        if not api_urls:
            print(f"   {Fore.YELLOW}[!]{Style.RESET_ALL} No API URLs for Arjun")
            return
        
        cleaned_urls = []
        for url in api_urls:
            try:
                from urllib.parse import urlparse
                parsed = urlparse(url)
                if parsed.netloc and ':' in parsed.netloc and '[' not in parsed.netloc:
                    continue
                if parsed.scheme in ('http', 'https') and parsed.netloc:
                    cleaned_urls.append(url)
            except:
                continue
        
        if not cleaned_urls:
            print(f"   {Fore.YELLOW}[!]{Style.RESET_ALL} No valid URLs after cleaning")
            return
        
        urls_to_scan = cleaned_urls[:10]
        
        arjun_input_file = os.path.join(api_dir, "arjun_input.txt")
        with open(arjun_input_file, 'w') as f:
            f.write('\n'.join(urls_to_scan))
        
        print(f"   {Fore.CYAN}[*]{Style.RESET_ALL} URLs for Arjun scan: {len(urls_to_scan)}")
        
        arjun_cmd = f"arjun -i {arjun_input_file} -oT {api_dir}/arjun_results.txt"
        
        print(f"\n{Fore.YELLOW}╔══════════════════[Arjun]══════════════════╗{Style.RESET_ALL}")
        print(f"{Fore.WHITE}{arjun_cmd}{Style.RESET_ALL}")
        
        success, output = self.run_tool_with_progress(arjun_cmd, "arjun", show_cmd=False)
        
        if success:
            results_file = os.path.join(api_dir, "arjun_results.txt")
            if os.path.exists(results_file) and os.path.getsize(results_file) > 0:
                with open(results_file, 'r') as f:
                    lines = f.readlines()
                    if lines:
                        print(f"   {Fore.GREEN}[✓]{Style.RESET_ALL} Arjun found parameters: {len(lines)} parameters")
                        
                        print(f"   {Fore.CYAN}[*]{Style.RESET_ALL} Sample parameters found:")
                        for i, line in enumerate(lines[:5]):
                            line = line.strip()
                            if line:
                                print(f"   {Fore.CYAN}    {i+1}. {line}{Style.RESET_ALL}")
                        if len(lines) > 5:
                            print(f"   {Fore.CYAN}    ... and {len(lines)-5} more{Style.RESET_ALL}")
                    else:
                        print(f"   {Fore.CYAN}[✓]{Style.RESET_ALL} No parameters found by Arjun")
            else:
                print(f"   {Fore.CYAN}[✓]{Style.RESET_ALL} No results from Arjun")
        else:
            print(f"   {Fore.YELLOW}[!]{Style.RESET_ALL} Arjun execution had issues")
            if output:
                error_lines = output.split('\n')
                for line in error_lines[:3]:
                    if line.strip():
                        print(f"   {Fore.RED}    {line}{Style.RESET_ALL}")
    
    def run_kiterunner(self):
        print(f"\n{Fore.BLUE}[*]{Style.RESET_ALL} Running Kiterunner for API endpoint discovery...")
        
        api_dir = os.path.join(self.recon_dir, "API_Endpoints")
        
        wordlists = [
            ("routes-large.kite", "routes"),
            ("routes-small.kite", "swagger")
        ]
        
        live_subs_file = os.path.join(self.recon_dir, "httpx", "live_subs.txt")
        
        if not os.path.exists(live_subs_file):
            print(f"   {Fore.YELLOW}[!]{Style.RESET_ALL} No live subdomains file")
            return
        
        domains = set()
        with open(live_subs_file, 'r') as f:
            for line in f:
                url = line.strip()
                if url:
                    try:
                        from urllib.parse import urlparse
                        parsed = urlparse(url)
                        if parsed.netloc:
                            domain = parsed.netloc
                            if ':' in domain and '[' not in domain:
                                continue
                            if '.' in domain and not domain.startswith(('.', '-', '_')):
                                domain = domain.split(':')[0]
                                domains.add(domain)
                    except Exception:
                        continue
        
        if not domains:
            print(f"   {Fore.YELLOW}[!]{Style.RESET_ALL} No valid domains found")
            return
        
        domains_file = os.path.join(api_dir, "kiterunner_domains.txt")
        with open(domains_file, 'w') as f:
            f.write('\n'.join(sorted(domains)))
        
        print(f"   {Fore.CYAN}[*]{Style.RESET_ALL} Valid domains for Kiterunner: {len(domains)}")
        
        if len(domains) <= 10:
            for domain in sorted(domains):
                print(f"   {Fore.CYAN}  - {domain}{Style.RESET_ALL}")
        
        for wordlist_name, wordlist_type in wordlists:
            wordlist_path = None
            
            if os.path.exists(wordlist_name):
                wordlist_path = wordlist_name
            elif os.path.exists(os.path.join(self.user_home, "Larhen_Tools", "wordlists", wordlist_name)):
                wordlist_path = os.path.join(self.user_home, "Larhen_Tools", "wordlists", wordlist_name)
            elif os.path.exists(os.path.expanduser(f"~/{wordlist_name}")):
                wordlist_path = os.path.expanduser(f"~/{wordlist_name}")
            
            if wordlist_path and os.path.exists(wordlist_path):
                wordlist_size = os.path.getsize(wordlist_path)
                if wordlist_size == 0:
                    print(f"   {Fore.YELLOW}[!]{Style.RESET_ALL} {wordlist_type} wordlist is empty: {wordlist_path}")
                    continue
                
                print(f"\n   {Fore.CYAN}[*]{Style.RESET_ALL} Using {wordlist_type} wordlist: {wordlist_path}")
                print(f"   {Fore.CYAN}[*]{Style.RESET_ALL} Wordlist size: {wordlist_size:,} bytes")
                
                kr_output_file = os.path.join(api_dir, f"kiterunner_{wordlist_type}_results.txt")
                
                kr_cmd = f"kr scan {domains_file} -w {wordlist_path} -x 10 -j 50 -o {kr_output_file}"
                
                print(f"\n{Fore.YELLOW}╔══════════════════[kiterunner-{wordlist_type}]══════════════════╗{Style.RESET_ALL}")
                print(f"{Fore.WHITE}{kr_cmd}{Style.RESET_ALL}")
                
                success, output = self.run_tool_with_progress(kr_cmd, f"kiterunner-{wordlist_type}", show_cmd=False)
                
                if success:
                    if os.path.exists(kr_output_file) and os.path.getsize(kr_output_file) > 0:
                        with open(kr_output_file, 'r') as f:
                            lines = f.readlines()
                            result_count = len(lines)
                        print(f"   {Fore.GREEN}[✓]{Style.RESET_ALL} {wordlist_type.capitalize()} scan completed: {result_count} results")
                        
                        if result_count > 0:
                            print(f"   {Fore.CYAN}[*]{Style.RESET_ALL} Sample results:")
                            for i, line in enumerate(lines[:3]):
                                print(f"   {Fore.CYAN}    {i+1}. {line.strip()}{Style.RESET_ALL}")
                            if result_count > 3:
                                print(f"   {Fore.CYAN}    ... and {result_count-3} more{Style.RESET_ALL}")
                    else:
                        print(f"   {Fore.CYAN}[✓]{Style.RESET_ALL} {wordlist_type.capitalize()} scan completed - no results found")
                else:
                    print(f"   {Fore.YELLOW}[!]{Style.RESET_ALL} Kiterunner {wordlist_type} scan had issues")
                    if output:
                        error_lines = output.split('\n')
                        for line in error_lines[:5]:
                            if line.strip():
                                print(f"   {Fore.RED}    {line}{Style.RESET_ALL}")
            else:
                print(f"   {Fore.YELLOW}[!]{Style.RESET_ALL} {wordlist_type} wordlist not found: {wordlist_name}")
                print(f"   {Fore.YELLOW}[!]{Style.RESET_ALL} Please ensure wordlists are installed in ~/Larhen_Tools/wordlists/")
    
    def run_api_enumeration(self):
        print(f"\n{Fore.BLUE}[*]{Style.RESET_ALL} Starting API endpoint enumeration...")
        
        api_urls = self.extract_api_urls()
        
        if api_urls:
            self.run_arjun(api_urls)
            self.run_kiterunner()
            print(f"\n{Fore.GREEN}[✓]{Style.RESET_ALL} API enumeration completed")
        else:
            print(f"   {Fore.CYAN}[✓]{Style.RESET_ALL} No API URLs to enumerate")
    
    def show_summary(self):
        print(f"\n{Fore.GREEN}╔══════════════════════════════════════════════╗")
        print(f"║              RECON COMPLETED               ║")
        print(f"╚══════════════════════════════════════════════╝{Style.RESET_ALL}")
        
        print(f"\n{Fore.CYAN}[*]{Style.RESET_ALL} Results Directory: {self.recon_dir}")
        
        print(f"\n{Fore.CYAN}[*]{Style.RESET_ALL} Contents:")
        for root, dirs, files in os.walk(self.recon_dir):
            level = root.replace(self.recon_dir, '').count(os.sep)
            if level == 0:
                for dir_name in sorted(dirs):
                    dir_path = os.path.join(root, dir_name)
                    file_count = len([f for f in os.listdir(dir_path) if os.path.isfile(os.path.join(dir_path, f))])
                    if file_count > 0:
                        print(f"  {Fore.YELLOW}›{Style.RESET_ALL} {dir_name}/ ({file_count} files)")
        
        print(f"\n{Fore.GREEN}[✓]{Style.RESET_ALL} Reconnaissance completed!")
    
    def run(self):
        try:
            self.clear_screen()
            self.print_banner()
            self.get_target()
            self.create_dirs()
            self.collect_subdomains()
            self.run_httpx()
            self.categorize_status_codes()
            self.run_cors_analysis()
            self.collect_urls()
            self.analyze_js()
            self.run_api_enumeration()
            self.show_summary()
            
        except KeyboardInterrupt:
            print(f"\n\n{Fore.YELLOW}[!]{Style.RESET_ALL} Process interrupted by user")
            sys.exit(0)
        except Exception as e:
            print(f"\n{Fore.RED}[✗]{Style.RESET_ALL} Error: {str(e)}")
            sys.exit(1)

if __name__ == "__main__":
    tool = Larhenum()
    tool.run()
