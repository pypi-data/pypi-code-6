import json, subprocess, os, random
from clint.textui import colored

class TestHttpParser:

    def execute(self, stdin_data):
        args = ["{0}/bin/http_parser".format(os.getcwd())]
        try:
            p = subprocess.Popen(args,
                    stdin=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    stdout=subprocess.PIPE)
        except OSError:
            exit(colored.red(">>> Check your bin/http_parser. It must be the executable script with your code."))

        (result, stderr) = p.communicate(stdin_data.encode("utf-8"))
        if stderr:
            exit(colored.red("Error from your code: '{}'".format(stderr)))

        try:
            parsed = json.loads(result.decode("utf-8"))
        except ValueError as e:
            exit(colored.red(">>> Expected json in STDOUT, but actually was '{}'".format(result)))

        return parsed


    def test_error_on_invalid_data(self):
        result = self.execute("HAHA")
        assert "error" in result


    def test_basic_api(self):
        method = random.choice(["GET", "HEAD"])
        query_value = random.random()
        curl_version = random.randint(1, 10)
        port = random.randint(3000, 5000)

        words = ["W", "o", "r", "l", "d"]
        random.shuffle(words)
        body = "".join(words)

        headers = []
        headers.append("{0} /test?ok={1} HTTP/1.1\r\n".format(method, query_value))
        headers.append("User-Agent: curl/{0}\r\n".format(curl_version))
        headers.append("Host: 0.0.0.0:{0}\r\n".format(port))
        headers.append("Accept: */*\r\n")
        headers.append("Content-Length: 5\r\n")
        headers.append("\r\n")
        headers.append(body)

        http_request = "".join(headers)
        result = self.execute(http_request)

        assert "curl/{0}".format(curl_version) == result["User-Agent"]
        assert "5" == result["Content-Length"]
        assert method == result["method"]
        assert "0.0.0.0:{0}".format(port) == result["Host"]
        assert "*/*" == result["Accept"]
        assert "/test?ok={0}".format(query_value) == result["url"]
        assert "1.1" == result["http_version"]
        assert body == result["body"]
