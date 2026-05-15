import os
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

HEALTH_RESPONSE = b'{"status":"ok"}'


class HealthCheckHandler(BaseHTTPRequestHandler):
    def do_GET(self) -> None:
        if self.path != "/health":
            self.send_error(404, "Not Found")
            return

        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(HEALTH_RESPONSE)))
        self.end_headers()
        self.wfile.write(HEALTH_RESPONSE)


def run_server(host: str = "0.0.0.0", port: int = 8000) -> None:
    with ThreadingHTTPServer((host, port), HealthCheckHandler) as httpd:
        httpd.serve_forever()


if __name__ == "__main__":
    run_server(port=int(os.getenv("PORT", "8000")))
