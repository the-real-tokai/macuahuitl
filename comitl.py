#!/usr/bin/env python3
"""
	Comitl
	Concentrically arranges randomly sized arcs into a pretty disc shape.

	Copyright © 2020 Christian Rosentreter

	This program is free software: you can redistribute it and/or modify
	it under the terms of the GNU Affero General Public License as published
	by the Free Software Foundation, either version 3 of the License, or
	(at your option) any later version.

	This program is distributed in the hope that it will be useful,
	but WITHOUT ANY WARRANTY; without even the implied warranty of
	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
	GNU Affero General Public License for more details.

	You should have received a copy of the GNU Affero General Public License
	along with this program.  If not, see <https://www.gnu.org/licenses/>.

	$Id: comitl.py 92 2020-05-21 21:15:18Z tokai $
"""

import math
import random
import argparse
import sys
import os
import xml.etree.ElementTree as xtree


__author__  = 'Christian Rosentreter'
__version__ = '1.5'
__all__     = ['SVGArcPathSegment']



class SVGArcPathSegment():
	"""An 'arc' SVG path segment."""

	def __init__(self, offset=0.0, angle=90.0, radius=1.0, x=0.0, y=0.0):
		if abs(angle) >= 360:
			raise ValueError('angles of SVG arc path segments must be smaller than 360°')
		self.offset = offset
		self.angle  = angle
		self.radius = radius
		self.x      = x
		self.y      = y

	def __str__(self):
		if self.angle == 0:
			return ''

		ts = (self.offset - 180.0) * math.pi / -180.0
		td = (self.offset + self.angle - 180.0) * math.pi / -180.0

		return 'M {sx} {sy} A {r} {r} 0 {f} 1 {dx} {dy}'.format(
			sx=round(self.x + self.radius * math.sin(ts), 9),
			sy=round(self.y + self.radius * math.cos(ts), 9),
			r=round(self.radius, 9),
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
	g.add_argument('--circles',          metavar='INT',      type=int,   help='number of concentric arc elements to generate inside the disc  [:21]', default=21)
	g.add_argument('--stroke-width',     metavar='FLOAT',    type=float, help='width of the generated strokes  [:6]', default=6.0)
	g.add_argument('--gap',              metavar='FLOAT',    type=float, help='distance between the generated strokes')
	g.add_argument('--inner-radius',     metavar='FLOAT',    type=float, help='setup inner disc radius to create an annular shape')
	g.add_argument('--hoffset',          metavar='FLOAT',    type=float, help='shift the whole disc horizontally  [:0.0]', default=0.0)
	g.add_argument('--voffset',          metavar='FLOAT',    type=float, help='shift the whole disc vertically  [:0.0]', default=0.0)
	g.add_argument('--color',            metavar='COLOR',    type=str,   help='SVG compliant color specification or identifier  [:black]', default='black')
	g.add_argument('--random-seed',      metavar='INT',      type=int,   help='fixed initialization of the random number generator for predictable results')
	g.add_argument('--randomize',        action='store_true',            help='generate truly random disc layouts; other algorithm values provided via command line parameters are utilized as limits')

	g = ap.add_argument_group('Miscellaneous')
	g.add_argument('--separate-paths',   action='store_true',            help='generate separate <path> elements for each arc')
	g.add_argument('--outline-mode',     choices=['both', 'outside', 'inside', 'none'], help='generate bounding outline circles  [:both]', default='both')
	g.add_argument('--background-color', metavar='COLOR',    type=str,   help='SVG compliant color specification or identifier; adds a background <rect> to the SVG output')
	g.add_argument('--disc-color',       metavar='COLOR',    type=str,   help='SVG compliant color specification or identifier; fills the background of the generated disc by adding an extra <circle> element')

	g = ap.add_argument_group('Output')
	g.add_argument('-o', '--output',     metavar='FILENAME', type=str,   help='optionally rasterize the generated vector paths and write the result into a PNG file (requires the `svgcairo\' Python module)')
	g.add_argument('--output-size',      metavar='INT',      type=int,   help='force pixel width and height of the raster image; if omitted the generated SVG viewbox dimensions are used')

	user_input = ap.parse_args()


	#  Initialize…
	#
	chaos   = random.Random(user_input.random_seed)
	circles = user_input.circles
	stroke  = abs(user_input.stroke_width) if user_input.stroke_width else 1.0
	gap     = user_input.gap if (user_input.gap is not None) else stroke
	radius  = abs(user_input.inner_radius) if (user_input.inner_radius is not None) else stroke
	x       = user_input.hoffset
	y       = user_input.voffset
	color   = user_input.color

	if user_input.randomize:
		circles = chaos.randrange(0, circles) if circles else 0
		stroke  = chaos.uniform(0, stroke)
		stroke  = 1.0 if stroke == 0 else stroke
		gap     = chaos.uniform(0, gap)
		radius  = chaos.uniform(0, radius)
		x       = chaos.uniform(-x, x) if x else 0.0
		y       = chaos.uniform(-y, y) if y else 0.0
		color   = '#{:02x}{:02x}{:02x}'.format(chaos.randrange(0, 255), chaos.randrange(0, 255), chaos.randrange(0, 255))
		# TODO: randomize background and disc color too when the respective parameters are used
		#       (needs to respect color harmonies)

	if radius < stroke:
		radius = stroke


	#  Generate data…
	#
	outlines = []
	arcs = []

	if user_input.outline_mode in ('both', 'inside'):
		outlines.append({'x':x, 'y':y, 'r':radius})
		radius += (gap + stroke)

	for _ in range(circles):
		# Calculate angular space requirement for the "round" stroke caps to avoid some overlapping
		sqrd2 = 2.0 * math.pow(radius, 2.0)
		theta = ((2.0 * math.acos((sqrd2 - math.pow((stroke / 2.0), 2.0)) / sqrd2)) * (180.0 / math.pi))

		arcs.append(SVGArcPathSegment(offset=chaos.uniform(0, 359.0), angle=chaos.uniform(0, 359.0 - theta), radius=radius, x=x, y=y))
		radius += (gap + stroke)

	if user_input.outline_mode in ('both', 'outside'):
		outlines.append({'x':x, 'y':y, 'r':radius})
	else:
		radius -= (gap + stroke)


	#  Generate SVG/XML…
	#
	def _f(v, max_digits=9):
		if isinstance(v, float):
			v = round(v, max_digits)
		return v if isinstance(v, str) else str(v)

	vb_dim  = (radius + (stroke * 0.5)) * (256.0 / (256.0 - 37.35)) # 37px border for 256x256; a golden ratio in there… somewhere…
	vb_off  = _f(vb_dim * -1.0, 2)
	vb_dim  = _f(vb_dim *  2.0, 2)
	config  = {'stroke':color, 'stroke-width':_f(stroke), 'fill':'none'}

	svg = xtree.Element('svg', {'width':'100%', 'height':'100%', 'xmlns':'http://www.w3.org/2000/svg', 'viewBox':'{o} {o} {s} {s}'.format(o=vb_off, s=vb_dim)})

	if user_input.background_color:
		xtree.SubElement(svg, 'rect', {'id':'background', 'x':vb_off, 'y':vb_off, 'width':vb_dim, 'height':vb_dim, 'fill':user_input.background_color})

	svg_m = xtree.SubElement(svg, 'g', {'id':'comitl-disc'})

	if user_input.disc_color:
		xtree.SubElement(svg_m, 'circle', {'id':'disc-background', 'cx':_f(x), 'cy':_f(y), 'r':_f(radius), 'fill':user_input.disc_color})

	if arcs:
		if user_input.separate_paths:
			svg_ga = xtree.SubElement(svg_m, 'g', {'id':'arcs'})
			for aid, a in enumerate(arcs):
				xtree.SubElement(svg_ga, 'path', {'id':'arc-{}'.format(aid+1), 'd':str(a), 'stroke-linecap':'round', **config})
		else:
			xtree.SubElement(svg_m, 'path', {'id':'arcs', 'd':''.join(map(str, arcs)), 'stroke-linecap':'round', **config})

	if outlines:
		svg_go = xtree.SubElement(svg_m, 'g', {'id':'outlines'})
		for oid, o in enumerate(outlines):
			xtree.SubElement(svg_go, 'circle', {'id':'outline-{}'.format(oid+1), 'cx':_f(o['x']), 'cy':_f(o['y']), 'r':_f(o['r']), **config})

	rawxml = xtree.tostring(svg, encoding='unicode')


	#  Send happy little arcs out into the world…
	#
	if not user_input.output:
		print(rawxml)
	else:
		try:
			from cairosvg import svg2png
			svg2png(bytestring=rawxml,
				write_to=os.path.realpath(os.path.expanduser(user_input.output)),
				output_width=user_input.output_size,
				output_height=user_input.output_size
			)
		except ImportError as e:
			print('Couldn\'t rasterize nor write a PNG file. Required Python module \'cairosvg\' is not available: {}'.format(str(e)), file=sys.stderr)


if __name__ == "__main__":
	main()
