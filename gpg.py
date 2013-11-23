import os
import tempfile
import subprocess

import webcfg

def encrypt(msg, recipient):
    temp_fd, temp = tempfile.mkstemp()
    os.write(temp_fd, msg)
    os.close(temp_fd)
    proc = subprocess.Popen([webcfg.gpg, '--quiet', '--armor', '--no-tty',
        '--batch', '--trust-model', 'always', '--output', '-', '--encrypt',
        '--keyserver-options', 'timeout=3', '--recipient', recipient, temp],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = proc.communicate()
    failed = stderr.strip() != '' # Very rough approximation.
    os.remove(temp)
    return stdout, failed

def import_key(pubkey):
    temp_fd, temp = tempfile.mkstemp()
    os.write(temp_fd, pubkey)
    os.close(temp_fd)
    proc = subprocess.Popen([webcfg.gpg, '--quiet', '--no-tty', '--batch',
        '--import', temp], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = proc.communicate()
    os.remove(temp)
    return stderr.strip()
