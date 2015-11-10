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
			self.getNumber()
		elif not os.path.exists(self.gpg2_dir) and pubkey:
			print ("Initializing with key {}...".format(pubkey))
			os.mkdir(self.gpg2_dir, mode=0o700)
			self.recv_keys(pubkey)
			self.number = 0
			self.saveNumber()
		else:
			raise InvalidArgumentException

	def recv_keys(self, *pubkeys):
		cmd = list(self.gpg2_commandline)
		cmd.append("--recv-keys")
		for pubkey in pubkeys:
			cmd.append(pubkey)
		Popen(cmd).wait()

	def gendot(self):
		cmd = list(self.gpg2_commandline)
		cmd.append("--list-sigs")
		with open(os.path.join(self.folder, "{}.dot".format(self.number)), "w") as dot:
			with Popen(cmd, stdout=PIPE) as gpg2:
				Popen(["sig2dot", "-a"], stdin=gpg2.stdout, stdout=dot).wait()

	def draw(self, format="ps"):
		with open("{}.{}".format(os.path.join(self.folder, str(self.number)), format), "w") as drawing:
			Popen(["dot", "-T{}".format(format), "{}.dot".format(os.path.join(self.folder, str(self.number)))], stdout=drawing).wait()

	def nextRound(self):
		cmd = list(self.gpg2_commandline)
		cmd.append("--list-sigs")
		sigs_missing = []
		with Popen(cmd, stdout=PIPE, env={"LANG": "C.UTF-8"}) as gpg2:
			for sig in gpg2.stdout.read().splitlines():
				if b"[User ID not found]" in sig:
					for elem in sig.split():
						if len(elem) == 8:
							if elem.decode() not in sigs_missing: #we need each key only once
								sigs_missing.append(elem.decode())
		self.number += 1 #better safe than sorry
		self.saveNumber()
		self.recv_keys(*sigs_missing)

	def getNumber(self):
		with open(os.path.join(self.folder, "number"), "r") as number:
			self.number = int(number.read().strip())

	def saveNumber(self):
		with open(os.path.join(self.folder, "number"), "w") as number:
			number.write(str(self.number))
