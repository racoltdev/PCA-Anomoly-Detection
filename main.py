import argparse

import train

parser = argparse.ArgumentParser()
parser.add_argument("-i", "--interface")
parser.add_argument("-t", "--timeout")
args = parser.parse_args()
train.train_live_capture(args.interface, args.timeout)

