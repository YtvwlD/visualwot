#!/usr/bin/env python3
from subprocess import Popen, PIPE
import os

class InvalidArgumentException(Exception):
    pass

class WebofTrustVisualization():
    def __init__(self, folder, pubkey=None):
        self.folder = folder
        self.gpg2_dir = os.path.join(folder, "gnupg")
        self.gpg2_commandline = ["gpg2", "--homedir", self.gpg2_dir, "--keyserver", "pgp.mit.edu"]
        if not os.path.exists(self.folder):
            os.mkdir(self.folder)
        if os.path.exists(os.path.join(self.gpg2_dir, "pubring.gpg")) and not pubkey:
            print ("Continuing...")
        elif not os.path.exists(self.gpg2_dir) and pubkey:
            print ("Initializing with key {}...".format(pubkey))
            os.mkdir(self.gpg2_dir, mode=0o700)
            self.recv_keys(pubkey)
        else:
            raise InvalidArgumentException

    def recv_keys(self, *pubkeys):
        cmd = list(self.gpg2_commandline)
        cmd.append("--recv-keys")
        for pubkey in pubkeys:
            cmd.append(pubkey)
        Popen(cmd)
