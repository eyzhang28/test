import json
import unittest
from http.client import HTTPConnection
from threading import Thread

from server import HEALTH_RESPONSE, HealthCheckHandler
from http.server import ThreadingHTTPServer


class HealthEndpointSmokeTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.server = ThreadingHTTPServer(("127.0.0.1", 0), HealthCheckHandler)
        cls.port = cls.server.server_port
        cls.thread = Thread(target=cls.server.serve_forever, daemon=True)
        cls.thread.start()

    @classmethod
    def tearDownClass(cls) -> None:
        cls.server.shutdown()
        cls.server.server_close()
        cls.thread.join(timeout=2)

    def test_health_returns_expected_payload(self) -> None:
        conn = HTTPConnection("127.0.0.1", self.port, timeout=5)
        conn.request("GET", "/health")
        response = conn.getresponse()
        body = response.read()
        conn.close()

        self.assertEqual(response.status, 200)
        self.assertEqual(response.getheader("Content-Type"), "application/json")
        self.assertEqual(body, HEALTH_RESPONSE)
        self.assertEqual(json.loads(body.decode("utf-8")), {"status": "ok"})


if __name__ == "__main__":
    unittest.main()
