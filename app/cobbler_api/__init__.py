import xmlrpclib
from flask import current_app
from config import Config


class CobblerApi(object):
    def __init__(self):
        self.cobbler_user = Config.COBBLER_USER
        self.cobbler_password = Config.COBBLER_PASSWORD
        self.cobbler_url = Config.COBBLER_SERVER_URL
        try:
            self.remote = xmlrpclib.Server(self.cobbler_url)
            self.token = remote.login(self.cobbler_user,self.cobbler_pass) 
        except Exception as e:
            current_app.logger.error("couldn't connect to cobbler-server")
        
    def get_distros(self):
        return self.remote.get_distros()

    def get_profiles(self):
        return self.remote.get_profiles()

    def get_systems(self):
        return self.remote.get_systems()

    def get_images(self):
        return self.remote.get_images()

    def get_repos(self):
        return self.remote.get_repos()