#!/usr/bin/env python3
from argparse import ArgumentParser
from generate import WebofTrustVisualization

#parse the arguments
parser = ArgumentParser()

parser.add_argument("folder")
parser.add_argument("--pubkey")

args = parser.parse_args()

if args.pubkey:
	w = WebofTrustVisualization(args.folder, pubkey=args.pubkey)
	w.gendot()
else:
	w = WebofTrustVisualization(args.folder)
	w.nextRound()
	w.gendot()
