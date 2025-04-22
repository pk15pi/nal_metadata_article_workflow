import pickle
import pprint
import argparse

# Read in the file name, print mode, and pretty print width from the command line
parser = argparse.ArgumentParser()
parser.add_argument("input_file", help="The pickle file to read")
parser.add_argument("--pretty", action="store_true", help="Pretty print the output")
parser.add_argument("--output_file", help="Output file to save the pretty print result")
parser.add_argument("--width", type=int, default=60, help="Width for pretty print (default: 60)")
args = parser.parse_args()
input_file = args.input_file

# Check to make sure input file is a .pkl file
if not input_file.endswith(".pkl"):
    raise ValueError("Input file must be a .pkl file")

with open(input_file, "rb") as f:
    data = pickle.load(f)
    if args.pretty:
        if args.output_file:
            with open(args.output_file, "w") as out_f:
                pp = pprint.PrettyPrinter(width=args.width, stream=out_f)
                pp.pprint(data)
        else:
            pp = pprint.PrettyPrinter(width=args.width)
            pp.pprint(data)
    else:
        if args.output_file:
            with open(args.output_file, "w") as out_f:
                out_f.write(str(data))
        else:
            print(data)