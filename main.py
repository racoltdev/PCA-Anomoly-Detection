import argparse
import pickle

import train
import anomaly

parser = argparse.ArgumentParser()
parser.add_argument("-i", "--interface")
parser.add_argument("-t", "--timeout")
parser.add_argument("-l", "--load-and-train")
parser.add_argument("-o", "--output-model")
parser.add_argument("-c", "--continue", dest="cont", action="store_true")
parser.add_argument("-L", "--load-model")
parser.add_argument("-C", "--outlier-threshold", default=3)
parser.add_argument("-O", "--output-anomalies")
args = parser.parse_args()

model = None
if args.load_model == None:
	model = train.train_live_capture(args.interface, args.timeout, args.output_model, args.load_and_train)
else:
	with open(args.load_model, "rb") as f:
		model = pickle.load(f)

if args.cont or args.load_model != None:
	anomaly.live_anomaly_detect(model, int(args.outlier_threshold), args.interface, args.output_anomalies)
