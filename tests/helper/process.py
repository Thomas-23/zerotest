import subprocess

from tests import DEBUG


def call_process(args):
    try:
        from subprocess import DEVNULL
    except ImportError:
        import os
        DEVNULL = open(os.devnull, 'wb')
    if DEBUG:
        out = None
        close_fds = False
    else:
        out = DEVNULL
        close_fds = True
    return subprocess.call(args, stdout=out, stderr=out, close_fds=close_fds)
