from LedWall import Grid
import Simulate
import LedWallScenes as Scenes

import tkinter as tk
import time
import logging
import threading
import multiprocessing

class TouchInterface:
    def __init__(self):
        self.pixelGrid = Grid()
        self.InitializeInterface()

    def Start(self):
        self.StopSimulation = multiprocessing.Value('i', int(False))
        self.window.mainloop()

    def InitializeInterface(self):
        self.window = tk.Tk()
        buttons = []
        buttons.append(tk.Button(
            text="Stop",
            width=25,
            height=5,
            command=self.Stop
        ))

        buttons.append(tk.Button(
            text="Camera",
            width=25,
            height=5,
            command=self.StartCamera
        ))

        buttons.append(tk.Button(
            text="Waterfall",
            width=25,
            height=5,
            command=self.Waterfall
        ))

        for button in buttons:
            button.pack()
        self.threads = []

    def StartCamera(self):
        self.threads = [x for x in self.threads if x.is_alive()]
        while len(self.threads) > 0:
            self.StopSimulation.value = True
            self.threads = [x for x in self.threads if x.is_alive()]
        self.StopSimulation.value = False
        simulator = Simulate.Simulator(self.pixelGrid)
        worker_thread = threading.Thread(target=simulator.Camera, args=(self.StopSimulation,))
        self.threads.append(worker_thread)
        worker_thread.start()

    def Stop(self):
        self.StopSimulation.value = True

    def Waterfall(self):
        self.threads = [x for x in self.threads if x.is_alive()]
        while len(self.threads) > 0:
            self.StopSimulation.value = True
            self.threads = [x for x in self.threads if x.is_alive()]
        self.StopSimulation.value = False
        simulator = Simulate.Simulator(self.pixelGrid)
        scene = Scenes.Waterfall(self.pixelGrid)
        worker_thread = threading.Thread(target=simulator.Run, args=(scene, self.StopSimulation,))
        self.threads.append(worker_thread)
        worker_thread.start()


if __name__ == "__main__":
    touchInterface = TouchInterface()
    touchInterface.Start()

