import warnings
from abc import (
    ABCMeta,
    abstractmethod,
)
from six import with_metaclass

import exc

class BaseAPI(with_metaclass(ABCMeta)):

    def __init__(self, token, transport):
        self._token = token
        self._transport = transport

    @abstractmethod
    def send(self, **kwargs):
        """

        :param kwargs:
        :return:
        """

    @abstractmethod
    def get_api_methods(self):
        """
        :return: Should return dict with available pushalot API methods
        :rtype: dict
        """

    @abstractmethod
    def get_api_required_methods(self):
        """
        List with required params
        :return:
        :rtype: list
        """

    def _build_params_from_kwargs(self, **kwargs):
        api_methods = self.get_api_methods()
        required_methods = self.get_api_required_methods()
        ret_kwargs = {}
        for key, val in kwargs.items():
            if key not in api_methods:
                warnings.warn(
                    'Passed uknown parameter [{}]'.format(key),
                    Warning
                )
                continue
            if key not in required_methods and val is None:
                continue
            if type(val) != api_methods[key]['type']:
                raise ValueError(
                    "Invalid type specified to param: {}".format(key)
                )
            if 'max_len' in api_methods[key]:
                if len(val) > api_methods[key]['max_len']:
                    raise ValueError(
                        "Lenght of parameter [{}] more than "
                        "allowed length".format(key)
                    )
            ret_kwargs[api_methods[key]['param']] = val

        for item in required_methods:
            if item not in ret_kwargs:
                raise exc.PushalotException(
                    "Parameter [{}] required, but not set".format(item)
                )

        return ret_kwargs


class APILatest(BaseAPI):

    def send(self, title, body,
             link_title=None, link=None, is_important=False,
             is_silent=False, image=None, source=None, ttl=None, **kwargs):
        """
        :param token: Service authorization token
        :type token: str
        :param title: Message title, up to 250 characters
        :type title: str
        :param body:  Message body, up to 32768 characters
        :type body: str
        :param link_title: Title of the link, up to 100 characters
        :type link: str
        :param link: Link URI, up to 1000 characters
        :type link: str
        :param is_important: Determines, is message important
        :type is_important: bool
        :param is_silent:  Prevents toast notifications on devices
        :type is_silent: bool
        :param image: Image URL link, up to 250 characters
        :type image: str
        :param source: Notifications source name, up to 25 characters
        :type source: str
        :param ttl: Message time to live in minutes (0 .. 43200)
        :type ttl: int
        :return: True on success
        """
        params = self._build_params_from_kwargs(
            token=self._token,
            title=title,
            body=body,
            link_title=link_title,
            link=link,
            is_important=is_important,
            is_silent=is_silent,
            image=image,
            source=source,
            ttl=ttl,
            **kwargs
        )
        return self._transport.send(**params)

    def send_message(self, title, body):
        return self.send(title=title, body=body)

    def send_silent_message(self, title, body):
        return self.send(title=title, body=body, is_silent=True)

    def send_important_message(self, title, body):
        return self.send(title=title, body=body, is_important=True)

    def send_with_expiry(self, title, body, ttl):
        return self.send(title=title, body=body, ttl=ttl)

    def send_with_link(self, title, body, link, link_title=None):
        link_title = link_title or link
        return self.send(
            title=title,
            body=body,
            link=link,
            link_title=link_title
        )

    def send_with_icon(self, title, body, image):
        return self.send(title=title, body=body, image=image)

    def get_api_methods(self):
        return {
            'token': {
                'param': 'AuthorizationToken',
                'type': str,
                'max_len': 32,
            },
            'title': {
                'param': 'Title',
                'type': str,
                'max_len': 250,
            },
            'body': {
                'param': 'Body',
                'type': str,
                'max_len': 32768,
            },
            'link_title': {
                'param': 'LinkTitle',
                'type': str,
                'max_len': 100,
            },
            'link': {
                'param': 'Link',
                'type':str,
                'max_len': 1000,
            },
            'is_important': {
                'param': 'IsImportant',
                'type': bool,
            },
            'is_silent': {
                'param': 'IsSilent',
                'type': bool,
            },
            'image': {
                'param': 'Image',
                'type': str,
                'max_len': 250,
            },
            'source': {
                'param': 'Source',
                'type': str,
                'max_len': 25,
            },
            'ttl': {
                'param': 'TimeToLive',
                'type': int,
                # 'max_len': 43200,
            }
        }

    def get_api_required_methods(self):
        return ['AuthorizationToken', 'Title', 'Body']
