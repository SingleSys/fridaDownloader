#!/usr/bin/python3
# Author: Mateo Fumis (hackermater) - linkedin.com/in/mateo-gabriel-fumis
import os
import requests
import argparse
import subprocess

BRIGHT_RED = "\033[1;91m"
BRIGHT_GREEN = "\033[1;92m"
BRIGHT_YELLOW = "\033[1;93m"
BRIGHT_CYAN = "\033[1;96m"
RESET = "\033[0m"

BANNER = '''
*********************************************
*  Welcome to the Frida Downloader          *
*                           by hackermater  *
*********************************************
'''

def print_banner():
    print(f"{BRIGHT_CYAN}{BANNER}{RESET}")

def get_latest_version():
    url = "https://api.github.com/repos/frida/frida/releases/latest"
    try:
        response = requests.get(url)
        response.raise_for_status()
        release_data = response.json()
        return release_data['tag_name']
    except requests.RequestException as e:
        print(f"{BRIGHT_RED}[-] Error fetching the latest version: {e}{RESET}")
        return None

def url_exists(url):
    try:
        response = requests.head(url, allow_redirects=True)
        return response.status_code == 200
    except requests.RequestException:
        return False

def download_file(target, architecture, version, output_dir):
    base_url = f"https://github.com/frida/frida/releases/download/{version}/"
    file_extension = ".so.xz" if target == "gadget" else ".xz"
    frida_url = f"{base_url}frida-{target}-{version}-android-{architecture}{file_extension}"
    output_file = os.path.join(output_dir, f"frida-{target}-{version}-android-{architecture}{file_extension}")

    os.makedirs(output_dir, exist_ok=True)

    if not url_exists(frida_url):
        print(f"{BRIGHT_RED}[-] URL for {architecture} not found: {frida_url}{RESET}")
        print(f"{BRIGHT_RED}[-] Attempting to download another architecture...{RESET}")
        architecture = "x86_64"
        frida_url = f"{base_url}frida-{target}-{version}-android-{architecture}{file_extension}"
        output_file = os.path.join(output_dir, f"frida-{target}-{version}-android-{architecture}{file_extension}")

        if not url_exists(frida_url):
            print(f"{BRIGHT_RED}[-] Fallback URL for {architecture} not found either: {frida_url}{RESET}")
            return

    print(f"{BRIGHT_YELLOW}[*] Downloading Frida {target.capitalize()} for Android Architecture {architecture} from {frida_url}{RESET}")

    try:
        response = requests.get(frida_url, stream=True)
        response.raise_for_status()

        with open(output_file, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        
        print(f"{BRIGHT_GREEN}[+] Download completed successfully: {output_file}{RESET}")

        subprocess.run(["xz", "-d", output_file], check=True)
        print(f"{BRIGHT_GREEN}[+] Decompression completed: {output_file[:-3]}{RESET}")
    
    except requests.RequestException as e:
        print(f"{BRIGHT_RED}[-] Download failed: {e}{RESET}")
    except subprocess.CalledProcessError as e:
        print(f"{BRIGHT_RED}[-] Decompression failed: {e}{RESET}")

def main():
    print_banner()

    parser = argparse.ArgumentParser(description="Download Frida Gadget or Server for Android")
    
    parser.add_argument('-v', '--version', type=str, help="Download a specific version of Frida")
    parser.add_argument('-t', '--target', type=str, choices=['gadget', 'server'], required=True, help="Specify the target to download: gadget or server")
    parser.add_argument('-a', '--architecture', type=str, default='arm', help="Android architecture (default: arm). Options: arm, arm64, x86, x86_64")
    parser.add_argument('-o', '--output', type=str, default=os.path.expanduser('~') + '/Downloads', help="Directory to save the downloaded file (default: ~/Downloads)")

    args = parser.parse_args()

    if args.version:
        download_file(args.target, args.architecture, args.version, args.output)
    else:
        print(f"{BRIGHT_YELLOW}[*] Fetching the latest version of Frida...{RESET}")
        latest_version = get_latest_version()
        if latest_version:
            download_file(args.target, args.architecture, latest_version, args.output)

if __name__ == "__main__":
    main()
