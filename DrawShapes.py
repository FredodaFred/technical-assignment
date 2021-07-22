import cv2 as cv
import Colors as color
import numpy as np
import csv
import random
from datetime import datetime #for seeding rng, also timestamping in the csv
import os

class Pen():

    def __init__(self):
        self.width = 600
        self.height = 600
        self.blank = np.zeros((600,600, 3), dtype = 'uint8') #2d (square) array filled with unsigned 8bit zeros, 3 color channels, not that anyone really needed to know that

    def draw(self, shape : str):
        if not type(shape) is str:
            print("invalid parameter")
            return

        shape.lower() #for reasons
        if shape == 'square':
            cv.rectangle(self.blank, (150,150), (400, 400), color.GREEN, thickness = 2)
        elif shape == 'rectangle':
            cv.rectangle(self.blank, (150,100), (350, 450), color.GREEN, thickness = 2)
        elif shape == 'circle':
            cv.circle(self.blank, (250,250), 100, color.GREEN, thickness = 2)
        elif shape == 'triangle':
            cv.line(self.blank, (250, 0), (0, 250), color.GREEN, thickness = 2)
            cv.line(self.blank, (0, 250), (250, 250), color.GREEN, thickness = 2)
            cv.line(self.blank, (250,250), (250, 0), color.GREEN, thickness = 2)
        elif shape == 'trapezoid':
            cv.line(self.blank, (100, 100), (350,100), color.GREEN, thickness = 2)
            cv.line(self.blank, (100, 100), (25,275), color.GREEN, thickness = 2)
            cv.line(self.blank, (25,275), (425, 275), color.GREEN, thickness = 2)
            cv.line(self.blank, (425, 275), (350, 100), color.GREEN, thickness =2)
        elif shape == 'parallelogram':
            cv.line(self.blank, (150, 150), (400, 150), color.GREEN, thickness = 2)
            cv.line(self.blank, (400, 150), (300, 400), color.GREEN, thickness = 2)
            cv.line(self.blank, (300,400), (50, 400), color.GREEN, thickness = 2)
            cv.line(self.blank, (50, 400), (150,150), color.GREEN, thickness = 2)
        elif shape == 'ellipse':
            cv.ellipse(self.blank, (300, 300), (200, 100), 0, 0, 360, color.GREEN, thickness = 2)
        else:
            print("invalid shape")

    def clear(self):
        self.blank[:] = color.BLACK

    def draw_crossSection(self, eccentricity:float, min:float, max: float):
        self.clear() #eccentricity is not used
        #min and max are diameters, we can use this to calculate the area if we divide by 2 (pi*min*max)
        min_radius = int(min/2) #we need to make them ints
        max_radius = int(max/2)
        cv.ellipse(self.blank, ( int(self.width/2), int(self.height/2)), (max_radius, min_radius), 0, 0, 360, color.GREEN, thickness = 2)


    def draw_arc(self, curve, length):
        self.clear() #Length is not used
        radius = int(1/curve * (self.width/4)) #radius = 1/curvature, then scaled
        dt = datetime.now()
        random.seed(dt.microsecond)
        startAngle = random.randint(0, 150)
        endAngle = random.randint(200, 360)
        cv.ellipse(self.blank, (int(self.width/2), int(self.height/2)), (radius, radius), 0, startAngle, endAngle, color.GREEN, thickness = 2)

    def read_list(self, list):
        """
            This the most important method, as it complete the project. It reads
            a list of strings, generates the images and csv file into a csv folder
        """
        self.clear()
        #create and enter output directory
        if not os.path.isdir('output'):
            os.mkdir('output')
        current_dir = os.getcwd()
        os.chdir('output')

        file = open('shape_data.csv', 'a', newline = '') #append mode because it makes it compatible with the GUI
        writer = csv.writer(file)

        for item in list:
            if type(item) == str:
                if item == 'sectional':
                    dt = datetime.now()
                    random.seed(dt.microsecond)
                    max = random.randint(100, 250)
                    min = random.randint(50, max)
                    self.draw_crossSection(None, min, max)
                    writer.writerow(['sectional',f"max ={max}", f"min ={min}", datetime.now()])
                    cv.imwrite(f"{item}_{id(item)}.png", self.blank)
                elif item == 'arc':
                    dt = datetime.now()
                    random.seed(dt.microsecond)
                    curve = random.uniform(.5,1)
                    self.draw_arc(curve, None)
                    writer.writerow(['arc', f"curve = {curve}", datetime.now()])
                    cv.imwrite(f"{item}_{id(item)}.png", self.blank)
                else:
                    self.draw(item)
                    writer.writerow([item, datetime.now()])
                    cv.imwrite(f"{item}_{id(item)}.png", self.blank)
                self.clear()

        file.close()
        os.chdir(current_dir)
