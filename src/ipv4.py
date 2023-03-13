from network_infrastructure import network_names, network_range

# Function that removes "." of the IPs and returns them.
def convert_ipv4(ip):
    return tuple(int(n) for n in ip.split('.'))

# Function that compares the IP with the Network range.
def check_ipv4_in(addr, start, end):
    return convert_ipv4(start) <= convert_ipv4(addr) <= convert_ipv4(end)

# Function that compares the IPs from the .csv file and sees in which network it belongs to. It returns a dictionary containing that information.
def ListThem(ip, rede):
    for z in ip:
        for i in range(0, len(network_names)):
            x = tuple(network_range[network_names[i]])
            if check_ipv4_in(z, *x) == True:
                rede[z] = network_names[i]
                break
            else:
                rede[z] = ""