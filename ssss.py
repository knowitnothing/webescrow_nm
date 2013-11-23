import os
import subprocess

import webcfg


def split(secret, n, m):
    cmd = webcfg.ssss_split
    proc = subprocess.Popen([cmd, "-t", str(n), "-n", str(m), "-w", "s", "-q"],
            stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    stdout, _ = proc.communicate(secret)
    shares = stdout.strip().split()
    return shares

