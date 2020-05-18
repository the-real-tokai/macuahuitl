#!/usr/bin/env python3
"""
	Comitl
	Concentrically arranges randomly sized arcs into a pretty disc shape.

	Copyright © 2020 Christian Rosentreter
	All rights reserved.

	$Id: comitl.py 1 2020-05-16 00:00:00Z tokai $
"""

import math
import random
import argparse


__author__  = 'Christian Rosentreter'
__version__ = '1.1'
__all__     = []


ap = argparse.ArgumentParser(
	description=('Concentrically arranges randomly sized arcs into a pretty disc shape. Output is generated '
				'as a set of vector shapes in Scalable Vector Graphics (SVG) format and printed on the '
				'standard output stream.'),
	epilog='Mail bug reports and suggestions to <{}-comitl{}binaryriot{}>.'.format('feedback', chr(0x40), '.org'),
	add_help=False,
)

g = ap.add_argument_group('Startup')
g.add_argument('-V', '--version', action='version', version='%(prog)s {}'.format(__version__), help="show version number and exit")
g.add_argument('-h', '--help', action='help', help='show this help message and exit')

g = ap.add_argument_group('Algorithm')
g.add_argument('--circles',      metavar='INT',    type=int,   help='number of concentric arc elements to generate inside the disc  [:21]', default=21)
g.add_argument('--stroke-width', metavar='FLOAT',  type=float, help='width of the generated strokes  [:6]', default=6.0)
g.add_argument('--gap',          metavar='FLOAT',  type=float, help='distance between the generated strokes')
g.add_argument('--inner-radius', metavar='FLOAT',  type=float, help='setup an inner disc radius to create an annular shape')
g.add_argument('--hoffset',      metavar='FLOAT',  type=float, help='shift the whole disc horizontally  [:0.0]', default=0.0)
g.add_argument('--voffset',      metavar='FLOAT',  type=float, help='shift the whole disc vertically  [:0.0]', default=0.0)
g.add_argument('--colour',       metavar='COLOUR', type=str,   help='SVG compliant colour specification or identifier  [:black]', default='black')
g.add_argument('--random-seed',  metavar='INT',    type=int,   help='fixed initialisation of the random number generator for predictable results')
g.add_argument('--randomise',    action='store_true',          help='generate truly random discs layouts; other provided values are utilized as limits')

user_input = ap.parse_args()

chaos   = random.Random(user_input.random_seed)
circles = user_input.circles
stroke  = abs(user_input.stroke_width) if user_input.stroke_width else 1.0
gap     = user_input.gap if (user_input.gap is not None) else stroke
radius  = user_input.inner_radius if (user_input.inner_radius is not None) else stroke
x       = user_input.hoffset
y       = user_input.voffset
colour  = user_input.colour

if user_input.randomise:
	circles = chaos.randrange(0, circles) if circles else 0
	stroke  = chaos.uniform(0, stroke)
	stroke  = 1.0 if stroke == 0 else stroke
	gap     = chaos.uniform(0, gap)  # TODO: allow opposite values too (within limits)
	radius  = chaos.uniform(0, radius)
	x       = chaos.uniform(-x, x) if x else 0.0
	y       = chaos.uniform(-y, y) if y else 0.0
	colour  = '#{:02x}{:02x}{:02x}'.format(chaos.randrange(0, 255), chaos.randrange(0, 255), chaos.randrange(0, 255))


vb_offset = radius + ((circles + 1) * (stroke + gap))

print('<svg width="100%" height="100%" viewBox="{o} {o} {s} {s}"'.format(o=(-vb_offset), s=(vb_offset * 2)),
	 ' xmlns="http://www.w3.org/2000/svg">',
	 '<path d="', sep='', end='')


for circle in range(0, circles):
	theta = chaos.uniform(0, 2) * math.pi + math.pi
	t1    = -(chaos.uniform(0, 2) * math.pi + theta)
	t2    = -(chaos.uniform(0, 2) * math.pi + theta)

	if t1 < t2:
		t1, t2 = t2, t1

	print('M {sx} {sy}'.format(
		sx=round(x + radius * math.sin(t1), 9),
		sy=round(y + radius * math.cos(t1), 9)
	), 'A {r} {r} 0 {f} 1 {dx} {dy}'.format(
		r=radius,
		f=int(t1 - t2 > math.pi),
		dx=round(x + radius * math.sin(t2), 9),
		dy=round(y + radius * math.cos(t2), 9)
	), end=(' ' if circles - circle > 1 else ''))

	radius += (gap + stroke)


print('" stroke="{}" stroke-width="{}" stroke-linecap="round" fill="none"/>'.format(colour, stroke),
	'<circle cx="{}" cy="{}" r="{}" stroke="{}" stroke-width="{}" fill="none"/>'.format(x, y, radius, colour, stroke),
	'</svg>', sep='', end='')
