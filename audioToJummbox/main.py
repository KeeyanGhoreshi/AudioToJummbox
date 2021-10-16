import argparse
import os
import sys
import logging
from audioToJummbox import converter

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("infile", help="The audio file to convert")
    parser.add_argument("--base", "-b", default="./resources/template.json", help="The file used as the base for the output.  See readme.")
    parser.add_argument("--output", "-o", default="./resources/data.json", help="The output jummbox json file")
    parser.add_argument("--tempo", "-t", default=200, type=float, help="The tempo of the song the audio is going into, not the tempo of the audio!")
    parser.add_argument(
        "--smooth", 
        "-s", 
        type=int, 
        default=0,
        help="Can be 1, 2, or 3.  Max tempo for each is 300, 150, 100")
    args = parser.parse_args()
    args.output = (
        "{}.json".format(os.path.basename(args.infile))
        if not args.output
        else args.output
    )

    return args

def main():
    try:
        logging.basicConfig(level=logging.DEBUG, format="%(message)s")
        args = parse_args()
        converter.convert(args.infile, args.tempo, args.base, args.output, args.smooth)
        print(args)
    except KeyboardInterrupt:
        sys.exit(1)
    except Exception as e:
        logging.exception(e)
        sys.exit(1)

if __name__ == "__main__":
    main()