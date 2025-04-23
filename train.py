from sklearn.decomposition import IncrementalPCA
import pandas
import time
import pickle
import statistics

import allfields
import livecapture
import plot
import ui_interfaces
import anomaly

def train_live_capture(iface=None, timeout=None, out_file=None, pretrained=None, plot_anoms=True):
	scatter_sample = []
	sample_size = 1000
	anomaly_metrics = []

	batch_size = 100

	ipca = None
	if pretrained == None:
		ipca = IncrementalPCA(n_components=3, batch_size=batch_size)
	else:
		with open(pretrained, "rb") as f:
			ipca = pickle.load(f)
			batch_size = ipca.batch_size

	packet_count = 0
	start_time = int(time.time())
	if iface == None:
		iface = livecapture.select_interface()
	else:
		print(f"Using interface {iface}\n")

	exit_condition = setup_exit_function(timeout)
	while(not exit_condition()):
		ui_interfaces.ui_update(start_time, packet_count)

		packets, _ = livecapture.capture(iface, batch_size, exit_condition)
		packet_count += len(packets)

		# livecapture can exit before filling enough of a batch for pca to train with
		if (len(packets) > 10):
			ipca.partial_fit(packets)
			if plot_anoms:
				components = ipca.transform(packets)
				variance = ipca.explained_variance_
				anomaly_metrics.append(cluster(components, variance))
			# Collect a sample of packets collected to generate a scatter plot of pca fit
			proportion = batch_size / packet_count
			scatter_sample = plot.get_scatter_sample(scatter_sample, packets, proportion, sample_size)

	ui_interfaces.ui_update(start_time, packet_count)

	print("\n")
	print(f"Captured {packet_count} packets")

	print(f"Explained variance: {ipca.explained_variance_}")
	print(f"Explained variance ratio: {ipca.explained_variance_ratio_}")
	if out_file != None:
		with open(out_file, "wb") as f:
			pickle.dump(ipca, f)

	plot.scatter3d(scatter_sample, ipca)
	if plot_anoms:
		plot.anomalies_over_time(anomaly_metrics)
	print("Done")

	# Let main/cli handler pass model over to anomaly detection
	return ipca

def cluster(components, variance):
	sums = []
	for observation in components:
		obs_sum = sum([(y**2) / lambda_ for y, lambda_ in zip(observation, variance)])
		sums.append(obs_sum)
	mean_distance = statistics.fmean(sums)
	return mean_distance

def setup_exit_function(timeout):
	if timeout == None:
		print("Capturing packets and training PCA. Press q to stop training:")
		return ui_interfaces.exit_on_q()
	else:
		start_time = int(time.time())
		print(f"Capturing packets and training PCA. Capture will run for {timeout} seconds:")
		return lambda _=0: int(time.time()) - start_time > int(timeout)

def train_csv(csv):
	raise NotImplementedError
