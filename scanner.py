# scanner.py
# Responsible for scanning the local network and detecting connected devices

from scapy.all import ARP, Ether, srp


def scan(ip_range):
    try:
        arp = ARP(pdst=ip_range)
        ether = Ether(dst="ff:ff:ff:ff:ff:ff")
        packet = ether / arp

        result = srp(packet, timeout=3, verbose=0)[0]

        devices = []
        for sent, received in result:
            devices.append({
                "ip": received.psrc,
                "mac": received.hwsrc
            })

        return devices

    except PermissionError:
        return []

    except Exception:
        return []