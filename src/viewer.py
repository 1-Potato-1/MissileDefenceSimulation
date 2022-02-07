from typing import List

import cv2
import imageio
import numpy as np

from .defences import IDefenceProjectile, IDefence
from .missiles import IMissile
from .util import Vector
from .viewer_settings import ViewerSettings


class Viewer:
    """
    A simple viewer that creates images of the world state.
    """
    def __init__(self, viewer_settings: ViewerSettings):
        self.settings = viewer_settings
        self.frames = []

    def draw_frame(self, missiles: List[IMissile], projectiles: List[IDefenceProjectile], defences: List[IDefence]):
        """
        Draws frame for the current world state
        :param missiles: List of Missiles
        :param projectiles: List of Projectiles
        :param defences: List of Defences
        """
        # TODO It would be nicer to have something like: draw_frame(self, world_state: WorldState)

        img = np.zeros((self.settings.pixels_y, self.settings.pixels_x, 3), np.uint8)

        # create simple sky and ground background
        GROUND_PIXEL_HEIGHT = 10
        cv2.rectangle(img, (0, 0), (self.settings.pixels_x, self.settings.pixels_y),
                      color=(135, 206, 250), thickness=-1)
        cv2.rectangle(img, (0, 0), (self.settings.pixels_x, GROUND_PIXEL_HEIGHT),
                      color=(52, 140, 49), thickness=-1)

        # Image offsets to move world origin to lower center of image (actually upper center, but we flip later)
        offset = Vector()
        offset.x = int(self.settings.pixels_x/2)
        offset.y = GROUND_PIXEL_HEIGHT

        for missile in missiles:
            missile.draw(img, missile.p, offset)

        for projectile in projectiles:
            projectile.draw(img, projectile.p, offset)

        for defence in defences:
            defence.draw(img, defence.p, offset)

        img = cv2.flip(img, 0)
        self.frames.append(img)

    def export_gif(self, file_name: str, frame_rate: float):
        """
        Creates a gif file.
        :param file_name: File name of output file.
        :param frame_rate: Simulation frame rate.
        """
        num_frames = len(self.frames)
        frames = self.frames
        duration = 1/frame_rate
        # Workaround for an issue that saving large GIFS takes minutes
        GIF_FRAMES_CAP = 100
        if num_frames > GIF_FRAMES_CAP:
            stride = int(np.ceil(num_frames / GIF_FRAMES_CAP))
            duration *= stride
            frames = frames[slice(0, len(frames), stride)]

        imageio.mimsave(file_name, frames, duration=duration)


