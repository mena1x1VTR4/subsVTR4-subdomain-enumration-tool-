import requests
import sys
import socket
import pyfiglet
from rich import print


# 1. Print banner in ASCII art
print(pyfiglet.figlet_format("subsVTR4"))
print("[red]<Subdomain Enumration Tool>")


# 2. Read wordlist file and split into lines
sub_list = open("menasubs.txt").read().splitlines()

# 3. Get target domain from command line argument
target = sys.argv[1]

# 4. Loop through each subdomain in the wordlist
for sub in sub_list:
    sub_domain = f"https://{sub}.{target}"
    
    try:
        # Send HTTP GET request with a 3-second timeout
        response = requests.get(sub_domain, timeout=3)
        status = "[green]Active[/green]"
        # Extract Server header if available
        server = response.headers.get("Server", "Unknown")
        
        domain_name = f"{sub}.{target}"
        attack = socket.gethostbyname(domain_name)
        
    except KeyboardInterrupt:
    # exit if ctrl + c
        print("\n[red]Exiting tool...[/red]")
        sys.exit()    
        
        
    except:
        # Executed if the host is unreachable or down
        status = "[red]Inactive[/red]"
        server = "N/A"
        attack = "N/A"

    # 5. Output the structured result
    print(f"Subdomain: {sub_domain} | Server: [yellow]{server}[/yellow] | Status: {status} | ip: {attack}")