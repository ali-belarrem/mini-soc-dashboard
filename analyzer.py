# analyzer.py
# Responsible for analyzing server logs and detecting brute-force attacks

LOG_FILE_PATH = "logs/auth.log"
FAILED_ATTEMPTS_THRESHOLD = 3


def read_log_file(file_path):
    """Read the log file and return a list of all lines."""
    try:
        with open(file_path, "r") as file:
            lines = file.readlines()
        return lines
    except FileNotFoundError:
        return []


def extract_ip_from_line(line):
    """Extract the IP address from a failed login log line, if present."""
    words = line.split()
    if "from" not in words:
        return None
    ip_index = words.index("from") + 1
    return words[ip_index]


def find_failed_attempts(lines):
    """Return a list of IP addresses that had failed login attempts."""
    failed_ips = []
    for line in lines:
        if "Failed password" in line:
            ip = extract_ip_from_line(line)
            if ip is not None:
                failed_ips.append(ip)
    return failed_ips


def count_attempts_per_ip(failed_ips):
    """Count how many times each IP appears in the failed attempts list."""
    ip_counts = {}
    for ip in failed_ips:
        if ip in ip_counts:
            ip_counts[ip] += 1
        else:
            ip_counts[ip] = 1
    return ip_counts


def find_suspicious_ips(ip_counts):
    """Return IPs that failed more times than the allowed threshold."""
    suspicious = {}
    for ip, count in ip_counts.items():
        if count >= FAILED_ATTEMPTS_THRESHOLD:
            suspicious[ip] = count
    return suspicious


def run_analysis():
    """Run the full log analysis pipeline and return suspicious IPs."""
    lines = read_log_file(LOG_FILE_PATH)
    failed_ips = find_failed_attempts(lines)
    ip_counts = count_attempts_per_ip(failed_ips)
    suspicious_ips = find_suspicious_ips(ip_counts)
    return suspicious_ips