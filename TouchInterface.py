import tkinter as tk
from LedWall import Grid
import Simulate
import LedWallScenes as Scenes
import multiprocessing
import threading
import time
import logging

class TouchInterface:
    def __init__(self):
        self.pixelGrid = Grid()
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
        self.StopSimulation = multiprocessing.Value('i', int(False))

    def Start(self):
        self.window.mainloop()

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
    fmt = '%(levelname)s: %(filename)s: %(lineno)d: %(message)s'
    logging.basicConfig(level=logging.DEBUG, format=fmt)

    touchInterface = TouchInterface()
    touchInterface.Start()

