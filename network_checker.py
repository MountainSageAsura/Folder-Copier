"""
Network Connectivity Checker for Enhanced Folder Copier
"""

import subprocess
import platform
import socket
import logging
from typing import bool


class NetworkChecker:
    """Utility class for checking network connectivity"""

    def __init__(self):
        self.system = platform.system().lower()

    def ping_host(self, host: str, timeout: int = 3) -> bool:
        """
        Ping a host to check connectivity

        Args:
            host: IP address or hostname to ping
            timeout: Timeout in seconds

        Returns:
            True if host is reachable, False otherwise
        """
        try:
            # Determine ping command based on OS
            if self.system == "windows":
                # Windows ping command
                cmd = ["ping", "-n", "1", "-w", str(timeout * 1000), host]
            else:
                # Unix/Linux/macOS ping command
                cmd = ["ping", "-c", "1", "-W", str(timeout), host]

            # Execute ping command
            result = subprocess.run(
                cmd,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                timeout=timeout + 2  # Add buffer to subprocess timeout
            )

            # Return True if ping was successful (return code 0)
            is_reachable = result.returncode == 0

            if is_reachable:
                logging.debug(f"Successfully pinged {host}")
            else:
                logging.debug(f"Failed to ping {host}")

            return is_reachable

        except subprocess.TimeoutExpired:
            logging.warning(f"Ping to {host} timed out after {timeout} seconds")
            return False

        except FileNotFoundError:
            # Ping command not found, try alternative method
            logging.warning("Ping command not found, trying socket connection")
            return self.check_tcp_connection(host)

        except Exception as e:
            logging.error(f"Error pinging {host}: {str(e)}")
            return False

    def check_tcp_connection(self, host: str, port: int = 445, timeout: int = 3) -> bool:
        """
        Check TCP connection to a host (useful for SMB/network shares)

        Args:
            host: IP address or hostname
            port: Port to connect to (445 for SMB, 22 for SSH, etc.)
            timeout: Connection timeout in seconds

        Returns:
            True if connection successful, False otherwise
        """
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.settimeout(timeout)
                result = sock.connect_ex((host, port))

                is_connected = result == 0

                if is_connected:
                    logging.debug(f"Successfully connected to {host}:{port}")
                else:
                    logging.debug(f"Failed to connect to {host}:{port}")

                return is_connected

        except socket.gaierror as e:
            logging.error(f"DNS resolution failed for {host}: {str(e)}")
            return False

        except Exception as e:
            logging.error(f"Error connecting to {host}:{port}: {str(e)}")
            return False

    def check_smb_share(self, host: str, timeout: int = 3) -> bool:
        """
        Check if SMB/CIFS share is accessible

        Args:
            host: IP address or hostname of SMB server
            timeout: Connection timeout in seconds

        Returns:
            True if SMB share is accessible, False otherwise
        """
        # Try common SMB ports
        smb_ports = [445, 139]  # Modern SMB (445) and legacy NetBIOS (139)

        for port in smb_ports:
            if self.check_tcp_connection(host, port, timeout):
                logging.debug(f"SMB service detected on {host}:{port}")
                return True

        logging.debug(f"No SMB service detected on {host}")
        return False

    def get_local_ip(self) -> str:
        """
        Get the local IP address of this machine

        Returns:
            Local IP address as string, or '127.0.0.1' if detection fails
        """
        try:
            # Connect to a remote address to determine local IP
            with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
                # Connect to Google's DNS server (doesn't actually send data)
                sock.connect(("8.8.8.8", 80))
                local_ip = sock.getsockname()[0]

            logging.debug(f"Detected local IP: {local_ip}")
            return local_ip

        except Exception as e:
            logging.warning(f"Failed to detect local IP: {str(e)}")
            return "127.0.0.1"

    def is_valid_ip(self, ip_address: str) -> bool:
        """
        Validate if a string is a valid IP address

        Args:
            ip_address: String to validate

        Returns:
            True if valid IP address, False otherwise
        """
        try:
            socket.inet_aton(ip_address)
            return True
        except socket.error:
            return False

    def resolve_hostname(self, hostname: str) -> str:
        """
        Resolve hostname to IP address

        Args:
            hostname: Hostname to resolve

        Returns:
            IP address string, or empty string if resolution fails
        """
        try:
            ip_address = socket.gethostbyname(hostname)
            logging.debug(f"Resolved {hostname} to {ip_address}")
            return ip_address

        except socket.gaierror as e:
            logging.error(f"Failed to resolve {hostname}: {str(e)}")
            return ""

        except Exception as e