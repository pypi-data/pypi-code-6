import unittest
import byu_ws_sdk as oit
import credentials


class TestOITWebServicesLibrary(unittest.TestCase):

    def test_credentials(self):
        self.assertTrue(credentials.key, "No key supplied in credentials.py")
        self.assertTrue(credentials.shared_secret, "No shared_secret supplied in credentials.py")
        self.assertTrue(credentials.username, "No username supplied in credentials.py")
        self.assertTrue(credentials.password, "No password supplied in credentials.py")

    def test_send_wsSession_request_v1(self):
        wsSession = oit.get_ws_session(credentials.username,
                                       credentials.password, 1)
        self.assertTrue("apiKey" in wsSession)
        self.assertTrue(wsSession["apiKey"])
        self.assertTrue("personId" in wsSession)
        self.assertTrue(wsSession["personId"])
        self.assertTrue("expireDate" in wsSession)
        self.assertTrue(wsSession["expireDate"])
        self.assertTrue("sharedSecret" in wsSession)
        self.assertTrue(wsSession["sharedSecret"])

        url = "https://ws.byu.edu/example/authentication/hmac/services/v1/exampleWS"
        headerValue = oit.get_http_authorization_header(wsSession['apiKey'], wsSession['sharedSecret'],
                                                        "WsSession", "URL", url)

        version, status, headers, response = oit.send_ws_request(url, "GET", headers={'Authorization': headerValue})
        print(version)
        self.assertTrue(version)

    def test_send_apiKey_request_v1(self):
        url = "https://ws.byu.edu/example/authentication/hmac/services/v1/exampleWS"
        headerValue = oit.get_http_authorization_header(
            credentials.key,
            credentials.shared_secret,
            "API", "URL", url)

        version, status, headers, response = oit.send_ws_request(url, "GET", headers={'Authorization': headerValue})
        print(version)
        self.assertTrue(version)

    def test_get_nonce(self):
        nonce = oit.get_nonce(credentials.key)
        print(nonce)
        self.assertTrue(nonce["nonceKey"])
        self.assertTrue(nonce["nonceValue"])
        nonce = oit.get_nonce(credentials.key, "abc")
        print(nonce)
        self.assertTrue(nonce["nonceKey"])
        self.assertTrue(nonce["nonceValue"])


if __name__ == "__main__":
    unittest.main()
