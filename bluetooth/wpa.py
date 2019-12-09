# file used to interact with the wpa cli tools
import subprocess


class wpa:
    def __init__(self, commands):
        self.commands = commands
    
    def execute(self):
        str = "wpa_cli <<EOF\nadd_network\n"
        for command in self.commands:
            str += "set_network 0 {}\n".format(command)
        str += "EOF"
        print(str)
