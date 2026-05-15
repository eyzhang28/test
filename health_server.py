"""Lightweight HTTP health check endpoint.

This module intentionally uses only Python's standard library so deployments
can run the health endpoint without additional dependencies.
"""

from __future__ import annotations

import argparse
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlsplit


HEALTH_RESPONSE_BODY = b'{"status":"ok"}'


class HealthCheckHandler(BaseHTTPRequestHandler):
    """Serve a tiny, unauthenticated health endpoint."""

    def do_GET(self) -> None:  # noqa: N802 (required method name)
        if urlsplit(self.path).path != "/health":
            self.send_error(HTTPStatus.NOT_FOUND)
            return

        self.send_response(HTTPStatus.OK)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(HEALTH_RESPONSE_BODY)))
        self.end_headers()
        self.wfile.write(HEALTH_RESPONSE_BODY)

    def log_message(self, _format: str, *_args: object) -> None:
        # Keep endpoint output minimal and quiet in health probes.
        return


def run_server(host: str = "0.0.0.0", port: int = 8000) -> None:
    """Start the health check server."""

    httpd = ThreadingHTTPServer((host, port), HealthCheckHandler)
    print(f"Serving health checks on http://{host}:{port}/health")
    httpd.serve_forever()


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run health check HTTP server.")
    parser.add_argument("--host", default="0.0.0.0", help="Host interface to bind.")
    parser.add_argument(
        "--port",
        default=8000,
        type=int,
        help="Port to listen on.",
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = _parse_args()
    run_server(host=args.host, port=args.port)
