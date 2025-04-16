import argparse

import train

parser = argparse.ArgumentParser()
parser.add_argument("csv", nargs="?")
args = parser.parse_args()
if args.csv != None:
	train.train_csv(args.csv)
else:
	train.train_live_capture()

