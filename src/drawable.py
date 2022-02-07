from abc import abstractmethod
from typing import Type

import cv2

from .util import Vector


class IShape:
    @staticmethod
    @abstractmethod
    def draw(image_obj, position: Vector, image_offset: Vector, rgb: tuple, scale: float):
        """
        Interface for drawing a shape onto the image object.
        :param image_obj: A three dimensional array representing the image.
        :param position: The center point where to draw the shape
        :param image_offset: offsets to compensate for image object coordinates being different from world coordinates
        :param rgb: A tuple containing (r,g,b) on a range from 0 to 255
        :param scale: Scaling factor of the shape
        :return:
        """
        pass


class Drawable:
    """Interface for objects to become drawable on an rgb grid"""
    def __init__(self, shape: Type[IShape], scale=1, rgb=(255, 255, 255)):
        self.scale = scale
        self.rgb = rgb
        self.shape: Type[IShape] = shape

    def draw(self, image_obj, p: Vector, image_offset: Vector):
        """
        Draws itself onto the image object
        :param image_obj: A three dimensional array representing the image.
        :param p: a position of drawable object
        :param image_offset: offsets to compensate for image object coordinates being different from world coordinates
        :return:
        """
        self.shape.draw(image_obj, p, image_offset, self.rgb, self.scale)


class Circle(IShape):
    @staticmethod
    def draw(image_obj, p: Vector, image_offset: Vector, rgb, scale: float):
        x = int(p.x + image_offset.x)
        y = int(p.y + image_offset.y)
        cv2.circle(image_obj, (x, y), scale, rgb, -1)


class Square(IShape):
    @staticmethod
    def draw(image_obj, p: Vector, image_offset: Vector, rgb, scale: float):
        x = int(p.x + image_offset.x - scale/2)
        y = int(p.y + image_offset.y - scale/2)
        scale = int(scale)
        cv2.rectangle(image_obj, (x, y), (x+scale, y+scale), rgb, -1)