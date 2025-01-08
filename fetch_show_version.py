import requests
import sys

def fetch_show_version(router_ip, username, password):
    url = f"https://{router_ip}/restconf/data/Cisco-IOS-XE-native:native/version"
    headers = {
        "Content-Type": "application/yang-data+json",
        "Accept": "application/yang-data+json",
    }
    try:
        response = requests.get(url, auth=(username, password), headers=headers, verify=False)
        if response.status_code == 200:
            print(f"Success: Retrieved 'show version' for {router_ip}")
            print(response.json())
        else:
            print(f"Failed to retrieve 'show version' for {router_ip}: {response.status_code}")
            sys.exit(1)
    except Exception as e:
        print(f"Error connecting to {router_ip}: {e}")
        sys.exit(1)

if __name__ == "__main__":
    # Pass router IP, username, and password as arguments
    if len(sys.argv) != 4:
        print("Usage: python fetch_show_version.py <router_ip> <username> <password>")
        sys.exit(1)

    router_ip = sys.argv[1]
    username = sys.argv[2]
    password = sys.argv[3]
    fetch_show_version(router_ip, username, password)
