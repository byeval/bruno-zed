import contextlib
import importlib.machinery
import importlib.util
import io
import json
import pathlib
import tempfile
import threading
import unittest
from http.server import BaseHTTPRequestHandler, HTTPServer


ROOT = pathlib.Path(__file__).resolve().parents[1]
RUNNER = ROOT / "bin" / "bru-zed-yaml-run"


loader = importlib.machinery.SourceFileLoader("bru_zed_yaml_run", str(RUNNER))
spec = importlib.util.spec_from_loader(loader.name, loader)
runner = importlib.util.module_from_spec(spec)
loader.exec_module(runner)


class CaptureHandler(BaseHTTPRequestHandler):
    captured = {}

    def do_POST(self):
        length = int(self.headers.get("content-length", "0"))
        body = self.rfile.read(length)
        self.__class__.captured = {
            "path": self.path,
            "headers": dict(self.headers.items()),
            "body": body.decode("utf-8"),
        }
        payload = json.dumps({"ok": True, "path": self.path}).encode("utf-8")
        self.send_response(201)
        self.send_header("content-type", "application/json")
        self.send_header("content-length", str(len(payload)))
        self.end_headers()
        self.wfile.write(payload)

    def log_message(self, *_args):
        return


class YamlRunnerTest(unittest.TestCase):
    def test_builds_form_urlencoded_request_without_external_yaml(self):
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            (root / "opencollection.yml").write_text("name: sample\n", encoding="utf-8")
            request_path = root / "request.yml"
            request_path.write_text(
                """\
info:
  name: sample
  type: http

headers:
  - name: x-token
    value: secret

http:
  method: POST
  url: http://localhost/example
  query:
    data:
      - name: q
        value: search
      - name: ignored
        value: nope
        disabled: true
  body:
    type: form-urlencoded
    data:
      - name: html
        value: |-
          <main>
            hello
          </main>
      - name: enabled
        value: true
""",
                encoding="utf-8",
            )

            spec = runner.request_from_yaml(str(request_path))

        self.assertEqual(spec["method"], "POST")
        self.assertEqual(spec["url"], "http://localhost/example?q=search")
        self.assertEqual(spec["headers"]["x-token"], "secret")
        self.assertEqual(spec["headers"]["Content-Type"], "application/x-www-form-urlencoded")
        self.assertEqual(
            spec["body"].decode("utf-8"),
            "html=%3Cmain%3E%0A++hello%0A%3C%2Fmain%3E&enabled=true",
        )

    def test_interpolates_collection_environment_request_and_process_variables(self):
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            (root / "environments").mkdir()
            (root / "users").mkdir()
            (root / ".env").write_text("API_SECRET=from-dotenv\n", encoding="utf-8")
            (root / "opencollection.yml").write_text(
                """\
name: sample
variables:
  - name: baseUrl
    value: http://collection.example
  - name: token
    value: collection-token
""",
                encoding="utf-8",
            )
            (root / "environments" / "Local.yml").write_text(
                """\
name: Local
variables:
  - name: baseUrl
    value: http://env.example
  - name: token
    value: "{{process.env.API_SECRET}}"
""",
                encoding="utf-8",
            )
            env_file = root / "custom-env.json"
            env_file.write_text(
                json.dumps(
                    {
                        "variables": [
                            {"name": "source", "value": "env-file", "enabled": True},
                            {"name": "disabled", "value": "nope", "enabled": False},
                        ]
                    }
                ),
                encoding="utf-8",
            )
            (root / "users" / "folder.yml").write_text(
                """\
variables:
  - name: folderId
    value: folder-42
""",
                encoding="utf-8",
            )
            request_path = root / "users" / "request.yml"
            request_path.write_text(
                """\
variables:
  - name: userId
    value: user-7

http:
  method: POST
  url: "{{baseUrl}}/users/{{userId}}/{{folderId}}"
  headers:
    - name: Authorization
      value: Bearer {{token}}
    - name: X-Secret
      value: "{{process.env['API_SECRET']}}"
  query:
    data:
      - name: from
        value: "{{source}}"
  body:
    type: json
    data:
      id: "{{userId}}"
      token: "{{token}}"
""",
                encoding="utf-8",
            )

            spec = runner.request_from_yaml(
                str(request_path),
                root=str(root),
                env_name="Local",
                env_files=[str(env_file)],
                env_vars=["token=override-token"],
            )

        self.assertEqual(spec["url"], "http://env.example/users/user-7/folder-42?from=env-file")
        self.assertEqual(spec["headers"]["Authorization"], "Bearer override-token")
        self.assertEqual(spec["headers"]["X-Secret"], "from-dotenv")
        self.assertEqual(json.loads(spec["body"].decode("utf-8")), {"id": "user-7", "token": "override-token"})
        self.assertEqual(spec["unresolved_variables"], [])

    def test_run_request_prints_status_headers_and_json_body(self):
        server = HTTPServer(("127.0.0.1", 0), CaptureHandler)
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        try:
            with tempfile.TemporaryDirectory() as directory:
                root = pathlib.Path(directory)
                (root / "opencollection.yml").write_text("name: sample\n", encoding="utf-8")
                request_path = root / "request.yml"
                request_path.write_text(
                    f"""\
http:
  method: POST
  url: http://127.0.0.1:{server.server_port}/echo
  body:
    type: json
    data:
      hello: world
""",
                    encoding="utf-8",
                )

                output = io.StringIO()
                with contextlib.redirect_stdout(output):
                    exit_code = runner.run_request(str(request_path))

            self.assertEqual(exit_code, 0)
            self.assertIn("HTTP 201 Created", output.getvalue())
            self.assertIn("content-type: application/json", output.getvalue().lower())
            self.assertIn('"ok": true', output.getvalue())
            self.assertEqual(CaptureHandler.captured["path"], "/echo")
            self.assertEqual(CaptureHandler.captured["body"], '{"hello": "world"}')
        finally:
            server.shutdown()
            server.server_close()


if __name__ == "__main__":
    unittest.main()
