from sklearn.decomposition import IncrementalPCA
import pandas
import random
from pynput import keyboard
import sys

import allfields
import livecapture


def train_live_capture():
	# Must be bigger than 10 to work with PCA. 100 seems fine
	batch_size = 100
	n_components = len(allfields.get_all_fields())
	ipca = IncrementalPCA(n_components=n_components, batch_size=batch_size)

	interface = livecapture.select_interface()

	with keyboard.Listener(on_press=lambda _: False) as listener:
		while(listener.running):
			fields = livecapture.capture(batch_size, listener)
			print(".", end="")
			sys.stdout.flush()
			ipca.fit(fields)


	listener.join()
	print()
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

def train_csv(csv):
	raise NotImplementedError
