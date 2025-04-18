import matplotlib.pyplot as plt
import numpy
import random

def scatter3d(sample, pca):
	fig = plt.figure()
	ax = fig.add_subplot(projection='3d')

	transformed = numpy.array(pca.transform(sample))
	points, s = get_point_sizes(transformed)
	ax.scatter(points[:, 0], points[:, 1], zs=points[:, 2], s=s)

	plt.show()
	#plt.savefig("30min-NoIp.png")

def get_point_sizes(data):
	repeat_count = dict()
	point_lookup = dict()
	total_repeats = 0
	for point in data:
		hashed_point = point.tostring()
		if hashed_point not in repeat_count:
			repeat_count[hashed_point] = 20
			point_lookup[hashed_point] = point.tolist()
		else:
			repeat_count[hashed_point] += 2
			total_repeats += 1

	# Gauranteed to be the same order since they use the same hash
	points_list = list(point_lookup.values())
	ordered_points = numpy.array([numpy.array(p) for p in points_list])
	ordered_sizes = repeat_count.values()

	return ordered_points, ordered_sizes


def get_scatter_sample(scatter_sample, packets, proportion, sample_size):
	# In case the first iteration is cut short
	proportion = min(proportion, 1)

	if proportion == 1:
		return packets[:len(scatter_sample)]

	if len(scatter_sample) < sample_size:
		remaining_capacity = sample_size - len(scatter_sample)
		[scatter_sample.append(x) for x in packets[:remaining_capacity]]
		return scatter_sample

	replace_count = int(len(scatter_sample) * proportion)
	replace_count = max(replace_count, 1)
	replace_count = min(replace_count, len(packets))

	for _ in range(replace_count):
		pick = random.randint(0, len(packets) - 1)
		replace_index = random.randint(0, len(scatter_sample) - 1)
		scatter_sample[replace_index] = packets[pick]
		del packets[pick]
	return scatter_sample

def anomalies_over_time(metrics):
	plt.plot(metrics, linewidth=4)
	plt.title("Anomaly Metric")
	plt.show()
