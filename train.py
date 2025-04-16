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

def train_live_capture(stop_condition="keyboard"):
	scatter_sample = [0] * 1000

	# Must be bigger than 10 to work with PCA. 100 seems fine
	batch_size = 100
	n_components = len(allfields.get_all_fields())
	ipca = IncrementalPCA(n_components=3, batch_size=batch_size)

	interface = livecapture.select_interface()
	packet_count = 0
	start_time = int(time.time())

	with keyboard.Listener(on_press=on_press) as listener:
		print("Capturing packets and training PCA. Press q to stop training:")
		while(listener.running):
			elapsed_time = int(time.time()) - start_time
			format_time = time.strftime("%H:%M:%S", time.gmtime(elapsed_time))
			print(f"\rRun time: {format_time}\tCaptured packets: {packet_count}", end="")
			sys.stdout.flush()

			fields = livecapture.capture(batch_size, listener)
			packet_count += len(fields)
			# livecapture can exit before filling enough of a batch for pca to read
			if (len(fields) > 10):
				ipca.partial_fit(fields)
				scatter_sample = get_scatter_sample(scatter_sample, fields, batch_size / packet_count)

	listener.join()
	print("\n")
	scatter3d(scatter_sample, ipca)
	print("Done")

def scatter3d(sample, pca):
	fig = plt.figure()
	ax = fig.add_subplot(projection='3d')

	transformed = numpy.array(pca.transform(sample))
	ax.scatter(transformed[:, 0], transformed[:, 1], zs=transformed[:, 2])

	plt.show()

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
