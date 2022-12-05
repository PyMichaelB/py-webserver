import asyncio

from webserver.utils.constants import Method
from webserver.utils.types import Route
from webserver.server import HttpServer

from handler import handle_request

if __name__ == "__main__":
    server = HttpServer({
        "port": 8090,
        "host": "0.0.0.0"
    })
    
    route1 = Route(method=Method.GET, path='/home', resolve=handle_request)
    route2 = Route(method=Method.GET, path='/contacts', resolve=handle_request)

    server.add_route(route1) 
    server.add_route(route2)

    asyncio.run(server.run())