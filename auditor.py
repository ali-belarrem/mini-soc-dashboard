# auditor.py
# Responsible for running security checks on the Linux system

import subprocess
import socket
import os


def check_firewall():
    try:
        result = subprocess.run(
            ["ufw", "status"],
            capture_output=True,
            text=True
        )
        if "active" in result.stdout.lower():
            return {"check": "Firewall (UFW)", "status": "PASS", "detail": "Firewall is active"}
        else:
            return {"check": "Firewall (UFW)", "status": "FAIL", "detail": "Firewall is not active"}

    except FileNotFoundError:
        return {"check": "Firewall (UFW)", "status": "WARNING", "detail": "UFW not found on this system"}

    except Exception as e:
        return {"check": "Firewall (UFW)", "status": "ERROR", "detail": str(e)}


def check_open_ports():
    dangerous_ports = {
        21: "FTP",
        23: "Telnet",
        3306: "MySQL",
        5900: "VNC",
        6379: "Redis"
    }

    results = []
    for port, service in dangerous_ports.items():
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            connection = sock.connect_ex(("127.0.0.1", port))

            if connection == 0:
                results.append({"check": f"Port {port} ({service})", "status": "FAIL", "detail": f"Dangerous port {port} is open"})
            else:
                results.append({"check": f"Port {port} ({service})", "status": "PASS", "detail": f"Port {port} is closed"})
            sock.close()

        except Exception as e:
            results.append({"check": f"Port {port} ({service})", "status": "ERROR", "detail": str(e)})

    return results


def run_all_checks():
    """Run every security check and return the combined results."""
    results = []
    results.append(check_firewall())
    results.extend(check_open_ports())
    return results