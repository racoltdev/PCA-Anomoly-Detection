import time

import livecapture
import ui_interfaces

def live_anomaly_detect(model, c=3, iface=None, output_file=None):
	log = None
	if output_file != None:
		log = open(output_file, "w")

	batch_size = model.batch_size
	total_anomalies = 0
	start_time = int(time.time())
	packet_count = 0

	if iface == None:
		iface = livecapture.select_interface()
	else:
		print(f"Using interface {iface}\n")

	print("Capturing packets and recording anomalies. Press q to stop:")
	exit_condition = ui_interfaces.exit_on_q()

	# Sniff {batch_size} # of packets and detect anomalies each iteration
	while(not exit_condition()):
		ui_interfaces.ui_update(start_time, packet_count, total_anomalies)

		packets, raw = livecapture.capture(iface, batch_size, exit_condition, log != None)
		packet_count += len(packets)

		observations = model.transform(packets)
		variance = model.explained_variance_
		anomalies = get_anomalies(observations, variance, c)
		total_anomalies += len(anomalies)

		if (log != None):
			for a in anomalies:
				line = f"Anomaly score: {a[0]}"
				line += f"\n{raw[a[1]]}\n\n"
				log.write(line)

	ui_interfaces.ui_update(start_time, packet_count, total_anomalies)
	print()

	if log != None:
		log.close()

# Return any packet with a distance greater than c
def get_anomalies(observations, variance, c):
	anomalies = []
	for i, observation in enumerate(observations):
		# Shyu et al. implementation of Mahalanobis distance for PCA
		obs_sum = sum([(y**2) / lambda_ for y, lambda_ in zip(observation, variance)])
		if obs_sum > c:
			anomalies.append([obs_sum, i])
	return anomalies

