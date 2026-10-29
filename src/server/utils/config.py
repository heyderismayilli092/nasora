# Script for loading the configuration file

import json
import os

config_file = "config.json"

class Configuration:
    # configuration file load
    def load(self):
        with open(config_file, "r") as jsondata:
            data = json.load(jsondata)
        server_name = data["nasora"]["server_name"]
        publish_path = data["nasora"]["publish_path"]
        return {"server-name": server_name, "publish-path": publish_path}

    # configuration file check
    def checkconf(self):
        with open(config_file, "r") as jsondata:
            data = json.load(jsondata)
        server_name = data["nasora"]["server_name"]
        publish_path = data["nasora"]["publish_path"]
        # check server name
        if len(server_name) == 0:
            return {"status": False, "details": "Server name not entered !"}
        # check publishing path
        if len(publish_path) == 0:
            return {"status": False, "details": "The path for the folder to be published has not been entered !"}
        if not os.path.exists(publish_path):
            return {"status": False, "details": "The path for the folder to be published does not exist !"}

        return {"status": True}

