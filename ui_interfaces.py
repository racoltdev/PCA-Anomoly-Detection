from pynput import keyboard
import pywinctl
import time
import sys

app_window = pywinctl.getActiveWindow()

def exit_on_q():
	listener = keyboard.Listener(on_press=_quit_on_press_q)
	listener.start()
	return lambda _=0: not listener.running

def _quit_on_press_q(key):
	active_window = pywinctl.getActiveWindow()
	if active_window == app_window:
		try:
			if (key.char == 'q'):
				return False
		except AttributeError:
			pass
	return True

def ui_update(start_time, packet_count, anomalies=None):
	elapsed_time = int(time.time()) - start_time
	format_time = time.strftime("%H:%M:%S", time.gmtime(elapsed_time))
	print(f"\rRun time: {format_time}\tCaptured packets: {packet_count}", end="")
	if anomalies != None:
		print(f" \tAnomalies: {anomalies}", end="")
	sys.stdout.flush()

