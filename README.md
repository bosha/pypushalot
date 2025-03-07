# Pushalot

**Pushalot doesn't exist nowdays. The repository is archived. Consider using alternatives.**

Wrapper around [pushalot.com](https://pushalot.com) API. 

> Pushalot is a platform for receiving custom push notifications to connected devices running Windows Phone or Windows 8. Custom means that those push notifications can be sent from virtually any source, as long as that source can interact with our open REST API. 

# Installation

```
pip install pushalot
```

# Usage

```python
from pushalot import Pushalot
api = Pushalot(token='your-token-here')
api.send(title='Testing', body='Hey!')
```

Or using factory:

```python
from pushalot import PushalotFactory
api = PushalotFactory.create(token='your-token-here')
```

You can provide custom 'transport' or API version.
Right now there is only one API version, and one transport:

```python
from pushalot import PushalotFactory
from pushalot.transport import HTTPTransport
from pushalot.apis import APILatest
api = PushalotFactory(
    token='your-token-here',
    api=APILatest(),
    transport=HTTPTransport()
)
```

This code snippet do the same that above snippets, but shows how some parts can be changed to suit your needs.

# Tests

```python
python setup.py test
```

coverage:
```
pip install coverage
coverage run -m unittest discover
```

# License

Released under MIT License. See the bundled LICENSE file for details.
