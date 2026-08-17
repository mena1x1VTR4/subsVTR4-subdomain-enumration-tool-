import requests
import sys
import socket
import argparse
import pyfiglet
from rich import print

# 1. Print banner in ASCII art
print(pyfiglet.figlet_format("subsVTR4"))
print("[red]<Subdomain Enumration Tool>")

# 2. Parse command line arguments using argparse
parser = argparse.ArgumentParser(
    description="Subdomain Enumeration Tool"
)
parser.add_argument(
    "target",
    help="Target domain, e.g. example.com"
)
parser.add_argument(
    "-t", "--timeout",
    type=int,
    default=5,
    help="Request timeout in seconds (default: 5)"
)
parser.add_argument(
    "-w", "--wordlist",
    default="menasubs.txt",
    help="Path to wordlist file (default: menasubs.txt)"
)
args = parser.parse_args()
target = args.target

# 3. Read wordlist file and split into lines
try:
    with open(args.wordlist) as f:
        sub_list = f.read().splitlines()
except FileNotFoundError:
    print(f"[red]Error: wordlist file '{args.wordlist}' not found![/red]")
    sys.exit(1)

total = len(sub_list)

# 4. Loop through each subdomain in the wordlist
for i, sub in enumerate(sub_list, start=1):
    sub_domain = f"https://{sub}.{target}"
    domain_name = f"{sub}.{target}"

    try:
        # Send HTTP GET request with a timeout
        response = requests.get(sub_domain, timeout=args.timeout)
        status_code = response.status_code

        if status_code == 200:
            status = "[green]Active (200)[/green]"
        elif status_code == 404:
            status = "[yellow]Not Found (404)[/yellow]"
        elif status_code == 403:
            status = "[yellow]Forbidden (403)[/yellow]"
        elif status_code >= 500:
            status = f"[red]Server Error ({status_code})[/red]"
        else:
            status = f"[cyan]HTTP {status_code}[/cyan]"

        # Extract Server header if available
        server = response.headers.get("Server", "Unknown")
        ip_address = socket.gethostbyname(domain_name)

    except KeyboardInterrupt:
        # exit if ctrl + c
        print("\n[red]Exiting tool...[/red]")
        sys.exit()

    except requests.exceptions.Timeout:
        status = "[red]Timeout[/red]"
        server = "N/A"
        ip_address = "N/A"

    except requests.exceptions.ConnectionError:
        status = "[red]Connection Error[/red]"
        server = "N/A"
        ip_address = "N/A"

    except requests.exceptions.RequestException:
        status = "[red]Request Error[/red]"
        server = "N/A"
        ip_address = "N/A"

    # 5. Output the structured result
    print(f"[{i}/{total}] Subdomain: {sub_domain} | Server: [yellow]{server}[/yellow] | Status: {status} | ip: {ip_address}")
