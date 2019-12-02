#!/usr/bin/python

# MIT License
# 
# Copyright (c) 2019 AP Hogeschool
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
# encoding=utf8

import sys
import time
import pexpect
import subprocess

class BtAutoPair:
	"""Class to auto pair and trust with bluetooth."""

	def __init__(self):
		p = subprocess.Popen("./agent.py", shell = False)
		out = subprocess.check_output("/usr/sbin/rfkill unblock bluetooth", shell = True)
		self.child = pexpect.spawn("bluetoothctl", echo = False)

	def get_output(self,command, pause = 0):
		"""Run a command in bluetoothctl prompt, return output as a list of lines."""
		self.child.send(command + "\n")
		time.sleep(pause)
		start_failed = self.child.expect(["bluetooth", pexpect.EOF])

		if start_failed:
			raise BluetoothctlError("Bluetoothctl failed after running " + command)
			
		return self.child.before.split("\r\n")

	def enable_pairing(self):
		"""Make device visible to scanning and enable pairing."""
		print("pairing enabled")
		try:
			out = self.get_output("power on")
			#out = self.get_output("discoverable-timeout 86400")
			out = self.get_output("discoverable on")
			out = self.get_output("pairable on")
			out = self.get_output("agent off")

		except:
			return None

	def disable_pairing(self):
		"""Disable devices visibility and ability to pair."""
		try:
			out = self.get_output("discoverable off")
			out = self.get_output("pairable off")

		except e:
			print(e)
			return None

