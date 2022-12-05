from __future__ import annotations

import logging
import socket

from .utils.errors import PortValidationError

LOGGER = logging.getLogger(__name__)


class SocketConfig:
    """Class to provide TCP socket configuration."""
    def __init__(self, host: str, port: int, backlog: int) -> None:
        self.host = host

        if not 0 < port < 65565:
            raise PortValidationError(f"Port {port} is invalid.")
    
        self.port = port
        self.backlog = backlog

    @classmethod
    def create(cls, config) -> SocketConfig:
        """Helper function to create a SocketConfig (with defaults) from a config dictionary."""
        host = config.get('host', '127.0.0.1')
        port = config.get('port', 5000)
        backlog = config.get('backlog', 10)
        return SocketConfig(host, port, backlog)


class SocketFactory:
    def __init__(self, conf: SocketConfig):
        """Initialise the socket factory with config.
        :param conf: the configuration object to initialise a socket from
        :type conf: SocketConfig
        """
        self.conf = conf
    
    def create(self) -> socket.socket:
        """Create a new TCP socket for the server."""
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        LOGGER.info("serving on %s at %s", self.conf.port, self.conf.host)

        server_socket.bind((self.conf.host, self.conf.port))
        server_socket.listen(self.conf.backlog)

        return server_socket