# parse-ply-file
Requirements: python  >=3.8, pandas

How to run:
* Open cmd
* change directory to repo folder (the one with setup.py)
* `pip install -e .`
* Go wherever you want (probably directory with your .ply files)
* to display help message: `python  -m parse_ply_file -h`
* Example call: `python -m parse_ply_file my_file.ply`



# Versioning
<pre>
`A.B.C`
 | | |
 | | | _ _ bugfixes, backwards compatible changes
 | | _ _ _ improvements, not guaranteed to be backwards compatible
 | _ _ _ _ major changes, non backwards compatible
</pre>

## 1.0.0
* Dropped support for Excel
* Auto-detection of columns
* Supports MorphographX 1.x and 2.x

## 0.0.1 Initial release
* Support for Excel .xlsx and .ply files
* Compatible only with MorphographX 1.x
* Max file size 6 columns
* Column separator `" "`

