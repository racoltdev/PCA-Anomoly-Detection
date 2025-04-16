
def get_all_fields():
	return ["IP", "src_ip", "dst_ip", "proto", "length", "ttl", "ip_flags", "UDP", "src_port", "dst_port", "TCP", "tcp_flags"]

def empty_field_dict():
	field_dict = {}
	for f in get_all_fields():
		field_dict[f] = 0
	return field_dict

