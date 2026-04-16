import http.client
import threading
import unittest
from http.server import ThreadingHTTPServer

from health_server import HealthCheckHandler


class HealthCheckHandlerTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.server = ThreadingHTTPServer(("127.0.0.1", 0), HealthCheckHandler)
        cls.thread = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.thread.start()
        cls.host, cls.port = cls.server.server_address

    @classmethod
    def tearDownClass(cls) -> None:
        cls.server.shutdown()
        cls.server.server_close()
        cls.thread.join(timeout=2)

    def _request(self, method: str, path: str) -> tuple[int, str, dict[str, str]]:
        connection = http.client.HTTPConnection(self.host, self.port, timeout=5)
        try:
            connection.request(method, path)
            response = connection.getresponse()
            body = response.read().decode("utf-8")
            headers = {key.lower(): value for key, value in response.getheaders()}
            return response.status, body, headers
        finally:
            connection.close()

    def test_get_health_returns_expected_json(self) -> None:
        status, body, headers = self._request("GET", "/health")

        self.assertEqual(status, 200)
        self.assertEqual(body, '{"status":"ok"}')
        self.assertEqual(headers.get("content-type"), "application/json")

    def test_unknown_path_returns_not_found(self) -> None:
        status, _, _ = self._request("GET", "/missing")

        self.assertEqual(status, 404)


if __name__ == "__main__":
    unittest.main()
