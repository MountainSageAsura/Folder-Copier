"""
Network Checker - Enhanced Folder Copier
Utilities for checking network connectivity
"""

import subprocess
import platform
import socket
import logging
from typing import Optional


class NetworkChecker:
    """Network connectivity checker with multiple methods"""

    def __init__(self, timeout: int = 3):
        self.timeout = timeout

    def ping_host(self, host: str) -> bool:
        """
        Ping a host to check connectivity

        Args:
            host: IP address or hostname to ping

        Returns:
            bool: True if host is reachable, False otherwise
        """
        try:
            # Determine ping command based on OS
            if platform.system().lower() == "windows":
                cmd = ["ping", "-n", "1", "-w", str(self.timeout * 1000), host]
            else:
                cmd = ["ping", "-c", "1", "-W", str(self.timeout), host]

            # Execute ping command
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=self.timeout + 2
            )

            success = result.returncode == 0

            if success:
                logging.info(f"Successfully pinged {host}")
            else:
                logging.warning(f"Failed to ping {host}")

            return success

        except subprocess.TimeoutExpired:
            logging.warning(f"Ping timeout for {host}")
            return False
        except FileNotFoundError:
            logging.error("Ping command not found")
            return False
        except Exception as e:
            logging.error(f"Error pinging {host}: {str(e)}")
            return False

    def check_port(self, host: str, port: int) -> bool:
        """
        Check if a specific port is open on a host

        Args:
            host: IP address or hostname
            port: Port number to check

        Returns:
            bool: True if port is open, False otherwise
        """
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.settimeout(self.timeout)
                result = sock.connect_ex((host, port))

                if result == 0:
                    logging.info(f"Port {port} is open on {host}")
                    return True
                else:
                    logging.warning(f"Port {port} is closed on {host}")
                    return False

        except socket.gaierror as e:
            logging.error(f"DNS resolution failed for {host}: {str(e)}")
            return False
        except Exception as e:
            logging.error(f"Error checking port {port} on {host}: {str(e)}")
            return False

    def check_smb_share(self, host: str) -> bool:
        """
        Check if SMB/CIFS shares are available

        Args:
            host: IP address or hostname

        Returns:
            bool: True if SMB is available, False otherwise
        """
        # Check common SMB ports
        smb_ports = [445, 139]  # SMB over TCP, NetBIOS

        for port in smb_ports:
            if self.check_port(host, port):
                logging.info(f"SMB service detected on {host}:{port}")
                return True

        logging.warning(f"No SMB service detected on {host}")
        return False

    def resolve_hostname(self, hostname: str) -> Optional[str]:
        """
        Resolve hostname to IP address

        Args:
            hostname: Hostname to resolve

        Returns:
            str: IP address if successful, None otherwise
        """
        try:
            ip_address = socket.gethostbyname(hostname)
            logging.info(f"Resolved {hostname} to {ip_address}")
            return ip_address
        except socket.gaierror as e:
            logging.error(f"Failed to resolve {hostname}: {str(e)}")
            return None

    def comprehensive_check(self, host: str) -> dict:
        """
        Perform comprehensive network connectivity check

        Args:
            host: IP address or hostname

        Returns:
            dict: Results of various connectivity tests
        """
        results = {
            'host': host,
            'ping': False,
            'smb_available': False,
            'resolved_ip': None,
            'timestamp': None
        }

        try:
            import datetime
            results['timestamp'] = datetime.datetime.now().isoformat()

            # Try to resolve hostname if not an IP
            if not self._is_ip_address(host):
                results['resolved_ip'] = self.resolve_hostname(host)
                if not results['resolved_ip']:
                    return results

            # Ping test
            results['ping'] = self.ping_host(host)

            # SMB check (for network shares)
            results['smb_available'] = self.check_smb_share(host)

            logging.info(f"Comprehensive check completed for {host}: {results}")

        except Exception as e:
            logging.error(f"Error in comprehensive check for {host}: {str(e)}")

        return results

    def _is_ip_address(self, address: str) -> bool:
        """Check if string is a valid IP address"""
        try:
            socket.inet_aton(address)
            return True
        except socket.error:
            return False

    def get_local_ip(self) -> Optional[str]:
        """Get local machine's IP address"""
        try:
            # Connect to a remote address to determine local IP
            with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
                sock.connect(("8.8.8.8", 80))
                local_ip = sock.getsockname()[0]
                logging.info(f"Local IP address: {local_ip}")
                return local_ip
        except Exception as e:
            logging.error(f"Failed to get local IP: {str(e)}")
            return None