import os


os.environ['MPLCONFIGDIR'] = os.getcwd() + "/ configs/"


import matplotlib.pyplot as plt


class Pie:
    def __init__(self, labels, sizes):
        self.labels = labels
        self.sizes = sizes
        self.draw()

    def draw(self):
        pas, wind = plt.subplots()
        wind.pie(self.sizes, labels=self.labels)
        wind.axis('equal')  
        plt.show()

