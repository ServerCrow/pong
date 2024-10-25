from creyPY.fastapi.testing import GenericClient

from .main import app


class TestAPI:
    def setup_class(self):
        self.c = GenericClient(app)

    def test_swagger_gen(self):
        re = self.c.get("/openapi.json")
        assert re["info"]["title"] == "ServerCrow Pong API"

    def test_health_check(self):
        self.c.get("/", parse_json=False)

    def test_get_pong(self):
        re = self.c.get("/pong/?code=200&response_text=OK", parse_json=False)
        assert re == b"OK"

    def test_get_pong_404(self):
        re = self.c.get("/pong/?code=404&response_text=Not Found", parse_json=False, r_code=404)
        assert re == b"Not Found"

    def test_get_pong_503(self):
        re = self.c.get(
            "/pong/?code=503&response_text=Service Unavailable", parse_json=False, r_code=503
        )
        assert re == b"Service Unavailable"

    def test_get_pong_500(self):
        re = self.c.get(
            "/pong/?code=500&response_text=Internal Server Error", parse_json=False, r_code=500
        )
        assert re == b"Internal Server Error"

    def test_get_pong_400(self):
        re = self.c.get("/pong/?code=400&response_text=Bad Request", parse_json=False, r_code=400)
        assert re == b"Bad Request"

    def test_get_pong_401(self):
        re = self.c.get("/pong/?code=401&response_text=Unauthorized", parse_json=False, r_code=401)
        assert re == b"Unauthorized"
