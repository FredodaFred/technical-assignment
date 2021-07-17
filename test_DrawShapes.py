import unittest
from DrawShapes import Pen
import datetime
import time
import random

class TestDrawShapes(unittest.TestCase):

    """
    def test_draw_arc(self):
        for i in range(10):
            pen = Pen()
            curve = random.uniform(.5, 1)
            pen.draw_arc(curve, None)
            time.sleep(1.5)
            pen.clear()
        """

    def test_read_list(self):
        pen = Pen()
        shapes = ['circle', 'square', 'rectangle', 'parallelogram', 'triangle', 'trapezoid', 'arc', 'sectional']

        pen.read_list(shapes)


if __name__ == '__main__':
    unittest.main()
