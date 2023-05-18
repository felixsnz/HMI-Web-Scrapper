import netifaces

def get_ip_address():
    for interface in netifaces.interfaces():
        try:
            ip = netifaces.ifaddresses(interface)[netifaces.AF_INET][0]['addr']
            if ip != '127.0.0.1':
                return ip
        except KeyError:
            pass
    return None

# Example usage
ip = get_ip_address()
if ip is not None:
    print("IP address:", ip)
else:
    print("No IP address found.")