#!/usr/bin/env python3
"""
	Temo
	Creates a colorful maze inspired by a famous one line C64 BASIC
	program.

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

	$Id: temo.py 146 2020-06-19 14:15:06Z tokai $
"""

import random
import argparse
import sys
import colorsys
import xml.etree.ElementTree as xtree

__author__  = 'Christian Rosentreter'
__version__ = '1.1'
__all__     = []


class DLine():
	"""A diagonal line segment inside a square."""

	def __init__(self, direction, hue, x1, y1, x2, y2):
		# direction = 1 -> "\"
		# direction = 0 -> "/"
		self.direction = direction
		self.hue       = hue
		self.x1        = x1 if direction else x2
		self.x2        = x2 if direction else x1
		self.y1        = y1
		self.y2        = y2

	def __repr__(self):
		return '\\' if self.direction else '/'


def hue_blend(a, b):
	"""Blends two angular hue values with linear interpolation."""
	if a > b:
		a, b = b, a
	d = b - a
	if d > 180:
		a += 360
		return (a + ((b - a) / 2.0)) % 360
	return a + (d / 2.0)


def lookup_hue(direction, x, y, rows):
	"""Looks up a hue value or a pair of hue values from the already generated grid elements."""
	hues = []
	if y:
		if direction: # "\"
			if x and rows[y-1][x-1].direction:
				hues.append(rows[y-1][x-1].hue)
			if rows[y-1][x].direction == 0:
				hues.append(rows[y-1][x].hue)
		else:  # direction = "/"
			if rows[y-1][x].direction:
				hues.append(rows[y-1][x].hue)
			if (x < len(rows[y-1]) - 1) and (rows[y-1][x+1].direction == 0):
				hues.append(rows[y-1][x+1].hue)
	if hues:
		if len(hues) == 2:
			return hue_blend(hues[0], hues[1])
		return (hues[0] + 15.0) % 360
	return None


def main():
	"""It's not just a single line of code, but what can we do? :)"""

	ap = argparse.ArgumentParser(
		description=('Creates a colorful maze inspired by a famous one line C64 BASIC program '
			'(`10 PRINT CHR$(205.5+RND(1)); : GOTO 10\'). Output is generated as a set of vector '
			'shapes in Scalable Vector Graphics (SVG) format and printed on the standard output '
			'stream.'),
		epilog='Report bugs, request features, or provide suggestions via https://github.com/the-real-tokai/macuahuitl/issues',
		add_help=False,
	)

	g = ap.add_argument_group('Startup')
	g.add_argument('-V', '--version',   action='version',               help="show version number and exit", version='%(prog)s {}'.format(__version__), )
	g.add_argument('-h', '--help',      action='help',                  help='show this help message and exit')

	g = ap.add_argument_group('Algorithm')
	g.add_argument('--columns',         metavar='INT',      type=int,   help='number of grid columns  [:11]', default=40)
	g.add_argument('--rows',            metavar='INT',      type=int,   help='number of grid rows  [:11]', default=30)
	g.add_argument('--scale',           metavar='FLOAT',    type=float, help='base scale factor of the grid elements [:10.0]', default=10.0)
	g.add_argument('--random-seed',     metavar='INT',      type=int,   help='fixed initialization of the random number generator for predictable results')

	g = ap.add_argument_group('Miscellaneous')
	g.add_argument('--frame',            metavar='FLOAT',    type=float, help='increase or decrease spacing around the maze  [:20.0]', default=20.0)
	g.add_argument('--stroke-width',     metavar='FLOAT',    type=float, help='width of the generated strokes  [:2.0]', default=2.0)
	g.add_argument('--background-color', metavar='COLOR',    type=str,   help='SVG compliant color specification or identifier; adds a background <rect> to the SVG output')
	g.add_argument('--hue-shift',        metavar='FLOAT',    type=float, help='amount to rotate an imaginary color wheel before looking up new colors (in degrees)  [:15.0]', default=15.0)

	g = ap.add_argument_group('Output')
	g.add_argument('-o', '--output',    metavar='FILENAME', type=str,   help='optionally rasterize the generated vector paths and write the result into a PNG file (requires the `svgcairo\' Python module)')
	g.add_argument('--output-size',     metavar='INT',      type=int,   help='force pixel width of the raster image, height is automatically calculated; if omitted the generated SVG viewbox dimensions are used')

	user_input = ap.parse_args()

	# Generate data…
	#
	chaos      = random.Random(user_input.random_seed)
	scale      = user_input.scale
	frame      = user_input.frame
	rows       = []
	master_hue = chaos.uniform(0,360)

	for y in range(0, user_input.rows):
		# master_hue = (360 / user_input.rows * y) % 360
		rows.append([])
		for x in range(0, user_input.columns):
			direction = chaos.choice([0, 1])
			hue       = lookup_hue(direction, x, y, rows)
			if hue is None:
				hue = master_hue
				master_hue = (master_hue + user_input.hue_shift) % 360
			rows[y].append(DLine(direction, hue, (x * scale + frame), (y * scale + frame), (x * scale + scale + frame), (y * scale + scale + frame)))

	# Output…
	#
	vbw = int((scale * user_input.columns) + (frame * 2.0))
	vbh = int((scale * user_input.rows   ) + (frame * 2.0))

	svg = xtree.Element('svg', {'width':'100%', 'height':'100%', 'xmlns':'http://www.w3.org/2000/svg', 'viewBox':'0 0 {} {}'.format(vbw, vbh)})
	title = xtree.SubElement(svg, 'title')
	title.text = 'A Temo Artwork'

	if user_input.background_color:
		xtree.SubElement(svg, 'rect', {'id':'background', 'x':'0', 'y':'0', 'width':str(vbw), 'height':str(vbh), 'fill':user_input.background_color})
	svg_g = xtree.SubElement(svg, 'g', {'id':'goto10', 'stroke-width':str(user_input.stroke_width), 'stroke-linecap':'round'})

	for row_id, row in enumerate(rows):
		for col_id, element in enumerate(row):
			xtree.SubElement(svg_g, 'line', {
				'id':'line-{}x{}'.format(col_id + 1, row_id + 1),
				'x1':str(element.x1),
				'y1':str(element.y1),
				'x2':str(element.x2),
				'y2':str(element.y2),
				'stroke':'#{:02x}{:02x}{:02x}'.format(*(int(c*255) for c in list(colorsys.hls_to_rgb(element.hue / 360, 0.6, 0.5)))),
			})

	rawxml = xtree.tostring(svg, encoding='unicode')

	if not user_input.output:
		print(rawxml)
	else:
		try:
			import os
			from cairosvg import svg2png

			w = vbw if user_input.output_size is None else user_input.output_size

			svg2png(bytestring=rawxml,
				write_to=os.path.realpath(os.path.expanduser(user_input.output)),
				output_width=w,
				output_height=int(w * vbh / vbw)
			)
		except ImportError as e:
			print('Couldn\'t rasterize nor write a PNG file. Required Python module \'cairosvg\' is not available: {}'.format(str(e)), file=sys.stderr)


if __name__ == '__main__':
	main()
