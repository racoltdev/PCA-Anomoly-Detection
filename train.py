from sklearn.decomposition import IncrementalPCA
import pandas
from pynput import keyboard
import sys
import time
import pywinctl

import allfields
import livecapture
import plot

app_window = pywinctl.getActiveWindow()

def train_live_capture(iface=None, timeout=None):
	scatter_sample = []
	sample_size = 1000

	batch_size = 100
	n_components = len(allfields.get_all_fields())
	ipca = IncrementalPCA(n_components=3, batch_size=batch_size)

	packet_count = 0
	start_time = int(time.time())
	exit_condition = setup_exit_function(timeout)
	if iface == None:
		iface = livecapture.select_interface()
	else:
		print(f"Using interface {iface}\n")

	while(not exit_condition(0)):
		ui_update(start_time, packet_count)

		packets = livecapture.capture(iface, batch_size, exit_condition)
		packet_count += len(packets)

		# livecapture can exit before filling enough of a batch for pca to train with
		if (len(packets) > 10):
			ipca.partial_fit(packets)
			proportion = batch_size / packet_count
			scatter_sample = plot.get_scatter_sample(scatter_sample, packets, proportion, sample_size)

	ui_update(start_time, packet_count)

	print("\n")
	print(f"Captured {packet_count} packets")
	plot.scatter3d(scatter_sample, ipca)
	print("Done")

def setup_exit_function(timeout):
	if timeout == None:
		listener = keyboard.Listener(on_press=quit_on_q)
		listener.start()
		print("Capturing packets and training PCA. Press q to stop training:")
		return lambda _: not listener.running
	else:
		start_time = int(time.time())
		print(f"Capturing packets and training PCA. Capture will run for {timeout} seconds:")
		return lambda _: int(time.time()) - start_time > int(timeout)

def quit_on_q(key):
	active_window = pywinctl.getActiveWindow()
	if active_window == app_window:
		try:
			if (key.char == 'q'):
				return False
		except AttributeError:
			pass
	return True

def ui_update(start_time, packet_count):
	elapsed_time = int(time.time()) - start_time
	format_time = time.strftime("%H:%M:%S", time.gmtime(elapsed_time))
	print(f"\rRun time: {format_time}\tCaptured packets: {packet_count}", end="")
	sys.stdout.flush()

def train_csv(csv):
	raise NotImplementedError
