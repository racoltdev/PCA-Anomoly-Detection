import pickle
import time
import statistics

import livecapture
import ui_interfaces

def live_anomaly_detect(model_file, c=2, iface=None):
	model = None
	with open(model_file, "rb") as f:
		model = pickle.load(f)

	batch_size = model.batch_size
	total_anomalies = 0
	start_time = int(time.time())
	packet_count = 0

	if iface == None:
		iface = livecapture.select_interface()
	else:
		print(f"Using interface {iface}\n")

	if c == None:
		c = 2

	print("Capturing packets and recording anomalies. Press q to stop:")
	exit_condition = ui_interfaces.exit_on_q()

	while(not exit_condition()):
		ui_interfaces.ui_update(start_time, packet_count, total_anomalies)

		packets = livecapture.capture(iface, batch_size, exit_condition)
		packet_count += len(packets)

		observations = model.transform(packets)
		variance = model.explained_variance_
		anomalies = get_anomalies(observations, variance, c)
		total_anomalies += len(anomalies)

	ui_interfaces.ui_update(start_time, packet_count, total_anomalies)
	print()

def get_anomalies(observations, variance, c):
	anomalies = []
	for i, observation in enumerate(observations):
		obs_sum = sum([(y**2) / lambda_ for y, lambda_ in zip(observation, variance)])
		if obs_sum > c:
			anomalies.append([obs_sum, i])
	return anomalies

