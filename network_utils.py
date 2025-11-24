import ipaddress

def ip_to_binary(ip_obj):
    """Converts an IPv4 address object to a dotted binary string."""
    # Replicates: IPAddressToBinaryString
    return ".".join(f"{octet:08b}" for octet in ip_obj.packed)

def get_legacy_class(ip_obj):
    """Determines legacy class based on first octet."""
    # Replicates: GetLegacyClass
    first_octet = ip_obj.packed[0]
    
    if 0 <= first_octet <= 127: return "Class A"
    if 128 <= first_octet <= 191: return "Class B"
    if 192 <= first_octet <= 223: return "Class C"
    if 224 <= first_octet <= 239: return "Class D (Multicast)"
    if 240 <= first_octet <= 255: return "Class E (Reserved)"
    return "Unknown"

def get_address_type(ip_obj):
    """Determines address type (Private, Loopback, APIPA, etc)."""
    # Replicates: GetIPAddressType
    octets = list(ip_obj.packed)
    
    if ip_obj.is_loopback: return "Loopback"
    
    # Private RFC1918
    if octets[0] == 10: return "Private (RFC1918)"
    if octets[0] == 172 and 16 <= octets[1] <= 31: return "Private (RFC1918)"
    if octets[0] == 192 and octets[1] == 168: return "Private (RFC1918)"
    
    # APIPA
    if octets[0] == 169 and octets[1] == 254: return "APIPA"
    
    # Multicast
    if 224 <= octets[0] <= 239: return "Multicast"
    
    # Reserved
    if octets[0] == 0: return "Reserved (Current Network)"
    if octets[0] >= 240: return "Reserved (Future Use)"
    
    return "Public"

def calculate_subnet(ip_str, cidr_str):
    """
    Main calculation logic.
    Returns a dictionary of results or raises ValueError.
    """
    try:
        cidr = int(cidr_str)
        if not (0 <= cidr <= 32):
            raise ValueError("CIDR must be between 0 and 32")
            
        # Create network object. strict=False allows passing a host IP (e.g. .10)
        # and having the library calculate the network address automatically.
        interface = ipaddress.IPv4Interface(f"{ip_str}/{cidr}")
        network = interface.network
        
        # Basic details
        subnet_mask = network.netmask
        net_address = network.network_address
        broadcast = network.broadcast_address
        
        # Host Logic (Replicating C# logic for /31 and /32)
        total_hosts = network.num_addresses
        usable_hosts = 0
        first_ip = None
        last_ip = None
        
        if cidr == 32:
            first_ip = interface.ip
            last_ip = interface.ip
            usable_hosts = 1 # C# logic says 1
            broadcast = interface.ip # Broadcast is same as IP for /32
        elif cidr == 31:
            first_ip = network.network_address
            last_ip = network.broadcast_address
            usable_hosts = 2 # Both usable for p2p
        else:
            first_ip = network.network_address + 1
            last_ip = network.broadcast_address - 1
            usable_hosts = total_hosts - 2

        return {
            "success": True,
            "data": {
                "ip": str(interface.ip),
                "cidr": cidr,
                "subnet_mask": str(subnet_mask),
                "network_address": str(net_address),
                "broadcast_address": str(broadcast),
                "first_ip": str(first_ip),
                "last_ip": str(last_ip),
                "total_hosts": f"{total_hosts:,}",
                "usable_hosts": f"{usable_hosts:,}",
                "type": get_address_type(interface.ip),
                "class": get_legacy_class(interface.ip),
                # Binary Data
                "bin_ip": ip_to_binary(interface.ip),
                "bin_mask": ip_to_binary(subnet_mask),
                "bin_net": ip_to_binary(net_address),
                "bin_bc": ip_to_binary(broadcast)
            }
        }
        
    except ValueError as e:
        return {"success": False, "error": str(e)}
    except Exception as e:
        return {"success": False, "error": "Invalid IPv4 Address format."}