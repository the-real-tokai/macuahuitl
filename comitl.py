#!/usr/bin/env python3
"""
	Comitl
	Concentrically arranges randomly sized arcs into a pretty disc shape.

	Copyright © 2020 Christian Rosentreter
	All rights reserved.

	$Id: comitl.py 84 2020-05-20 16:04:16Z tokai $
"""

import math
import random
import argparse


__author__  = 'Christian Rosentreter'
__version__ = '1.4'
__all__     = ['SVGArcPathSegment']



class SVGArcPathSegment():
	"""An 'arc' SVG path segment."""

	def __init__(self, offset=0.0, angle=90.0, radius=1.0, x=0.0, y=0.0):
		if abs(angle) >= 360:
			raise ValueError('angles of SVG arc path segments must be smaller than 360°')
		self.offset      = offset
		self.angle       = angle
		self.radius      = radius
		self.x           = x
		self.y           = y

	def __str__(self):
		ts = (self.offset - 180.0) * math.pi / -180.0
		td = (self.offset + self.angle - 180.0) * math.pi / -180.0

		return 'M {sx} {sy} A {r} {r} 0 {f} 1 {dx} {dy}'.format(
			sx=round(self.x + self.radius * math.sin(ts), 9),
			sy=round(self.y + self.radius * math.cos(ts), 9),
			r=self.radius,
			f=int(abs(ts - td) > math.pi),
			dx=round(self.x + self.radius * math.sin(td), 9),
			dy=round(self.y + self.radius * math.cos(td), 9)
		)



def main():
	"""First, build fire. Second, start coffee."""

	ap = argparse.ArgumentParser(
		description=('Concentrically arranges randomly sized arcs into a pretty disc shape. Output is '
			'generated as a set of vector shapes in Scalable Vector Graphics (SVG) format and printed '
			'on the standard output stream.'),
		epilog='Report bugs, request features, or provide suggestions via https://github.com/the-real-tokai/macuahuitl/issues',
		add_help=False,
	)

	g = ap.add_argument_group('Startup')
	g.add_argument('-V', '--version', action='version', version='%(prog)s {}'.format(__version__), help="show version number and exit")
	g.add_argument('-h', '--help', action='help', help='show this help message and exit')

	g = ap.add_argument_group('Algorithm')
	g.add_argument('--circles',      metavar='INT',    type=int,   help='number of concentric arc elements to generate inside the disc  [:21]', default=21)
	g.add_argument('--stroke-width', metavar='FLOAT',  type=float, help='width of the generated strokes  [:6]', default=6.0)
	g.add_argument('--gap',          metavar='FLOAT',  type=float, help='distance between the generated strokes')
	g.add_argument('--inner-radius', metavar='FLOAT',  type=float, help='setup inner disc radius to create an annular shape')
	g.add_argument('--hoffset',      metavar='FLOAT',  type=float, help='shift the whole disc horizontally  [:0.0]', default=0.0)
	g.add_argument('--voffset',      metavar='FLOAT',  type=float, help='shift the whole disc vertically  [:0.0]', default=0.0)
	g.add_argument('--colour',       metavar='COLOUR', type=str,   help='SVG compliant colour specification or identifier  [:black]', default='black')
	g.add_argument('--random-seed',  metavar='INT',    type=int,   help='fixed initialisation of the random number generator for predictable results')
	g.add_argument('--randomise',    action='store_true',          help='generate truly random disc layouts; values provided via other commandline parameters are utilised as limits')

	user_input = ap.parse_args()

	chaos   = random.Random(user_input.random_seed)
	circles = user_input.circles
	stroke  = abs(user_input.stroke_width) if user_input.stroke_width else 1.0
	gap     = user_input.gap if (user_input.gap is not None) else stroke
	radius  = abs(user_input.inner_radius) if (user_input.inner_radius is not None) else stroke
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


	arcs = []

	for _ in range(circles):
		arcs.append(SVGArcPathSegment(offset=chaos.uniform(0, 359), angle=chaos.uniform(1, 359), radius=radius, x=x, y=y))
		radius += (gap + stroke)

	vb_dim = radius + ((gap + stroke) * 2)  # Needs some extra space for the outline too.

	print('<svg width="100%" height="100%" viewBox="{o} {o} {s} {s}" xmlns="http://www.w3.org/2000/svg">'.format(o=(-vb_dim), s=(vb_dim * 2)),
		'<g id="comitl-disc">',
		'<path id="arcs" d="', ' '.join(map(str, arcs)), '" stroke="{}" stroke-width="{}" stroke-linecap="round" fill="none"/>'.format(colour, stroke),
		'<circle id="outline" cx="{}" cy="{}" r="{}" stroke="{}" stroke-width="{}" fill="none"/>'.format(x, y, radius, colour, stroke),
		'</g>',
		'</svg>', sep='', end='')


if __name__ == "__main__":
	main()
