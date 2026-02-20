
import sys
import ipaddress
import subprocess
import platform
import re
from datetime import datetime


def ping_host(ip):
    """
    Pings a single host and returns:
    (status, response_time, error_message)
    """

    system = platform.system().lower()

   
    if system == "windows":
        command = ["ping", "-n", "1", "-w", "1000", str(ip)]
    else:
        command = ["ping", "-c", "1", "-W", "1", str(ip)]

    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True
        )

        if result.returncode == 0:
            
            match = re.search(r'time[=<]?\s*(\d+\.?\d*)', result.stdout)
            if match:
                return ("UP", f"{match.group(1)}ms", None)
            else:
                return ("UP", "Unknown", None)
        else:
            return ("DOWN", None, "No response")

    except Exception as e:
        return ("ERROR", None, str(e))


def main():
    if len(sys.argv) != 2:
        print("Usage: python3 ip-freely.py <CIDR>")
        print("Example: python3 ip-freely.py 192.168.1.0/24")
        sys.exit(1)

    cidr_input = sys.argv[1]

    try:
        network = ipaddress.ip_network(cidr_input, strict=False)
    except ValueError as e:
        print(f"Invalid CIDR notation: {e}")
        sys.exit(1)

    print(f"\nScanning network {network}...")
    print("-" * 45)

    up_count = 0
    down_count = 0
    error_count = 0

    start_time = datetime.now()

    
    for ip in network.hosts():
        status, response_time, error = ping_host(ip)

        ip_str = str(ip) 

        if status == "UP":
            print(f"{ip_str:<15} - UP    ({response_time})")
            up_count += 1
        elif status == "DOWN":
            print(f"{ip_str:<15} - DOWN  ({error})")
            down_count += 1
        else:
            print(f"{ip_str:<15} - ERROR ({error})")
            error_count += 1

    end_time = datetime.now()
    duration = (end_time - start_time).total_seconds()

    print("\nScan complete.")
    print(f"Found {up_count} active hosts, {down_count} down, {error_count} error")
    print(f"Scan duration: {duration:.2f} seconds")


if __name__ == "__main__":
    main()
