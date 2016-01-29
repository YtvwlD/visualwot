#!/usr/bin/env python3
from subprocess import Popen, PIPE
from gnupg import GPG
import os

class InvalidArgumentException(Exception):
	pass

class WebofTrustVisualization():
	def __init__(self, folder, pubkey=None):
		self.folder = folder
		self.gpg2_dir = os.path.join(folder, "gnupg")
		if not os.path.exists(self.folder):
			os.mkdir(self.folder)
		if os.path.exists(os.path.join(self.gpg2_dir, "pubring.gpg")) and not pubkey:
			print ("Continuing...")
			self.getNumber()
			self.gpg2 = GPG(gpgbinary="gpg2", gnupghome=self.gpg2_dir)
		elif not os.path.exists(self.gpg2_dir) and pubkey:
			print ("Initializing with key {}...".format(pubkey))
			os.mkdir(self.gpg2_dir, mode=0o700)
			self.gpg2 = GPG(gpgbinary="gpg2", gnupghome=self.gpg2_dir)
			self.recv_keys(pubkey)
			self.number = 0
			self.saveNumber()
		else:
			raise InvalidArgumentException

	def recv_keys(self, *pubkeys):
		self.gpg2.recv_keys("pgp.mit.edu", *pubkeys)

	def gendot(self):
		with open(os.path.join(self.folder, "{}.dot".format(self.number)), "w") as dot:
			with Popen(self.gpg2.make_args(["--list-sigs"], False), stdout=PIPE) as gpg2:
				Popen(["sig2dot", "-a"], stdin=gpg2.stdout, stdout=dot).wait()

	def draw(self, format="ps"):
		with open("{}.{}".format(os.path.join(self.folder, str(self.number)), format), "w") as drawing:
			Popen(["dot", "-T{}".format(format), "{}.dot".format(os.path.join(self.folder, str(self.number)))], stdout=drawing).wait()

	def nextRound(self):
		sigs_missing = []
		print ("gpg2")
		with Popen(self.gpg2.make_args(["--list-sigs"], False), stdout=PIPE, env={"LANG": "C.UTF-8"}) as gpg2:
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
