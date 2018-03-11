# praat
A suite of python tools to manipulate Praat software, running it with certain inputs and processing its textgrid file formats

For the textgrid format:
http://www.fon.hum.uva.nl/praat/manual/TextGrid_file_formats.html

One initial task is to convert it into something that can be more easily processed programmatically, such as python dictionaries or json format. For this, we use textgrid_lib.py

# Command line
Usage: textgrid_lib.py /input/directory/path/file.textgrid /output/directory/file.json -order
hint: -order is optional, the default is that elements (points/intervals) are in unordered dictionary, so if you specify -order they are in an ordered list

# within python code
from textgrid_lib import textgrid_2_dict
python_dict=textgrid_2_dict(text_grid_file_path,order_elements=True)
