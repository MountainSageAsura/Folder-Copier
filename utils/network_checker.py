"""
Network Connectivity Checker for Enhanced Folder Copier
"""

import subprocess
import platform
import socket
import logging
import time
import re
from typing import Optional, Dict, Any


class NetworkChecker:
    """Utility class for checking network connectivity"""

    def __init__(self):
        self.system = platform.system().lower()
        self.logger = logging.getLogger(__name__)

    def ping_host(self, host: str, timeout: int = 3, count: int = 1) -> bool:
        """
        Ping a host to check connectivity

        Args:
            host: IP address or hostname to ping
            timeout: Timeout in seconds
            count: Number of ping packets to send

        Returns:
            True if host is reachable, False otherwise
        """
        try:
            # Validate input
            if not host or not host.strip():
                self.logger.warning("Empty host provided for ping")
                return False

            host = host.strip()

            # Determine ping command based on OS
            if self.system == "windows":
                # Windows ping command
                cmd = [
                    "ping",
                    "-n", str(count),  # Number of packets
                    "-w", str(timeout * 1000),  # Timeout in milliseconds
                    host
                ]
            else:
                # Unix/Linux/macOS ping command
                cmd = [
                    "ping",
                    "-c", str(count),  # Number of packets
                    "-W", str(timeout),  # Timeout in seconds
                    host
                ]

            self.logger.debug(f"Executing ping command: {' '.join(cmd)}")

            # Execute ping command
            start_time = time.time()
            result = subprocess.run(
                cmd,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                timeout=timeout + 5,  # Add buffer to subprocess timeout
                creationflags=subprocess.CREATE_NO_WINDOW if self.system == "windows" else 0
            )

            execution_time = time.time() - start_time

            # Return True if ping was successful (return code 0)
            is_reachable = result.returncode == 0

            if is_reachable:
                self.logger.debug(f"Successfully pinged {host} in {execution_time:.2f}s")
            else:
                self.logger.debug(f"Failed to ping {host} (return code: {result.returncode})")

            return is_reachable

        except subprocess.TimeoutExpired:
            self.logger.warning(f"Ping to {host} timed out after {timeout} seconds")
            return False

        except FileNotFoundError:
            # Ping command not found, try alternative method
            self.logger.warning("Ping command not found, trying socket connection")
            return self.check_tcp_connection(host, 80, timeout)

        except subprocess.SubprocessError as e:
            self.logger.error(f"Subprocess error pinging {host}: {str(e)}")
            return False

        except Exception as e:
            self.logger.error(f"Unexpected error pinging {host}: {str(e)}")
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
            # Validate inputs
            if not host or not host.strip():
                self.logger.warning("Empty host provided for TCP connection")
                return False

            if not isinstance(port, int) or port <= 0 or port > 65535:
                self.logger.error(f"Invalid port number: {port}")
                return False

            host = host.strip()

            self.logger.debug(f"Attempting TCP connection to {host}:{port}")

            # Create socket with timeout
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.settimeout(timeout)

                start_time = time.time()
                result = sock.connect_ex((host, port))
                connection_time = time.time() - start_time

                is_connected = result == 0

                if is_connected:
                    self.logger.debug(f"Successfully connected to {host}:{port} in {connection_time:.2f}s")
                else:
                    self.logger.debug(f"Failed to connect to {host}:{port} (error code: {result})")

                return is_connected

        except socket.gaierror as e:
            self.logger.error(f"DNS resolution failed for {host}: {str(e)}")
            return False

        except socket.timeout:
            self.logger.warning(f"Connection to {host}:{port} timed out after {timeout} seconds")
            return False

        except OSError as e:
            self.logger.error(f"OS error connecting to {host}:{port}: {str(e)}")
            return False

        except Exception as e:
            self.logger.error(f"Unexpected error connecting to {host}:{port}: {str(e)}")
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
        if not host or not host.strip():
            return False

        # Try common SMB ports
        smb_ports = [445, 139]  # Modern SMB (445) and legacy NetBIOS (139)

        for port in smb_ports:
            self.logger.debug(f"Checking SMB on {host}:{port}")
            if self.check_tcp_connection(host, port, timeout):
                self.logger.info(f"SMB service detected on {host}:{port}")
                return True

        self.logger.debug(f"No SMB service detected on {host}")
        return False

    def get_local_ip(self) -> str:
        """
        Get the local IP address of this machine

        Returns:
            Local IP address as string, or '127.0.0.1' if detection fails
        """
        try:
            # Method 1: Connect to a remote address to determine local IP
            with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
                # Connect to Google's DNS server (doesn't actually send data)
                sock.connect(("8.8.8.8", 80))
                local_ip = sock.getsockname()[0]

            if local_ip and local_ip != "127.0.0.1":
                self.logger.debug(f"Detected local IP: {local_ip}")
                return local_ip

        except Exception as e:
            self.logger.debug(f"Method 1 failed to detect local IP: {str(e)}")

        try:
            # Method 2: Use hostname resolution
            hostname = socket.gethostname()
            local_ip = socket.gethostbyname(hostname)

            if local_ip and local_ip != "127.0.0.1":
                self.logger.debug(f"Detected local IP via hostname: {local_ip}")
                return local_ip

        except Exception as e:
            self.logger.debug(f"Method 2 failed to detect local IP: {str(e)}")

        self.logger.warning("Failed to detect local IP, using loopback")
        return "127.0.0.1"

    def is_valid_ip(self, ip_address: str) -> bool:
        """
        Validate if a string is a valid IPv4 address

        Args:
            ip_address: String to validate

        Returns:
            True if valid IP address, False otherwise
        """
        if not ip_address or not isinstance(ip_address, str):
            return False

        try:
            # Check if it's a valid IPv4 address
            parts = ip_address.strip().split('.')
            if len(parts) != 4:
                return False

            for part in parts:
                if not part.isdigit():
                    return False
                num = int(part)
                if num < 0 or num > 255:
                    return False

            # Additional validation using socket
            socket.inet_aton(ip_address.strip())
            return True

        except (socket.error, ValueError, AttributeError):
            return False

    def is_valid_hostname(self, hostname: str) -> bool:
        """
        Validate if a string is a valid hostname

        Args:
            hostname: String to validate

        Returns:
            True if valid hostname, False otherwise
        """
        if not hostname or not isinstance(hostname, str):
            return False

        hostname = hostname.strip()

        # Basic hostname validation
        if len(hostname) > 253:
            return False

        if hostname.endswith('.'):
            hostname = hostname[:-1]

        allowed = re.compile(r"^[a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?$")

        return all(allowed.match(label) for label in hostname.split('.'))

    def resolve_hostname(self, hostname: str, timeout: int = 5) -> Optional[str]:
        """
        Resolve hostname to IP address

        Args:
            hostname: Hostname to resolve
            timeout: Resolution timeout in seconds

        Returns:
            IP address string, or None if resolution fails
        """
        if not hostname or not isinstance(hostname, str):
            return None

        try:
            hostname = hostname.strip()

            # Set socket timeout for DNS resolution
            old_timeout = socket.getdefaulttimeout()
            socket.setdefaulttimeout(timeout)

            try:
                ip_address = socket.gethostbyname(hostname)
                self.logger.debug(f"Resolved {hostname} to {ip_address}")
                return ip_address
            finally:
                socket.setdefaulttimeout(old_timeout)

        except socket.gaierror as e:
            self.logger.error(f"Failed to resolve {hostname}: {str(e)}")
            return None

        except Exception as e:
            self.logger.error(f"Unexpected error resolving {hostname}: {str(e)}")
            return None

    def check_internet_connectivity(self, timeout: int = 3) -> bool:
        """
        Check if internet connectivity is available

        Args:
            timeout: Timeout for each test

        Returns:
            True if internet is accessible, False otherwise
        """
        # Test with multiple reliable servers
        test_hosts = [
            "8.8.8.8",  # Google DNS
            "1.1.1.1",  # Cloudflare DNS
            "208.67.222.222"  # OpenDNS
        ]

        successful_pings = 0

        for host in test_hosts:
            try:
                if self.ping_host(host, timeout=timeout):
                    successful_pings += 1
                    self.logger.debug(f"Internet connectivity confirmed via {host}")

                    # If at least one ping succeeds, we have internet
                    if successful_pings >= 1:
                        return True

            except Exception as e:
                self.logger.debug(f"Failed to ping {host}: {str(e)}")
                continue

        self.logger.warning("No internet connectivity detected")
        return False

    def get_network_info(self) -> Dict[str, Any]:
        """
        Get comprehensive network information

        Returns:
            Dictionary with network information
        """
        info = {
            "local_ip": self.get_local_ip(),
            "has_internet": False,
            "system": self.system,
            "platform": platform.platform(),
            "timestamp": time.time()
        }

        # Check internet connectivity (with shorter timeout for info gathering)
        try:
            info["has_internet"] = self.check_internet_connectivity(timeout=2)
        except Exception as e:
            self.logger.warning(f"Failed to check internet connectivity: {str(e)}")
            info["has_internet"] = False

        return info

    def comprehensive_network_test(self, host: str, timeout: int = 5) -> Dict[str, Any]:
        """
        Perform comprehensive network testing for a host

        Args:
            host: Target host to test
            timeout: Timeout for tests

        Returns:
            Dictionary with test results
        """
        results = {
            "host": host,
            "timestamp": time.time(),
            "ping_test": False,
            "tcp_445_test": False,  # SMB
            "tcp_80_test": False,  # HTTP
            "tcp_443_test": False,  # HTTPS
            "dns_resolution": None,
            "is_valid_ip": False,
            "response_time": None
        }

        if not host:
            return results

        # Test if it's a valid IP
        results["is_valid_ip"] = self.is_valid_ip(host)

        # DNS resolution test (if not an IP)
        if not results["is_valid_ip"]:
            results["dns_resolution"] = self.resolve_hostname(host, timeout)

        # Ping test
        start_time = time.time()
        results["ping_test"] = self.ping_host(host, timeout)
        if results["ping_test"]:
            results["response_time"] = time.time() - start_time

        # TCP port tests
        common_ports = [
            (445, "tcp_445_test"),  # SMB
            (80, "tcp_80_test"),  # HTTP
            (443, "tcp_443_test")  # HTTPS
        ]

        for port, result_key in common_ports:
            try:
                results[result_key] = self.check_tcp_connection(host, port, timeout)
            except Exception as e:
                self.logger.debug(f"TCP test failed for {host}:{port}: {str(e)}")
                results[result_key] = False

        return results

# Import regex module at the top
# import re