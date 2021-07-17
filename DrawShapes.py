import cv2 as cv
import Colors as color
import numpy as np
import csv
import random
from datetime import datetime #for seeding rng
import os

class Pen():

    def __init__(self):
        #2d (square) array filled with unsigned 8bit zeros, 3 color channels
        self.width = 600
        self.height = 600
        self.blank = np.zeros((600,600, 3), dtype = 'uint8') #this is our canvas

    def draw(self, shape : str):

        if not type(shape) is str:
            print("invalid parameter")
            return

        shape.lower()
        if shape == 'square':
            cv.rectangle(self.blank, (150,150), (400, 400), color.GREEN, thickness = 2)
            cv.imshow("Shape", self.blank)
        elif shape == 'rectangle':
            cv.rectangle(self.blank, (150,100), (350, 450), color.GREEN, thickness = 2)
            cv.imshow("Shape", self.blank)
        elif shape == 'circle':
            cv.circle(self.blank, (250,250), 100, color.GREEN, thickness = 2)
            cv.imshow("Shape", self.blank)
        elif shape == 'triangle':
            cv.line(self.blank, (250, 0), (0, 250), color.GREEN, thickness = 2)
            cv.line(self.blank, (0, 250), (250, 250), color.GREEN, thickness = 2)
            cv.line(self.blank, (250,250), (250, 0), color.GREEN, thickness = 2)
            cv.imshow("Shape", self.blank)
        elif shape == 'trapezoid':
            cv.line(self.blank, (100, 100), (350,100), color.GREEN, thickness = 2)
            cv.line(self.blank, (100, 100), (25,275), color.GREEN, thickness = 2)
            cv.line(self.blank, (25,275), (425, 275), color.GREEN, thickness = 2)
            cv.line(self.blank, (425, 275), (350, 100), color.GREEN, thickness =2)
            cv.imshow("Shape", self.blank)
        elif shape == 'parallelogram':
            cv.line(self.blank, (150, 150), (400, 150), color.GREEN, thickness = 2)
            cv.line(self.blank, (400, 150), (300, 400), color.GREEN, thickness = 2)
            cv.line(self.blank, (300,400), (50, 400), color.GREEN, thickness = 2)
            cv.line(self.blank, (50, 400), (150,150), color.GREEN, thickness = 2)
            cv.imshow("Shape", self.blank)
        elif shape == 'ellipse':
            cv.ellipse(self.blank, (300, 300), (200, 100), 0, 0, 360, color.GREEN, thickness = 2)
            cv.imshow("Shape", self.blank)
        else:
            print("invalid shape")
        cv.waitKey(0)
    def clear(self):
        self.blank[:] = color.BLACK
    def draw_crossSection(self, eccentricity:float, min:float, max: float):
        self.clear()
        #min and max are diameters, we can use this to calculate the area if we divide by 2 (pi*min*max)
        min_radius = int(min/2) #we need to make them ints
        max_radius = int(max/2)
        cv.ellipse(self.blank, ( int(self.width/2), int(self.height/2)), (max_radius, min_radius), 0, 0, 360, color.GREEN, thickness = 2)
        cv.imshow("sectional", self.blank)
        cv.waitKey(0)

    def draw_arc(self, curve, length):
        self.clear()
        radius = int(1/curve * (self.width/4)) #radius = 1/curvature, then scaled
        dt = datetime.now()
        random.seed(dt.microsecond)
        startAngle = random.randint(0, 150)
        endAngle = random.randint(200, 360)
        cv.ellipse(self.blank, (int(self.width/2), int(self.height/2)), (radius, radius), 0, startAngle, endAngle, color.GREEN, thickness = 2)
        cv.imshow("arc", self.blank)
        cv.waitKey(0)

    def read_list(self, list):
        self.clear()
        #create and enter output directory
        if not os.path.isdir('output'):
            os.mkdir('output')
        os.chdir('output')

        file = open('shape_data.csv', 'w', newline = '')
        writer = csv.writer(file)

        for item in list:
            if type(item) == str:
                if item == 'sectional':
                    dt = datetime.now()
                    random.seed(dt.microsecond)
                    max = random.randint(100, 250)
                    min = random.randint(50, max)
                    self.draw_crossSection(0.0, min, max)
                    writer.writerow(['sectional',f"max ={max}", f"min ={min}"])
                    cv.imwrite(f"{item}_{id(item)}.png", self.blank)
                elif item == 'arc':
                    dt = datetime.now()
                    random.seed(dt.microsecond)
                    curve = random.uniform(.5,1)
                    self.draw_arc(curve, None)
                    writer.writerow(['arc', f"curve = {curve}"])
                    cv.imwrite(f"{item}_{id(item)}.png", self.blank)
                else:
                    self.draw(item)
                    writer.writerow([item])
                    cv.imwrite(f"{item}_{id(item)}.png", self.blank)
                self.clear()

        file.close()
