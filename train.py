from sklearn.decomposition import IncrementalPCA
import pandas
import random
from pynput import keyboard
import sys
import time
import pywinctl
import random
import matplotlib.pyplot as plt
import numpy

import allfields
import livecapture

app_window = pywinctl.getActiveWindow()

def train_live_capture(iface=None, timeout=None):
	scatter_sample = [0] * 1000

	# Must be bigger than 10 to work with PCA. 100 seems fine
	batch_size = 100
	n_components = len(allfields.get_all_fields())
	ipca = IncrementalPCA(n_components=3, batch_size=batch_size)

	if iface == None:
		iface = livecapture.select_interface()
	else:
		print(f"Using interface {iface}\n")

	packet_count = 0
	start_time = int(time.time())

	exit_condition = lambda _: False
	if timeout == None:
		print("Capturing packets and training PCA. Press q to stop training:")
		listener = keyboard.Listener(on_press=on_press)
		listener.start()
		exit_condition = lambda _: not listener.running
	else:
		print(f"Capturing packets and training PCA. Capture will run for {timeout} seconds:")
		exit_condition = lambda _: int(time.time()) - start_time > int(timeout)

	while(not exit_condition(0)):
		elapsed_time = int(time.time()) - start_time
		format_time = time.strftime("%H:%M:%S", time.gmtime(elapsed_time))
		print(f"\rRun time: {format_time}\tCaptured packets: {packet_count}", end="")
		sys.stdout.flush()

		fields = livecapture.capture(iface, batch_size, exit_condition)
		packet_count += len(fields)
		# livecapture can exit before filling enough of a batch for pca to read
		if (len(fields) > 10):
			ipca.partial_fit(fields)
			scatter_sample = get_scatter_sample(scatter_sample, fields, batch_size / packet_count)

	print("\n")
	print(f"Captured {packet_count} packets")
	scatter3d(scatter_sample, ipca)
	print("Done")

def scatter3d(sample, pca):
	fig = plt.figure()
	ax = fig.add_subplot(projection='3d')

	transformed = numpy.array(pca.transform(sample))
	points, s = get_point_sizes(transformed)
	# TODO find repeat points and plot with s proportional to frquency
	ax.scatter(points[:, 0], points[:, 1], zs=points[:, 2], s=s)

	plt.show()
	#plt.savefig("30min-NoIp.png")

def get_point_sizes(data):
	repeat_count = dict()
	point_lookup = dict()
	for point in data:
		hashed_point = point.tostring()
		if hashed_point not in repeat_count:
			repeat_count[hashed_point] = 20
			point_lookup[hashed_point] = point.tolist()
		else:
			repeat_count[hashed_point] += 2

	# Gauranteed to be the same order since they use the same hash
	#print(list(point_lookup.values()))
	points_list = list(point_lookup.values())
	ordered_points = numpy.array([numpy.array(p) for p in points_list])
	#points = numpy.ndarray(list(point_lookup.values()))
	ordered_sizes = repeat_count.values()

	return ordered_points, ordered_sizes


def get_scatter_sample(scatter_sample, packets, proportional_weight):
	# In case the first iteration is cut short
	proportional_weight = min(proportional_weight, 1)

	if proportional_weight == 1:
		return packets[:len(scatter_sample)]

	replace_count = int(len(scatter_sample) * proportional_weight)
	replace_count = max(replace_count, 1)
	replace_count = min(replace_count, len(packets))

	for i in range(replace_count):
		pick = random.randint(0, len(packets) - 1)
		replace_index = random.randint(0, len(scatter_sample) - 1)
		scatter_sample[replace_index] = packets[pick]
		del packets[pick]
	return scatter_sample

def on_press(key):
	active_window = pywinctl.getActiveWindow()
	if active_window == app_window:
		try:
			if (key.char == 'q'):
				return False
		except AttributeError:
			pass
	return True

def train_csv(csv):
	raise NotImplementedError
