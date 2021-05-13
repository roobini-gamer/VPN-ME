#! /usr/bin/env python2

#################################################################
#                                                               #
#                                                               #
#                                                               #
#                                                               #
#       ██████╗  ██████╗  ██████╗ ██████╗ ██╗███╗   ██╗██╗      #
#       ██╔░░██╗██╔░████╗██╔░████╗██╔░░██╗██║████╗  ██║██║      #
#       ██████╔╝██║██╔██║██║██╔██║██████╔╝██║██╔██╗ ██║██║      #
#       ██╔░░██╗████╔╝██║████╔╝██║██╔░░██╗██║██║╚██╗██║██║      #
#       ██║  ██║╚██████╔╝╚██████╔╝██████╔╝██║██║ ╚████║██║      #
#       ╚░╝  ╚░╝ ╚░░░░░╝  ╚░░░░░╝ ╚░░░░░╝ ╚░╝╚░╝  ╚░░░╝╚░╝      #
#                                                               #
#              Email    : roobini.gamer@protonmail.com          #
#              Instagram: https://bit.ly/3iX0ljO                #
#              Youtube  : https://bit.ly/2Emapnn                #
#              Facebook : https://bit.ly/3he568k                #
#              Github   : https://bit.ly/2E8gFzx                #
#                                                               #
#################################################################

from base64 import b64decode
from contextlib import closing
from os import devnull, geteuid, remove
from os.path import isfile
from random import choice
from subprocess import call
from sys import argv, exit, stderr
from urllib2 import urlopen


class VpnMe(object):
    def __init__(self, country="US"):
        self.country = country.upper()
        self.servers = list()
        self.get_serverlist()

    def save_config_file(self, server):
        print "[VPN-ME> writing config file"
        try:
            with open("/tmp/openvpnconf", "w") as config_file:
                config_file.write(
                    "\n".join(
                        str(b64decode(self.servers[server + 8])
                           ).split("\n")[:-1]
                    )
                )
        except:
            print "[VPN-ME> rewriting config file"
            self.get_serverlist()
        else:
            print "[VPN-ME> running openvpn\n"
            self.openvpn()

    def get_serverlist(self):
        if not self.country:
            self.country = "US"
        print "[VPN-ME> looking for %s" % self.country

        with closing(
            urlopen("https://www.vpngate.net/api/iphone/")
                    ) as serverlist:
            serverlist = serverlist.read().split(",")
            self.servers.extend([x for x in serverlist if len(serverlist) > 15])
            try:
                server = self.servers.index(self.country)
            except ValueError:
                exit(
                    "[\033[91m!\033[0m] Country code "
                    + "\033[93m"
                    + self.country
                    + "\033[0m"
                    + " not in server list"
                )
            else:
                self.save_config_file(server)

    def openvpn(self):
        fnull = open(devnull, "w")
        call(["openvpn", "--config", "%s" % "/tmp/openvpnconf"],
        stderr=fnull)

    @staticmethod
    def clean_up():
        if isfile("/tmp/openvpnconf"):
            remove("/tmp/openvpnconf")


if __name__ == "__main__":
    if geteuid() is not 0:
        exit("\033[91m[!]\033[0m Run as super user!")

    try:
        print "\033[96m" + "\n[VPN-ME] getting server list"
        print "[VPN-ME> parsing response"
        VpnMe("".join(argv[1:]))

    except KeyboardInterrupt:
        call(["killall", "-9", "openvpn"])
        call(["clear"])
        VpnMe.clean_up()
        retry = ("y", "yes")
        try:
            ans = raw_input(
                "\033[92m\n[VPN-ME>\033[93m try another VPN? (y/n)\033[0m " +
                "\033[92m"
            )
            if ans.lower() in retry:
                try:
                    servers = ("JP", "KR")
                    VpnMe(choice(servers))
                except:
                    VpnMe.clean_up()
        except:
            pass
