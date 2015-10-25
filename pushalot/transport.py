import json
from abc import (
    ABCMeta,
    abstractmethod,
)
from six import with_metaclass
try:
    from urllib.request import urlopen
    from urllib.parse import (
        urlparse,
        urlencode,
    )
except ImportError:
    from urlparse import urlparse
    from urllib import (
        urlopen,
        urlencode,
    )

import exc

API_URL = 'https://pushalot.com/api/sendmessage'

class PushalotTransportInterface(with_metaclass(ABCMeta)):

    @abstractmethod
    def send(self, **kwargs):
        """
        :return:
        :rtype: bool
        """

class HTTPTransport(PushalotTransportInterface):

    def send(self, **kwargs):
        try:
            response = urlopen(url=API_URL, data=urlencode(kwargs))
        except (Exception) as e:
            # TODO: log
            raise exc.PushalotException(
                'Something goes wrong while sending request '
                'to pushalot server.'
            )
        text = "\n".join(response.readlines())
        decoded = json.loads(text)
        code = response.code
        response.close()
        if code == 200:
            return True
        elif code == 400:
            raise exc.PushalotBadRequestException(
                decoded.Description
            )
        elif code == 406:
            raise exc.PushalotNotAcceptableException(
                decoded.Description
            )
        elif code == 410:
            raise exc.PushalotGoneException(
                decoded.Description
            )
        elif code == 500:
            raise exc.PushalotInternalErrorException()
        elif code == 503:
            raise exc.PushalotUnavailableException()
