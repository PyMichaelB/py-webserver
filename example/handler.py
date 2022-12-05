import os

from webserver.utils.types import Response, Request, Header
from webserver.utils.constants import Status

dirname = os.path.dirname(__file__)

def handle_request(request: Request) -> Response:
    """Matches request to method and path and generates response"""

    with open(f'{dirname}/index.html', 'r') as html_file:
        # Format the HTML
        html: str = html_file.read().replace("{path}", request.path)

    return Response(Status.OK, headers=[Header("foo", "bar"), Header("bar", "foo")], body=html)
