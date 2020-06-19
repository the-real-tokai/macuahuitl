# The “Macuahuitl” Generative Art Toolbox

[![GitHub](https://img.shields.io/github/license/the-real-tokai/macuahuitl?color=green&label=License&style=flat)](https://github.com/the-real-tokai/macuahuitl/blob/master/LICENSE)
[![GitHub Code Size in Bytes](https://img.shields.io/github/languages/code-size/the-real-tokai/macuahuitl?label=Code%20Size&style=flat)](https://github.com/the-real-tokai/macuahuitl/)
[![IRC](https://img.shields.io/badge/IRC-irc.freenode.net%20%23macuahuitl-orange&style=flat)](https://webchat.freenode.net/#macuahuitl)
[![Twitter Follow](https://img.shields.io/twitter/follow/binaryriot?color=blue&label=Follow%20%40binaryriot&style=flat)](https://twitter.com/binaryriot)

## Synopsis

*The “Macuahuiltl” Generative Art Toolbox* is a collection of personal `Python 3` scripts to
generate artworks or elements for artworks that can either be used directly or processed further
in common vector design software packages.

All scripts output `Scalable Vector Graphics` (SVG) image files directly which easily can be
loaded in common vector graphics application like `InkScape`, `Affinity Designer`, `Adobe
Illustrator`, and so on. A few of the scripts also can output a custom `JSON`-based format of
particle or shape descriptions which then can be further processed by related scripts or
imported into 3D graphic software packages like `Blender` or `CINEMA 4D` for rendering.

## The “How?” and The “Why?”

Usually to automatize generation of shapes or pattern for vector illustrations —which would
be *way too boring* to create manually in Affinity Designer— the scripts start out with a quick
visual idea and just a handful lines of quick code as proof of concept.

Once that's done crazy silliness starts by making every variable of the algorithm user-configurable
via a CLI interface. The result: the scripts explode in code size exponentially. Not that this
really makes a lot of sense or would revolutionize the world… it's simply **fun stuff** done for
recreation. So here we are! 😅

## Script Overview

### Comitl

<img width="90" height="90" src="Documentation/Comitl/Examples/basic_01.svg" alt="Figure 1 - Comitl Example"> <img width="90" height="90" src="Documentation/Comitl/Examples/basic_04.svg" alt="Figure 2 - Comitl Example"> <img width="90" height="90" src="Documentation/Comitl/Examples/basic_06.svg" alt="Figure 3 - Comitl Example"> <img width="90" height="90" src="Documentation/Comitl/Examples/basic_08.svg" alt="Figure 4 - Comitl Example"> <img width="90" height="90" src="Documentation/Comitl/Examples/basic_02.svg" alt="Figure 5 - Comitl Example">

Comitl concentrically arranges randomly sized arcs into a pretty disc shape. Output is generated as a set of vector shapes in Scalable
Vector Graphics (SVG) format and printed on the standard output stream. Comitl also supports SVG animations, optional PNG output
(with `cairosvg`), and has countless of parameters for configuration of the generated shape.

[Direct Download](https://raw.githubusercontent.com/the-real-tokai/macuahuitl/master/comitl.py) | [Documentation](comitl.md)

### Altepetl

<img width="90" height="90" src="Documentation/Altepetl/Examples/basic_01.svg" alt="Figure 1 - Altepetl Example"> <img width="90" height="90" src="Documentation/Altepetl/Examples/basic_02.svg" alt="Figure 2 - Altepetl Example"> <img width="90" height="90" src="Documentation/Altepetl/Examples/basic_03.svg" alt="Figure 3 - Altepetl Example"> <img width="90" height="90" src="Documentation/Altepetl/Examples/basic_04.svg" alt="Figure 4 - Altepetl Example">

Altepetl implements an artful grid-based layout of "U"-shapes; inspired by some of generative art pioneer [Véra Molnar](http://www.veramolnar.com)'s
artworks. Output is generated as a set of vector shapes in Scalable Vector Graphics (SVG) format and printed on the standard output stream. Altepetl
also supports optional PNG output (with `cairosvg`), and has a handful of parameters for configuration of the generated artwork.

[Direct Download](https://raw.githubusercontent.com/the-real-tokai/macuahuitl/master/altepetl.py) | [Documentation](altepetl.md)

### Atlatl

coming soon.

### Xonacatl

coming soon.

### Acahualli

coming soon.

### Ohtli

coming soon.

### Temo

<img width="90" height="90" src="Documentation/Temo/Examples/basic_02.svg" alt="Figure 1 - Temo Example"> <img width="90" height="90" src="Documentation/Temo/Examples/basic_03.svg" alt="Figure 2 - Temo Example"> <img width="90" height="90" src="Documentation/Temo/Examples/basic_04.svg" alt="Figure 3 - Temo Example"> <img width="90" height="90" src="Documentation/Temo/Examples/basic_05.svg" alt="Figure 4 - Temo Example">

Temo creates a colorful maze inspired by a famous one line C64 BASIC program (`10 PRINT CHR$(205.5+RND(1)); : GOTO 10`). Output is generated as a set
of vector shapes in Scalable Vector Graphics (SVG) format and printed on the standard output stream. Temo also supports optional PNG output (with `cairosvg`),
and has a handful of parameters for configuration of the generated artwork.

[Direct Download](https://raw.githubusercontent.com/the-real-tokai/macuahuitl/master/temo.py) | [Documentation](temo.md)

## Copyright and License

Copyright © 2019-2020 Christian Rosentreter
(https://www.binaryriot.org/)

All scripts are free software: you can redistribute them and/or modify them under the terms of the [GNU Affero General Public License](LICENSE) as
published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
