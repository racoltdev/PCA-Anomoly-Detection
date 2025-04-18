import argparse

import train

parser = argparse.ArgumentParser()
parser.add_argument("-i", "--interface")
parser.add_argument("-t", "--timeout")
parser.add_argument("-l", "--load-and-train")
parser.add_argument("-o", "--output-model")
args = parser.parse_args()
print(args)
train.train_live_capture(args.interface, args.timeout, args.output_model, args.load_and_train)

