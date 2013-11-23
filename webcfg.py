import os

using_nginx = False
html_path = 'static'
static_path = 'static'

host = '127.0.0.1'
port = 19191

ssl_conf = None

# Configure the following according to where ssss is installed.
ssss_split = os.path.abspath(os.path.join("ssss-0.5", "ssss-split"))

# ZMQ socket path for pushing/pulling data regarding emails to be sent.
# For more configurations about this, check send_email.py
zmqemail = 'ipc:///tmp/zmqemail_escrow'
