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

	$Id: temo.py 162 2020-07-04 14:23:33Z tokai $
"""

import random
import argparse
import sys
import colorsys
import logging
from enum import Enum
import xml.etree.ElementTree as xtree

__author__  = 'Christian Rosentreter'
__version__ = '1.2'
__all__     = []



class Direction(Enum):
	"""<insert description>"""
	NORTH = 1
	SOUTH = 2
	EAST  = 3
	WEST  = 4


class Slope(Enum):
	"""<insert description>"""
	UP    = 0  # "/"
	DOWN  = 1  # "\"



class DLine():
	"""A diagonal line segment inside a square."""

	def __init__(self, slope, hue, x1, y1, x2, y2):
		self.slope = slope
		self.hue   = hue
		self.x1    = x1 if (slope == Slope.DOWN) else x2
		self.x2    = x2 if (slope == Slope.DOWN) else x1
		self.y1    = y1
		self.y2    = y2

	def __repr__(self):
		return '\\' if (self.slope == Slope.DOWN) else '/'


def hue_blend(a, b):
	"""Blends two angular hue values with linear interpolation."""
	if a > b:
		a, b = b, a
	d = b - a
	if d > 180:
		a += 360
		return (a + ((b - a) / 2.0)) % 360
	return a + (d / 2.0)


def lookup_hue(slope, x, y, rows, hue_shift_line):
	"""Looks up a hue value or a pair of hue values from the already generated grid elements."""
	hues = []
	if y:
		if slope == Slope.DOWN:
			if x and (rows[y-1][x-1].slope == Slope.DOWN):
				hues.append(rows[y-1][x-1].hue)
			if rows[y-1][x].slope == Slope.UP:
				hues.append(rows[y-1][x].hue)
		else:  # slope == Slope.UP
			if rows[y-1][x].slope == Slope.DOWN:
				hues.append(rows[y-1][x].hue)
			if (x < len(rows[y-1]) - 1) and (rows[y-1][x+1].slope == Slope.UP):
				hues.append(rows[y-1][x+1].hue)
	if hues:
		if len(hues) == 2:
			return hue_blend(hues[0], hues[1])
		return (hues[0] + hue_shift_line) % 360
	return None


def hls_to_hex(hue, lightness, saturation):
	"""Converts a HLS color triplet into a SVG hex string."""
	return '#{:02x}{:02x}{:02x}'.format(*(int(c*255) for c in list(colorsys.hls_to_rgb(hue / 360, lightness, saturation))))



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
	g.add_argument('--hue-shift-line',   metavar='FLOAT',    type=float, help='separate hue shift for continuous lines; if not passed `--hue-shift\' applies too')
	g.add_argument('--best-path-width',  metavar='FLOAT',    type=float, help='show the best (aka the longest) path through the maze and set width of its marker line')

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
	huesl      = user_input.hue_shift if user_input.hue_shift_line is None else user_input.hue_shift_line

	for y in range(0, user_input.rows):
		# master_hue = (360 / user_input.rows * y) % 360
		rows.append([])
		for x in range(0, user_input.columns):
			slope = chaos.choice([Slope.UP, Slope.DOWN])
			hue   = lookup_hue(slope, x, y, rows, huesl)
			if hue is None:
				hue = master_hue
				master_hue = (master_hue + user_input.hue_shift) % 360
			rows[y].append(DLine(slope, hue, (x * scale + frame), (y * scale + frame), (x * scale + scale + frame), (y * scale + scale + frame)))

	# Primitive path walking…
	#
	bestwalker = None
	circle_pos = None

	if user_input.best_path_width:
		coords = []
		for x in range(0, user_input.columns):
			coords.append((x, -1, Direction.SOUTH))
			coords.append((x, user_input.rows, Direction.NORTH))
		for y in range(0, user_input.rows):
			coords.append((-1, y, Direction.EAST))
			coords.append((user_input.columns, y, Direction.WEST))
		chaos.shuffle(coords)

		offset = scale / 2.0

		for pos in coords:
			wx, wy, wd = pos
			cx = (wx * scale) + frame + offset
			cy = (wy * scale) + frame + offset
			tempwalker = ['M{} {}{}{}'.format(cx, cy,
				'v' if wd in (Direction.SOUTH, Direction.NORTH) else 'h',
				offset if wd in (Direction.SOUTH, Direction.EAST) else -offset
			)]
			tx, ty = 1, 1

			while True:
				if wd == Direction.SOUTH:
					wy += 1
					if wy >= user_input.rows:
						break
					wd, tx, ty = (Direction.EAST, 1, 1) if (rows[wy][wx].slope == Slope.DOWN) else (Direction.WEST, -1, 1)
				elif wd == Direction.WEST:
					wx -= 1
					if wx < 0:
						break
					wd, tx, ty = (Direction.NORTH, -1, -1) if (rows[wy][wx].slope == Slope.DOWN) else (Direction.SOUTH, -1, 1)
				elif wd == Direction.EAST:
					wx += 1
					if wx >= user_input.columns:
						break
					wd, tx, ty = (Direction.SOUTH, 1, 1) if (rows[wy][wx].slope == Slope.DOWN) else (Direction.NORTH, 1, -1)
				else:  # wd == Direction.NORTH
					wy -= 1
					if wy < 0:
						break
					wd, tx, ty = (Direction.WEST, -1, -1) if (rows[wy][wx].slope == Slope.DOWN) else (Direction.EAST, 1, -1)

				tempwalker.append('l{} {}'.format((offset * tx), (offset * ty)))
				logging.debug('New position <%u×%u>, direction <%s>', wx, wy, wd)

			logging.debug(tempwalker)
			if bestwalker is None or len(tempwalker) > len(bestwalker):
				bestwalker = tempwalker.copy()
				circle_pos = (cx, cy)

	# Generate SVG…
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
				'id':     'line-{}x{}'.format(col_id + 1, row_id + 1),
				'x1':     str(element.x1),
				'y1':     str(element.y1),
				'x2':     str(element.x2),
				'y2':     str(element.y2),
				'stroke': hls_to_hex(element.hue, 0.6, 0.5),
			})

	if bestwalker:
		svg_g  = xtree.SubElement(svg, 'g', {'id':'best_walker'})
		wcolor = hls_to_hex(chaos.uniform(0, 360), 0.5, 0.8)
		xtree.SubElement(svg_g, 'path', {
			'd':               ''.join(bestwalker),
			'stroke-width':    str(user_input.best_path_width),
			'stroke':          wcolor,
			'stroke-linecap':  'round',
			'stroke-linejoin': 'round',
			'fill':            'none',
		})
		xtree.SubElement(svg_g, 'circle', {
			'id':   'start_point',
			'cx':   str(circle_pos[0]),
			'cy':   str(circle_pos[1]),
			'r':    str(user_input.best_path_width),
			'fill': wcolor,
		})

	rawxml = xtree.tostring(svg, encoding='unicode')

	# Output…
	#
	if not user_input.output:
		print(rawxml)
	else:
		try:
			import os
			from cairosvg import svg2png
			svg2png(
				bytestring    = rawxml,
				write_to      = os.path.realpath(os.path.expanduser(user_input.output)),
				output_width  = user_input.output_size,
				output_height = int(user_input.output_size * vbh / vbw) if user_input.output_size is not None else None
			)
		except ImportError as e:
			print('Couldn\'t rasterize nor write a PNG file. Required Python module \'cairosvg\' is not available: {}'.format(str(e)), file=sys.stderr)


if __name__ == '__main__':
	main()
