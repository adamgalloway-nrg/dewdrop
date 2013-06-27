#!/usr/bin/env python
#
# App.py

from config import Config
from loginWindow import LoginWindow
from dapi import DAPI
from dewdrop import DewDrop
from version import new_version
import gtk
import sys
import os
import pkg_resources

class App:
	def __init__(self):
		if not pkg_resources.resource_exists(__name__, 'config.cfg'):
			print 'Config file (config.cfg) is missing'
			# import ConfigParser
			# config = ConfigParser.ConfigParser()
			# config.add_section('NetworkSettings')
			# config.set('NetworkSettings', 'PublicKey', '<Enter Public Key>')
			# config.set('NetworkSettings', 'PrivateKey', '<Enter Private Key>')
			# config.set('NetworkSettings', 'Server', 'sandbox.droplr.com')
			# config.set('NetworkSettings', 'Port', '8069')
			# config.set('NetworkSettings', 'Scheme', 'http')
			# file = open('config.cfg', 'w')
			# config.write(file)
			# file.close()
			sys.exit(1)

		self._cfg = Config()

		new_version()

		if self._cfg.get('email') == None:
			# Time to login
			self.show_login()
		else:
			# Test the credentials
			if self.test_credentials(self._cfg.get('email'), self._cfg.get('passhash')) == True:
				self.start()
			else:
				self.logout()

	def logout(self): 
		self._cfg.set('email', None)
		self._cfg.set('passhash', None)
		self._cfg.save()

		if hasattr(self, 'dew'):
			delattr(self, 'dew')
		self.show_login()

	def show_login(self):
		login = LoginWindow(self)
		login.show()

	def test_credentials(self, email, passhash):
		d = DAPI()
		d.auth(email, passhash)
		rtn = d.account_details()
		
		if rtn.is_error():
			return rtn
		return True

	def start(self):
		self.dew = DewDrop(self)
		print 'start'

if __name__ == "__main__":
	app = App()
