from apis import APILatest
from transport import HTTPTransport

class PushalotAPI(object):

    def __init__(self, token, transport):
        self._token = token
        self._transport = transport

    def send_message(self, title, body):
        return self._transport.send(
            token=self._token,
            title=title,
            body=body
        )
