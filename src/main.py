# -*- coding: utf-8 -*-

import socket, fire, pyfiglet, sys
from loguru import logger
from nmap import PortScanner
from typing import List
from datetime import datetime


class BColors:
    OKCYAN = "\033[96m"
    WARNING = "\033[93m"

class Mode:
    SIMPLE = "simple"
    LOOP = "loop"
    NMAP = "nmap"

def connect_scan(target_host: str, target_port: int) -> None:
    # AF_INET refers to the ipv4 family-address
    # SOCK_STREAM means that the connection is oriented by TCP protocol
    with socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM) as conn:
        try:
            conn.connect((target_host, target_port))
            logger.info(f"👻 Port {target_port} Opened")
        except:
            logger.warning(f"🥶 Port {target_port} Closed")
        finally:
            logger.debug("💥 Closing connection")
            conn.close()


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

def port_scan_loop(target_host: str) -> None:
    logger.debug("✨ Enable port scan loop mode")
    for port in range(1,52000):
        logger.debug(f"🔎 Scanning port: {port}")
        connect_scan(target_host, int(port))

def port_scan(
    target_host: str = "google.com",
    target_ports: List[int] = [443, 80],
    mode: str = "simple"
) -> None:

    print(BColors.OKCYAN + f"✨ Target host: {target_host}")
    print(BColors.OKCYAN + f"✨ Target ports: {target_ports}")
    print(BColors.OKCYAN + f"✨ Target mode: {mode}", end="\n\n")

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

    start = datetime.now()

    if mode == Mode.SIMPLE:
        port_scan_simple(target_host, target_ports)

    if mode == Mode.LOOP:
        port_scan_loop(target_host)

    if mode == Mode.NMAP:
        nmap_scan(target_host, target_ports)

    end = datetime.now()
    print(f"\nScanning completed in: {end - start}\n")


def main() -> None:
    ascii_banner = pyfiglet.figlet_format("Port Scanner")
    print(BColors.OKCYAN + ascii_banner)
    print(BColors.WARNING + "                   by @CI Monk")
    print(BColors.WARNING + "		      @lpmatos \n")
    fire.Fire(port_scan)


if __name__ == "__main__":
    main()
