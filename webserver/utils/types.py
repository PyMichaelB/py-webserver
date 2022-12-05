from __future__ import annotations
from typing import List, Callable
import functools
from dataclasses import dataclass
from urllib.parse import urlparse

from .constants import Status, Method


class Request:
    """The class for a request."""
    def __init__(self, path: str, query: str, method: Method, headers: List[Header], body: str) -> None:
        self.path = path
        self.query = query
        self.method = method
        self.headers = headers
        self.body = body

    @property
    def key(self) -> tuple[Method, str]:
        """Property used to match this request to a route."""
        return self.method, self.path

    @classmethod
    def from_str(cls, request: str) -> Request:
        """Helper function to create a new request object from a decoded string request."""
        _lines: List[str] = request.split('\r\n')
        
        # Extract request sections
        status_line: str = _lines[0]
        headers: List[str] = _lines[1:-2]
        body: str = _lines[-1]
        
        method, path, _ = status_line.split(' ')
        headers = Header.from_str_list(headers)

        r = urlparse(path)

        return Request(
            path=r.path, 
            query=r.query, 
            method=Method(method), 
            headers=headers, 
            body=body
        )

@dataclass
class Response:
    """Class to hold a response object."""
    status: Status
    headers: List[Header]
    body: str
  
    @property
    def format_status(self) -> str:
        return f"HTTP/1.1 {self.status.value} {self.status.name}"

    @property
    def f(self) -> str:
        return '\r\n'.join([
            self.format_status, 
            Header.format(self.headers),
            self.body
        ])

@dataclass
class Header:
    """Class to hold the request and response header(s)."""
    name: str
    value: str
    
    @property
    def f(self) -> str:
        return f"{self.name}: {self.value}\r\n"    

    @classmethod
    def from_str_list(cls, header_lines: List[str]) -> List[Header]:
        return [
            cls(*map(str.strip, line.split(':', 1)))
            for line in header_lines
        ]

    @classmethod
    def format(cls, headers: List[Header]) -> str:
        return functools.reduce(lambda cur, h: cur + h.f, headers, "")

@dataclass
class Route:
    """Class to hold server routes. These are matched based on method and path only."""
    method: Method
    path: str
    resolve: Callable

    @property    
    def key(self) -> tuple[Method, str]:
        return self.method, self.path
