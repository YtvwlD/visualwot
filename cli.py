#!/usr/bin/env python3

#    visualwot - Visualize it!
#    Copyright (C) 2015  Niklas Sombert
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

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
