Requirements
============

Python 2.7 (http://python.org),
ZMQ (http://zeromq.org/),
pyzmq (https://github.com/zeromq/pyzmq),
python-ecdsa (https://github.com/warner/python-ecdsa)
ssss (http://point-at-infinity.org/ssss/),
tornado (http://www.tornadoweb.org/),
OpenSSL (https://www.openssl.org/),
pyOpenSSL (https://launchpad.net/pyopenssl),
GPG (http://gnupg.org/),
and a SMTP server properly configured.

Setup
=====

Adjust `webcfg.py` and `send_email.py` to match your local
configurations. Make sure the program `ssss-split` is found at
the place specified by `ssss_split` at `webcfg.py`.

Running
=======

The rough way: `python send_email.py & python main.py`. It is
recommended to setup supervisord, as well using nginx for
serving static files.
