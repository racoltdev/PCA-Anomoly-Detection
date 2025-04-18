import argparse

import train
import anomaly

parser = argparse.ArgumentParser()
parser.add_argument("-i", "--interface")
parser.add_argument("-t", "--timeout")
parser.add_argument("-l", "--load-and-train")
parser.add_argument("-o", "--output-model")
parser.add_argument("-L", "--load-model")
parser.add_argument("-C", "--outlier-threshold")
args = parser.parse_args()

if args.load_model != None:
	anomaly.live_anomaly_detect(args.load_model, args.outlier_threshold, args.interface)
else:
	train.train_live_capture(args.interface, args.timeout, args.output_model, args.load_and_train)

