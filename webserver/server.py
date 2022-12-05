import logging
from typing import Callable, Optional, Mapping, Any

from _thread import start_new_thread

from .socket_setup import SocketConfig, SocketFactory
from .utils.types import Request, Response, Route
from .utils.constants import Status

logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__name__)


class HttpServer:
    BAD_REQUEST = Response(status=Status.BAD_REQUEST, headers=[], body='Bad request.')
    NOT_FOUND = Response(status=Status.NOT_FOUND, headers=[], body='The requested page doesn\'t exist.')

    def __init__(self, config: Mapping[str, Any]):
        """Initialise the HTTP webserver.
        Loads config and sets up the socket configuration.
        """    
        self.socketconf = SocketConfig.create(config)
        self.routes: Mapping[Route] = {}

    def add_route(self, route: Route) -> None:
        """Adds a new route to the webserver
        :param route: the route object to add
        :type route: Route
        """
        self.routes[route.key] = route
        LOGGER.info('added route for %s at %s', route.method, route.path)

    def respond(self, request: Request) -> Callable:
        """Method to match the request to a route and produce a response object."""
        # Look for a resolver for this route
        matched_route: Optional[Route] = self.routes.get(request.key)
        return matched_route.resolve(request) if matched_route is not None else self.NOT_FOUND

    def handle_request(self, client_connection):
        """Matches and responds to new client connections.
        :param client_connection: the socket connection made with the user
        :type client_connection: socket
        """
        # Get the client request
        request_str = client_connection.recv(1024).decode()
        request = Request.from_str(request_str) if request_str != "" else None

        # Produce response
        response = self.respond(request) if request is not None else self.BAD_REQUEST

        # Send HTTP response
        client_connection.sendall(response.f.encode())
        client_connection.close()
 
    async def run(self):
        """Async method to run the webserver."""
        sf: SocketFactory = SocketFactory(self.socketconf)
        server_socket = sf.create()

        while True:    
            # Wait for client connections
            client_connection, _ = server_socket.accept()
            start_new_thread(self.handle_request, (client_connection,))
