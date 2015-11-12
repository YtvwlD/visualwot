#!/usr/bin/env python3
from argparse import ArgumentParser
from generate import WebofTrustVisualization

#parse the arguments
parser = ArgumentParser()

parser.add_argument("folder")
parser.add_argument("--pubkey")
parser.add_argument("--format", default="ps")

args = parser.parse_args()

if args.pubkey:
	w = WebofTrustVisualization(args.folder, pubkey=args.pubkey)
else:
	w = WebofTrustVisualization(args.folder)
	w.nextRound()
w.gendot()
w.draw(format=args.format)
