import argparse
import sys

from pycalc.pycalc import evaluate

try:
    parser = argparse.ArgumentParser(description="Pure-python command-line calculator.")
    parser.add_argument("expression", metavar="EXPRESSION", type=str, help="expression string to evaluate")
    parser.add_argument("-m", "--use-modules", metavar="MODULE", action="append", nargs='+',
                        help="additional modules to use")
    args = parser.parse_args()
    use_modules = []
    if args.use_modules:
        use_modules = [module for sublist in args.use_modules for module in sublist]
    result = evaluate(use_modules, args.expression)
    print(result)
except Exception as e:
    sys.exit("ERROR: " + str(e))