from config import base
from config import perror, psuccess, pinfo

import os
import json
import yaml

class configparser:

    filesToReplace = []

    def __init__(self, config_file=""):

        self.base = base()
        self.config = self.base.config
        self.globals = self.base.globals
        self.ready = True

        # Check if its the first run
        # by checking for ~/.c0nfigure
        if not os.path.exists(self.config["repo_dir"]):
            pinfo("Run --init first")
            self.ready = False

        # Use Custom/Default config file
        if config_file != "":
            self.config["config_file"] = config_file

    """Function to call from outside"""
    def parseConfig(self):
        if not self.ready:
            return 0
        return self.openConfig()

    """
    Opens the defined config file and passes it to the parser
    """
    def openConfig(self):

        try:
            with open(self.config["config_file"], "r") as config:
                return self.parse(config)
        except IOError:
                perror("Config File not found")
                return 0

    def getGlobal(self, obj, name):
        if name in obj.keys():

            if name == "repo_dir":
                self.config[name] = os.path.abspath(obj[name])
            else:
                self.config[name] = obj[name]

    """
    Parse the Config file
    Config file is in YAML format
    """
    def parse(self, config):

        try:
            obj = yaml.safe_load(config)

            # 1. parse global variables

            for glVar, _ in self.globals:
                self.getGlobal(obj, glVar)

            # 1.2 Check of the required variables are set

            for name, req in self.globals:
                if req == True and name not in self.config.keys():
                    perror("Required global variable %s not found" % name)
                    raise Exception("Required global not found")



            # 2. parse programs

            folders = [key for key in obj.keys() if key not in [x for x, _ in self.globals]]


            # the adjustPath call, repaces ~ with the homepath

            # Dict with prorgams as keys, and list of replacement files as value
            self.replacement_rel = {key:self.adjustPath(obj[key]) for key in folders}

            return 1


        except Exception as e:
            print e.message
            perror("Failed to parse config")
            return 0


    """Adjusts the Path, eg. replces ~ with the home path, etc.."""
    def adjustPath(self, arr):
        # arr = [["1", "2"], ["1", "2"], ..]
        for i, (name, path) in enumerate(arr):
            arr[i][1] = self.base.getHome(path)

        return arr


