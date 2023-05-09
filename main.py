import os
import sys
import time
import socket
import math
import random
from toolConfigurator import Configure, VarData, Var
from opcua import ua, Server


from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.properties import ObjectProperty, StringProperty, NumericProperty
from kivy.uix.textinput import TextInput
from kivy.clock import Clock

sys.path.insert(0, "..")


def get_local_ip():
    ip = [(s.connect(('127.1.1.0', 53)), s.getsockname()[0], s.close()) for s in
            [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]
    ip = '127.1.1.0'
    return ip


class Console(Label):
    text = StringProperty(None)

    def on_size(self, *args):
        self.text_size = self.size

    def Clear(self):
        self.text = ''

    def Add(self, text):
        self.text = str(self.text) + '\n' + text


def TGetValue(_name):
    if _name == "txc":
        return 50.
    elif _name == "T1вхM1Г":
        return 250.
    elif _name == "G4":
        return 25.
    elif _name == "U1":
        return 220.
    else:
        return 0.


def DataUpdate():
    str = ''
    for i in range(5):
        if i == 4:
            str += f'TEST{i}'
        else:
            str += f'TEST{i}\t'
    str += '\n'
    for i in range(5):
        if i == 0:
            value = 'False'
        else:
            value = random.randint(-50, 50) / 10
        if i == 4:
            str += f'{value}'
        else:
            str += f'{value}\t'
    return str


class ServerKivyApp(App):
    isRunning = False
    console = Console()

    T = 0

    def update(self, dt):
        self.console.Clear()
        self.T += dt
        self.console.Add("opc.tcp://" + str(get_local_ip()) + ":4840")
        for i in VarArray[:-1]:
            if i.getData().GetName() == 'G4':
                self.console.Add(str(i.getData().GetName() + ": " + str(round(i.getVar().get_value(), 2))))
            else:
                i.getVar().set_value(TGetValue(i.getData().GetName()) + 10 * math.sin(2 * math.pi * self.T * 0.05) + 100 * math.sin(2 * math.pi * self.T * 0.0025) + 20 * math.sin(2 * math.pi * self.T * 0.2))
                self.console.Add(str(i.getData().GetName() + ": " + str(round(i.getVar().get_value(), 2))))
        # VarArray[-1].getVar().set_value(DataUpdate())
        self.console.Add(VarArray[-1].getVar().get_value())

    def build(self):
        self.isRunning = True
        Clock.schedule_interval(self.update, 1)

        return self.console

    def on_stop(self):
        self.isRunning = False


if __name__ == "__main__":

    # setup our server
    server = Server()
    server.set_endpoint("opc.tcp://" + str(get_local_ip()) + ":4840")

    name = "TEST SERVER"
    namespace = server.register_namespace(name)

    # get Objects node, this is where we should put our nodes
    root = server.get_root_node()
    objects = server.get_objects_node()

    # populating our address space
    laboratory1 = objects.add_object(namespace, "laboratory1")
    VarConfiguredArray = Configure("config.ic")
    VarArray = []
    for element in VarConfiguredArray:
        if element.name == 'test':
            temp = laboratory1.add_variable(namespace, element.name, DataUpdate())
            temp.set_writable()
            VarArray.append(Var(element, temp))
        else:
            temp = laboratory1.add_variable(namespace, element.name, 0)
            temp.set_writable()
            VarArray.append(Var(element, temp))
    NumVar = len(VarArray)
    try:
        # starting!
        server.start()
        ServerKivy = ServerKivyApp()
        ServerKivy.run()
    finally:
        # close connection, remove subcsriptions, etc
        server.stop()
