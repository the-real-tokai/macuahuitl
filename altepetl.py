#!/usr/bin/env python3
"""
	Altepetl
	Implements an artful grid-based layout of "U"-shapes; inspired by some of
	generative art pioneer Véra Molnar's artworks.

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

	$Id: altepetl.py 132 2020-06-09 19:57:18Z tokai $
"""

import random
import argparse
import sys
import xml.etree.ElementTree as xtree

__author__  = 'Christian Rosentreter'
__version__ = '1.1'
__all__     = ['USquare']



class USquare():
	"""SVG description for a square 'U' shape, optionally rotated and/ or flipped."""

	dmod = {'n':['h', 'v', 1], 'e':['v', 'h', 1], 'w':['v', 'h', -1], 's':['h', 'v', -1]}

	def __init__(self, x, y, scale=1.0, direction='n', variation=0.0):
		self.x         = x
		self.y         = y
		self.scale     = scale
		self.direction = direction
		self.variation = variation

	def __str__(self):
		m  = self.dmod[self.direction]
		m2 = m[2] * self.scale
		v  = 0.18 * min(self.variation, 1.0)

		layout = [
			['M',  -0.5 * m2 + self.x],
			[' ',  -0.5 * m2 + self.y],
			[m[0],  (0.2 + v) * m2],
			[m[1],  0.8 * m2],
			[m[0],  (0.6 - v) * m2],
			[m[1], -0.8 * m2],
			[m[0],  0.2 * m2],
			[m[1],  1.0 * m2],
			[m[0], -1.0 * m2],
			['Z',  None]
		]

		return ''.join(l[0] + ('' if l[1] is None else str(l[1])) for l in layout)


def main():
	"""Let's make a work of art."""

	ap = argparse.ArgumentParser(
		description=('Implements an artful grid-based layout of "U"-shapes; inspired '
			'by some of generative art pioneer Véra Molnar\'s artworks.'),
		epilog='Report bugs, request features, or provide suggestions via https://github.com/the-real-tokai/macuahuitl/issues',
		add_help=False,
	)

	g = ap.add_argument_group('Startup')
	g.add_argument('-V', '--version',   action='version',               help="show version number and exit", version='%(prog)s {}'.format(__version__), )
	g.add_argument('-h', '--help',      action='help',                  help='show this help message and exit')

	g = ap.add_argument_group('Algorithm')
	g.add_argument('--columns',         metavar='INT',      type=int,   help='number of grid columns  [:11]', default=11)
	g.add_argument('--rows',            metavar='INT',      type=int,   help='number of grid rows  [:11]', default=11)
	g.add_argument('--scale',           metavar='FLOAT',    type=float, help='base scale factor of the grid elements [:10.0]', default=10.0)
	g.add_argument('--gap',             metavar='FLOAT',    type=float, help='non-random base gap between grid elements [:5.0]', default=5.0)
	g.add_argument('--shape-variation', metavar='FLOAT',    type=float, help='variation factor for the shape\'s inner "cut out" area  [:1.0]', default=1.0)
	g.add_argument('--offset-jiggle',   metavar='FLOAT',    type=float, help='randomizing factor for horizontal and vertical shifts of the element\'s coordinates  [:2.0]', default=2.0)
	g.add_argument('--random-seed',     metavar='INT',      type=int,   help='fixed initialization of the random number generator for predictable results')

	g = ap.add_argument_group('Miscellaneous')
	g.add_argument('--separate-paths',  action='store_true',            help='generate separate <path> elements for each element')
	g.add_argument('--negative',        action='store_true',            help='inverse the output colors')
	g.add_argument('--frame',           metavar='FLOAT',    type=float, help='extra spacing around the grid (additionally to potential gap spacing on the outside)  [:20.0]', default=20.0)

	g = ap.add_argument_group('Output')
	g.add_argument('-o', '--output',    metavar='FILENAME', type=str,   help='optionally rasterize the generated vector paths and write the result into a PNG file (requires the `svgcairo\' Python module)')
	g.add_argument('--output-size',     metavar='INT',      type=int,   help='force pixel width of the raster image, height is automatically calculated; if omitted the generated SVG viewbox dimensions are used')

	user_input  = ap.parse_args()


	grid_x      = user_input.columns
	grid_y      = user_input.rows
	grid_size   = user_input.scale
	grid_gap    = user_input.gap
	variation   = user_input.shape_variation
	jiggle      = user_input.offset_jiggle
	frame       = user_input.frame

	chaos       = random.Random(user_input.random_seed)
	grid_offset = grid_size + grid_gap
	col1, col2  = 'white', 'black'
	if user_input.negative:
		col1, col2 = col2, col1

	squares = []
	for x in range(0, grid_x):
		for y in range(0, grid_y):
			dx = (x * grid_offset) + (grid_offset / 2.0) + frame + chaos.uniform(-jiggle, jiggle)
			dy = (y * grid_offset) + (grid_offset / 2.0) + frame + chaos.uniform(-jiggle, jiggle)
			squares.append(USquare(dx, dy, grid_size, chaos.choice('nwes'), chaos.uniform(0.0, variation)))

	vbw = int((grid_offset * grid_x) + (frame * 2.0))
	vbh = int((grid_offset * grid_y) + (frame * 2.0))

	svg = xtree.Element('svg', {'width':'100%', 'height':'100%', 'xmlns':'http://www.w3.org/2000/svg', 'viewBox':'0 0 {} {}'.format(vbw, vbh)})
	title = xtree.SubElement(svg, 'title')
	title.text = 'An Altepetl Artwork'

	xtree.SubElement(svg, 'rect', {'id':'background', 'x':'0', 'y':'0', 'width':str(vbw), 'height':str(vbh), 'fill':col1})
	if user_input.separate_paths:
		svg_g = xtree.SubElement(svg, 'g', {'id':'grid-of-us', 'stroke-width':'0', 'fill':col2})
		for si, s in enumerate(squares):
			xtree.SubElement(svg_g, 'path', {'id':'element-{}'.format(si), 'd':str(s)})
	else:
		xtree.SubElement(svg, 'path', {'id':'grid-of-us', 'stroke-width':'0', 'fill':col2, 'd':''.join(str(s) for s in squares)})

	rawxml = xtree.tostring(svg, encoding='unicode')

	if not user_input.output:
		print(rawxml)
	else:
		try:
			import os
			from cairosvg import svg2png
			svg2png(bytestring=rawxml,
				write_to=os.path.realpath(os.path.expanduser(user_input.output)),
				output_width=user_input.output_size,
				output_height=int(user_input.output_size * vbh / vbw)
			)
		except ImportError as e:
			print('Couldn\'t rasterize nor write a PNG file. Required Python module \'cairosvg\' is not available: {}'.format(str(e)), file=sys.stderr)


if __name__ == '__main__':
	main()
