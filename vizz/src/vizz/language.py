import os
from textx import metamodel_from_file
from textx import language

@language("vizz", "*.vizz")
def vizz_language():
    grammar = os.path.join(os.path.dirname(__file__), "vizz.tx")
    return metamodel_from_file(grammar)
