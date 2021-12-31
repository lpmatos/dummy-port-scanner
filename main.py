import socket
import fire
from loguru import logger
from nmap import PortScanner
from typing import List

HEADER = """'
____   ___  ____ _____   ____   ____    _    _   _ _   _ _____ ____
|  _ \ / _ \|  _ \_   _| / ___| / ___|  / \  | \ | | \ | | ____|  _ \
| |_) | | | | |_) || |   \___ \| |     / _ \ |  \| |  \| |  _| | |_) |
|  __/| |_| |  _ < | |    ___) | |___ / ___ \| |\  | |\  | |___|  _ <
|_|    \___/|_| \_\|_|   |____/ \____/_/   \_\_| \_|_| \_|_____|_| \_\

"""


def connect_scan(target_host: str, target_port: int) -> None:
    try:
        conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        conn.connect((target_host, target_port))
        logger.info(f"👻 Port {target_port} Opened")
        conn.close()
    except:
        logger.warning(f"🥶 Port {target_port} Closed")


def port_scan_simple(target_host: str, target_ports: List[int] = [443, 80]) -> None:
    logger.debug("✨ Enable port scan simple mode")
    for port in target_ports:
        logger.debug(f"🔎 Scanning port: {port}")
        connect_scan(target_host, int(port))


def nmap_scan(target_host: str, target_ports: List[int] = [443, 80]) -> None:
    logger.debug("✨ Enable port scan nmap mode")
    scan = PortScanner()
    for port in target_ports:
        print(f"Scanning port: {port}")
        portscan = scan.scan(target_host, str(port))
        print("Port", port, "is ", portscan["scan"][target_host]["tcp"][port]["state"])


def port_scan(
    target_host: str, target_ports: List[int] = [443, 80], mode: str = "simple"
) -> None:
    try:
        target_ip = socket.gethostbyname(target_host)
    except:
        print(f"🤬 Cannot resolve {target_host}")
        return

    try:
        target_name = socket.gethostbyaddr(target_ip)
        logger.debug(f"👾 Scan result of {target_name[0]}")
    except:
        logger.debug(f"👾 Scan result of {target_ip}")

    socket.setdefaulttimeout(1)

    if mode == "simple":
        port_scan_simple(target_host, target_ports)

    if mode == "nmap":
        nmap_scan(target_host, target_ports)


def main() -> None:
    print(HEADER)
    fire.Fire(port_scan)


if __name__ == "__main__":
    main()
