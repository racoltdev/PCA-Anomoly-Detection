from sklearn.decomposition import IncrementalPCA
import pandas
import random
from pynput import keyboard
import sys
import time
import pywinctl

import allfields
import livecapture

app_window = pywinctl.getActiveWindow()

def train_live_capture():
	# Must be bigger than 10 to work with PCA. 100 seems fine
	batch_size = 100
	n_components = len(allfields.get_all_fields())
	ipca = IncrementalPCA(n_components=n_components, batch_size=batch_size)

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
			ipca.fit(fields)

	listener.join()
	print("\n")
	print("Done")

def scatter3d(df, pca):
	fig = plt.figure()
	ax = fig.add_subplot(projection='3d')
	num_points = 1000;
	random.seed()
	row_count = df.shape[0]

	plt.scatter(pca[:1000,0], pca[:1000,1], pca[1000:2])
#	for i in range(num_points):
#		df_index = random.randint(0, row_count)
#		df.iloc[[df_index]]

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
