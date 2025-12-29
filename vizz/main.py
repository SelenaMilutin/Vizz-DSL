import sys
from textx import metamodel_from_file
from executor import execute

def main():
    mm = metamodel_from_file("vizz.tx")
    model = mm.model_from_file(sys.argv[1])
    execute(model)

if __name__ == "__main__":
    main()
