
# Comitl

`comitl` *noun* — Classical Nahuatl: [1] cooking pot, pan — a rounded or cylindrical container used to heat up meals over a fire.

### Synopsis

Concentrically arranges randomly sized arcs into a pretty disc shape. Output is generated as a set of vector shapes in Scalable
Vector Graphics (SVG) format and printed on the standard output stream.

### Requirements

An installation of Python 3 (any version above 3.5 should do fine; older versions might work, but have not been tested.). There are
currently no dependencies to any 3rd-party libraries or modules.

### Output Examples

![Figure 1](./Documentation/Comitl/Examples/basic_01.svg)
![Figure 2](./Documentation/Comitl/Examples/basic_02.svg)
![Figure 3](./Documentation/Comitl/Examples/basic_03.svg)
![Figure 4](./Documentation/Comitl/Examples/basic_04.svg)
![Figure 5](./Documentation/Comitl/Examples/basic_05.svg)
![Figure 6](./Documentation/Comitl/Examples/basic_06.svg)
![Figure 7](./Documentation/Comitl/Examples/basic_07.svg)
![Figure 8](./Documentation/Comitl/Examples/basic_08.svg)
![Figure 9](./Documentation/Comitl/Examples/basic_09.svg)
![Figure 10](./Documentation/Comitl/Examples/basic_10.svg)
![Figure 11](./Documentation/Comitl/Examples/basic_11.svg)
![Figure 12](./Documentation/Comitl/Examples/basic_12.svg)

### Usage

```
usage: comitl.py [-V] [-h] [--circles INT] [--stroke-width FLOAT]
                 [--gap FLOAT] [--inner-radius FLOAT] [--hoffset FLOAT]
                 [--voffset FLOAT] [--colour COLOUR] [--random-seed INT]
                 [--randomise]

Startup:
  -V, --version         show version number and exit
  -h, --help            show this help message and exit

Algorithm:
  --circles INT         number of concentric arc elements to generate inside
                        the disc  [:21]
  --stroke-width FLOAT  width of the generated strokes  [:6]
  --gap FLOAT           distance between the generated strokes
  --inner-radius FLOAT  setup inner disc radius to create an annular shape
  --hoffset FLOAT       shift the whole disc horizontally  [:0.0]
  --voffset FLOAT       shift the whole disc vertically  [:0.0]
  --colour COLOUR       SVG compliant colour specification or identifier
                         [:black]
  --random-seed INT     fixed initialisation of the random number generator
                        for predictable results
  --randomise           generate truly random disc layouts; values provided
                        via other commandline parameters are utilised as
                        limits
```

#### Usage Examples
```
./comitl.py --circles=10 --color=green > output.svg
```

```
# Preview output with ImageMagick's "convert" and Preview.app (Mac OS X)
./comitl.py --randomise | convert svg:- png:- | open -f -a Preview.app
# Preview output with ImageMagick's "convert" and "display" (Linux/BSD/etc.)
./comitl.py --randomise | convert svg:- png:- | display
````

### History

<table>
    <tr>
        <td valign=top>1.4</td>
        <td valign=top nowrap>20-May-2020</td>
        <td>
			<ul>
				<li>Allow arc specification in degree
				<li>Arcs are now initialised with angular offsets and ranges
				<li>Improved code reusability and scope separation
			</ul>
		</td>
    </tr>
    <tr>
        <td valign=top>1.3</td>
        <td valign=top nowrap>19-May-2020</td>
        <td>
			<ul>
				<li>Refactored in preparation for new features
				<li>Optimisations
			</ul>
		</td>
    </tr>
    <tr>
        <td valign=top>1.2</td>
        <td valign=top nowrap>18-May-2020</td>
        <td>
			<ul>
				<li>Utilise SVG groups in the generated output
				<li>Added automatic identifiers to the SVG elements
				<li>Updated help text
			</ul>
		</td>
    </tr>
    <tr>
        <td valign=top>1.1</td>
        <td valign=top nowrap>18-May-2020</td>
        <td>Initial public release</td>
    </tr>
</table>