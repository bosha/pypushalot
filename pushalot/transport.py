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
        """Send request to API

        Only this method required. Method receives
        dictionary with api requests params, and
        send request.
        Should return True if request successfully sent,
        or throw exception on failure.

        :raises PushalotBadRequestException: Bad parameters sent to API
        :raises PushalotNotAcceptableException: API message throttle limit hit
        :raises: PushalotGoneException: Invalid or blocked authorization token
        :raises PushalotInternalErrorException: API server error
        :raises PushalotUnavailableException: API server unavailable
        :param kwargs: Dictionary with API request parameters
        :type kwargs: dict
        :return: True on success
        :rtype: bool
        """

class HTTPTransport(PushalotTransportInterface):

    def send(self, **kwargs):
        try:
            params = urlencode(kwargs)
            response = urlopen(url=API_URL, data=params)
            text = "\n".join(response.readlines())
            decoded = json.loads(text)
            code = response.code
            response.close()
        except Exception as e:
            import sys
            raise exc.PushalotException(
                'Uncaught API exception: {}'.format(str(e))
            ), None, sys.exc_info()[2]

        if code == 200:
            if decoded['Success'] == False:
                raise exc.PushalotException(
                    "Uncaught error occupied: {}".format(decoded['Description'])
                )
            return True
        elif code == 400:
            raise exc.PushalotBadRequestException(
                decoded['Description']
            )
        elif code == 406:
            raise exc.PushalotNotAcceptableException(
                decoded['Description']
            )
        elif code == 410:
            raise exc.PushalotGoneException(
                decoded['Description']
            )
        elif code == 500:
            raise exc.PushalotInternalErrorException()
        elif code == 503:
            raise exc.PushalotUnavailableException()
