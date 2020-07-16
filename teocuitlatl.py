#!/usr/bin/env python3
"""
	Teocuitlatl
	Creates a grid of colored squares that are accentuated with smaller squares
	or discs

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

	$Id: teocuitlatl.py 166 2020-07-16 20:39:42Z tokai $
"""

import random
import argparse
import sys
import xml.etree.ElementTree as xtree
from collections import Counter

__author__  = 'Christian Rosentreter'
__version__ = '1.4'
__all__     = []



def triangular_stronger_bias(chaos, low, high, bias, iterations):
	"""Returns random values with a very strong bias."""
	candidates = [int(chaos.triangular(low, high, bias)) for _ in range(iterations)]
	result_set = Counter(candidates).most_common(1)
	return chaos.choice(result_set)[0]


def color_to_hex(color):
	"""Converts a color tuple (r,g,b) into a SVG compatible hexadecimal color descriptor."""
	return '#{:02x}{:02x}{:02x}'.format(*color)


def float_to_svg(v):
	"""Tries to generate smallest string representation of the supplied float value."""
	return '{:g}'.format(round(v, 10))



def main():
	"""Yet another grid generator… and it probably won't be the last one either. :) """

	palettes = {
		'shadowplay': [   # Bridget Riley: "Shadowplay"
			( 61,  85, 119),
			( 48, 102, 208),
			(  0, 141, 184),
			(112, 179, 113),
			(232,  98, 131),
			(112, 169, 236),
			(162, 124, 171),
			(197, 141, 211),
			(255, 164,  82),
			(248, 221, 143),
			(255, 224, 230),
		],
		'spectrum9': [   # Ellsworth Kelly: "Spectrum Ⅸ"
			(238, 225,  58),
			(143, 220,  67),
			(104, 209, 120),
			( 42, 176, 186),
			( 48, 138, 214),
			( 97, 114, 197),
			(116,  95, 166),
			(138, 102, 152),
			(206, 105, 120),
			(241, 103 , 98),
			(250, 139,   0),
			(250, 196,  64),
		],
		'binary': [
			(  0,   0,   0),
			(255, 255, 255),
		],
		'greyscale': [
			(   0,    0,    0),
			(0x11, 0x11, 0x11),
			(0x22, 0x22, 0x22),
			(0x33, 0x33, 0x33),
			(0x44, 0x44, 0x44),
			(0x55, 0x55, 0x55),
			(0x66, 0x66, 0x66),
			(0x77, 0x77, 0x77),
			(0x88, 0x88, 0x88),
			(0x99, 0x99, 0x99),
			(0xAA, 0xAA, 0xAA),
			(0xBB, 0xBB, 0xBB),
			(0xCC, 0xCC, 0xCC),
			(0xDD, 0xDD, 0xDD),
			( 255,  255,  255),
		],
		'rgb': [
			(255,   0,   0),
			(  0, 255,   0),
			(  0,   0, 255),
		],
		'yell': [  # Unknown Artist: "Yell" (NHK asadora) marketing
			(0x00, 0x00, 0x00),
			(0x05, 0xae, 0xb0),
			(0xeb, 0x55, 0x75),
			(0xef, 0xba, 0x1f),
			(0xff, 0xff, 0xff),
		],
		'owinja': [  # Carla Thompson: "Turquoise & Orange Star Quilt"
			(195, 216, 227),
			(148, 209, 225),
			(  0, 141, 171),
			(162,  37,  23),
			(231, 105,  83),
			(252, 117,  21),	
		],
		'folklore': [  # Victor Vasarely: "Planetary Folklore Participations N° 1" (selection)
			(187, 248, 249),
			(252, 252,   4),
			(105, 222, 249),
			(252, 207,  10),
			(250, 126, 250),
			( 35, 249,  66),
			(  4, 159, 242),
			(251, 117,  13),
			( 15, 114, 214),
			(  6, 187,  82),
			(252,  62,   4),
			( 36, 112, 178),
			(206,  76, 113),
			(105,  58, 162),
			( 10, 131,  51),
			(135,  27,  65),
			( 57,  34, 114),
			( 17,  33,  13),
		],
		# TODO: implement "original" special selection mode (separate array)
	}


	ap = argparse.ArgumentParser(
		description=('Creates a grid of colored squares that are accentuated with smaller squares '
			'or discs. Output is generated as a set of vector shapes in Scalable Vector Graphics (SVG) '
			'format and printed on the standard output stream.'),
		epilog='Report bugs, request features, or provide suggestions via https://github.com/the-real-tokai/macuahuitl/issues',
		add_help=False,
	)

	g = ap.add_argument_group('Startup')
	g.add_argument('-V', '--version',      action='version',               help="show version number and exit", version='%(prog)s {}'.format(__version__), )
	g.add_argument('-h', '--help',         action='help',                  help='show this help message and exit')

	g = ap.add_argument_group('Algorithm')
	g.add_argument('--columns',            metavar='INT',      type=int,   help='number of grid columns  [:11]', default=10)
	g.add_argument('--rows',               metavar='INT',      type=int,   help='number of grid rows  [:11]', default=10)
	g.add_argument('--no-inset',           action='store_true',            help='disable the default accent shape inset')
	g.add_argument('--inset-offset',       metavar='INT',      type=int,   help='manually force amount of frame tiles around the inset, else it\'s automatically calculated')
	g.add_argument('--no-horizontal-flip', action='store_true',            help='disable the default horizontal accent shape flip')
	g.add_argument('--no-vertical-flip',   action='store_true',            help='disable the default vertical accent shape flip')
	g.add_argument('--color-bias',         metavar='INT',      type=int,   help='increase amount of directional bias when choosing random colors  [:1]', default=1)
	g.add_argument('--scale',              metavar='INT',      type=int,   help='base scale factor of the grid elements  [:74.0]', default=74.0)
	g.add_argument('--padding',            metavar='FLOAT',    type=float, help='manually force inner padding to control the frame around the accent shapes')
	g.add_argument('--palette',            choices=list(palettes.keys()),  help='choose random colors from the specified color scheme  [:default]', default='folklore')
	g.add_argument('--random-seed',        metavar='INT',      type=int,   help='fixed initialization of the random number generator for predictable results')
	g.add_argument('--randomize',          action='store_true',            help='generate truly random layouts; other algorithm values provided via command line parameters are utilized as limits')

	g = ap.add_argument_group('Output')
	g.add_argument('-o', '--output',       metavar='FILENAME', type=str,   help='optionally rasterize the generated vector paths and write the result into a PNG file (requires the `svgcairo\' Python module)')
	g.add_argument('--output-size',        metavar='INT',      type=int,   help='force pixel width of the raster image, height is automatically calculated; if omitted the generated SVG viewbox dimensions are used')

	user_input = ap.parse_args()


	# Generate data/ SVG…
	#
	chaos      = random.Random(user_input.random_seed)

	tile_size  = max(1, user_input.scale)
	tiles_x    = max(1, user_input.columns)
	tiles_y    = max(1, user_input.rows)
	tiles_ioff = user_input.inset_offset if user_input.inset_offset is not None else int(min(tiles_x, tiles_y)/2.0/2.0)
	tile_frame = user_input.padding if user_input.padding is not None else round(0.14 * tile_size, 2)
	palette    = palettes[user_input.palette] # if chaos.uniform(0, 1) < 0.5 else list(reversed(palettes[user_input.palette]))
	color_iter = max(1, user_input.color_bias)
	flip_x     = False if user_input.no_horizontal_flip else True
	flip_y     = False if user_input.no_vertical_flip else True
	inset      = False if user_input.no_inset else True

	if user_input.randomize:
		tile_size  = chaos.randrange(0, tile_size) + 1
		tiles_x    = chaos.randrange(0, tiles_x) + 1
		# TODO: we get a lot of silly pictures here; use some sane limits for now
		#       tyles_y = chaos.randrange(0, tiles_y) + 1
		if tiles_x % 2:
			tiles_x += 1
		tiles_y    = tiles_x
		#
		tiles_ioff = chaos.randrange(0, tiles_ioff + 1)
		tile_frame = chaos.uniform(0, tile_frame)
		palette    = palettes[chaos.choice(list(palettes.keys()))]
		color_iter = int(max(1.0, triangular_stronger_bias(chaos, 0, color_iter, 0, 10)))
		flip_x     = chaos.choice([0, 1])
		flip_y     = chaos.choice([0, 1])
		inset      = chaos.choice([0, 1])

	if chaos.uniform(0, 1) < 0.5:
		palette.reverse()

	stile_size = tile_size - tile_frame - tile_frame
	stile_rad  = stile_size / 2.0
	vbw        = int(tile_size * tiles_x)
	vbh        = int(tile_size * tiles_y)
	colors     = len(palette)

	svg = xtree.Element('svg', {'width':'100%', 'height':'100%', 'xmlns':'http://www.w3.org/2000/svg', 'viewBox':'0 0 {} {}'.format(vbw, vbh)})
	title = xtree.SubElement(svg, 'title')
	title.text = 'A Teocuitlatl Artwork'

	tile_backgrounds = []
	init_shape = chaos.choice([0, 1])  # 1 == square, 2 == circle

	for y in range(0, tiles_y):
		for x in range(0, tiles_x):

			#  Select inner shape
			shape = init_shape
			bias  = x / tiles_x * colors
			if inset and (tiles_ioff <= x < (tiles_x - tiles_ioff)) and (tiles_ioff <= y < (tiles_y - tiles_ioff)):
				shape = 1 - shape  # swap
				bias  = colors - bias
				# TODO: reversing the bias direction should also change/ map the range and
				#       take 'tiles_ioff' into account (so the inset uses the full range of
				#       available colors), maybe something like this:
				#       "colors - (x+tiles_ioff / tiles_x-tiles_ioff*2  * colors)" ?
			if flip_y and (y >= (tiles_y / 2)):
				shape = 1 - shape  # swap
			if flip_x and (x >= (tiles_x / 2)):
				shape = 1 - shape  # swap

			#  Fetch background color
			loop_cnt = 0
			while loop_cnt < 100:
				loop_cnt += 1
				tile_color_bg = triangular_stronger_bias(chaos, 0, colors, bias, color_iter)
				if (x > 0) and (tile_color_bg is tile_backgrounds[-1]):       # one to the left
					continue
				if (y > 0) and (tile_color_bg is tile_backgrounds[-tiles_x]): # one to the top
					continue
				break
			else:
				print('Warning: Couldn\'t get a non-colliding tile background color for tile "{}×{}", because the color bias is too high for the amount of available colors.'.format(x, y), file=sys.stderr)
			tile_backgrounds.append(tile_color_bg)

			#  Fetch foreground color
			loop_cnt = 0
			while loop_cnt < 100:
				loop_cnt += 1
				tile_color_shape = triangular_stronger_bias(chaos, 0, colors, bias, color_iter)
				if tile_color_shape is not tile_color_bg:
					break
			else:
				print('Warning: Couldn\'t get a non-colliding accent shape color for tile "{}×{}", because the color bias is too high for the amount of available colors.'.format(x, y), file=sys.stderr)

			#  Output the tile
			svg_tile_group = xtree.SubElement(svg, 'g', {'id': 'tile_{}x{}'.format(x+1, y+1)})

			xtree.SubElement(svg_tile_group, 'rect', {
				'x':      float_to_svg(x * tile_size),
				'y':      float_to_svg(y * tile_size),
				# Note: overlap to avoid potential hairlines between the tiles in some SVG renderers
				'width':  float_to_svg(tile_size * (2 if ((x + 1) < tiles_x) else 1)),
				'height': float_to_svg(tile_size * (2 if ((y + 1) < tiles_y) else 1)),
				'fill':   color_to_hex(palette[tile_color_bg])
			})

			if shape == 0:
				xtree.SubElement(svg_tile_group, 'rect', {
					'x':      float_to_svg((x * tile_size) + tile_frame),
					'y':      float_to_svg((y * tile_size) + tile_frame),
					'width':  float_to_svg(stile_size),
					'height': float_to_svg(stile_size),
					'fill':   color_to_hex(palette[tile_color_shape])
				})
			else:
				xtree.SubElement(svg_tile_group, 'circle', {
					'cx':     float_to_svg((x * tile_size) + (tile_size / 2)),
					'cy':     float_to_svg((y * tile_size) + (tile_size / 2)),
					'r':      float_to_svg(stile_rad),
					'fill':   color_to_hex(palette[tile_color_shape])
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
