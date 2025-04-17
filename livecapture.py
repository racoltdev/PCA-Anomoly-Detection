#from scapy.sendrecv import sniff
from scapy.all import sniff
from scapy import interfaces
import scapy

import allfields

def select_interface():
	print("Select an interface by index, or press enter to choose the default:\n")
	interfaces.show_interfaces()
	iface = scapy.config.conf.iface
	print(f"Default: {iface}")
	selection = input("\nInterface selection: ")
	if selection != '':
		iface = interfaces.dev_from_index(int(selection))
	print(f"Using interface {iface}\n")
	return iface

def capture(iface, packet_count, exit_condition):
	# Stop capture part way through a batch if user requests a stop
	#stop_if = lambda _: not listener.running
	packet_filter = "tcp or udp"
	capture = sniff(iface=iface, count=packet_count, filter=packet_filter, stop_filter=exit_condition)

	fields = extract_fields(capture)
	for i in range(len(fields)):
		fields[i] = list(fields[i].values())
	return fields

def expand_layers(x):
    yield x
    while x.payload:
        x = x.payload
        yield x

def get_packet_layers(packet):
    counter = 0
    while True:
        layer = packet.getlayer(counter)
        if layer is None:
            break

        yield layer
        counter += 1

def extract_fields(capture):
	fields = []
	for packet in capture:
		field_dict = allfields.empty_field_dict()
		if packet.haslayer("IP"):
			layer = packet.getlayer("IP")
			field_dict["IP"] = 1
			field_dict["src_ip"] = hash(layer.src)
			field_dict["dst_ip"] = hash(layer.dst)
			field_dict["proto"] = layer.proto
			field_dict["length"] = len(packet)
			field_dict["ttl"] = layer.ttl
			field_dict["ip_flags"] = int(layer.flags)

		if packet.haslayer("UDP"):
			layer = packet.getlayer("UDP")
			field_dict["UDP"] = 1
			field_dict["src_port"] = layer.sport
			field_dict["dst_port"] = layer.dport

		if packet.haslayer("TCP"):
			layer = packet.getlayer("TCP")
			field_dict["TCP"] = 1
			field_dict["src_port"] = layer.sport
			field_dict["dst_port"] = layer.dport
			field_dict["tcp_flags"] = int(layer.flags)

		layer_count = 0
		for layer in get_packet_layers(packet):
			# print(layer.name)
			# print(layer.fields)
			layer_count += 1
		field_dict["layer_count"] = layer_count
		fields.append(field_dict)
	return fields


