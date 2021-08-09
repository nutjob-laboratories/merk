import sys
import os
import json
from pathlib import Path

from .resources import *

INSTALL_DIRECTORY = sys.path[0]
MERK_MODULE_DIRECTORY = os.path.join(INSTALL_DIRECTORY, "merk")
DATA_DIRECTORY = os.path.join(MERK_MODULE_DIRECTORY, "data")

CONFIG_DIRECTORY = None
CONFIG_FILE = None

MDI_BACKGROUND_IMAGE = None
APPLICATION_FONT = None
DISPLAY_NAME = APPLICATION_NAME
DISPLAY_ICON = APPLICATION_ICON

def save_settings(filename):

	settings = {
		"mdi_background_image": MDI_BACKGROUND_IMAGE,
		"application_font": APPLICATION_FONT,
		"display_name": DISPLAY_NAME,
		"display_icon": DISPLAY_ICON,
	}

	with open(filename, "w") as write_data:
		json.dump(settings, write_data, indent=4, sort_keys=True)

def patch_settings(settings):
	if not "mdi_background_image" in settings:
		settings["mdi_background_image"] = MDI_BACKGROUND_IMAGE
	if not "application_font" in settings:
		settings["application_font"] = APPLICATION_FONT
	if not "display_name" in settings:
		settings["display_name"] = DISPLAY_NAME
	if not "display_icon" in settings:
		settings["display_icon"] = DISPLAY_ICON

	return settings

def load_settings(filename):
	global MDI_BACKGROUND_IMAGE
	global APPLICATION_FONT
	global DISPLAY_NAME
	global DISPLAY_ICON

	if os.path.isfile(filename):
		with open(filename, "r") as read_settings:
			settings = json.load(read_settings)

			settings = patch_settings(settings)

			MDI_BACKGROUND_IMAGE = settings["mdi_background_image"]
			APPLICATION_FONT = settings["application_font"]
			DISPLAY_NAME = settings["display_name"]
			DISPLAY_ICON = settings["display_icon"]
	else:
		save_settings(filename)

def check_settings(filename):
	if os.path.isfile(filename):
		with open(filename, "r") as read_settings:
			settings = json.load(read_settings)

			if not "mdi_background_image" in settings: return False
			if not "application_font" in settings: return False
			if not "display_name" in settings: return False
			if not "display_icon" in settings: return False
	else:
		return False

	return True

def initialize(directory):
	global CONFIG_DIRECTORY
	global CONFIG_FILE

	# If the passed directory is set to None,
	# set the storage directory to the user's
	# home directory
	if directory==None:
		directory = str(Path.home())

	CONFIG_DIRECTORY = os.path.join(directory, ".merk")
	if not os.path.isdir(CONFIG_DIRECTORY): os.mkdir(CONFIG_DIRECTORY)

	CONFIG_FILE = os.path.join(CONFIG_DIRECTORY, "config.json")