import sys

import pygame
from PIL import Image
from copy import copy

MEDIA = '../media'
WIDTH = 800
HEIGHT = 600


def split_animated_gif(gif_file_path):
    ret = []
    gif = Image.open(gif_file_path)
    for frame_index in range(gif.n_frames):
        gif.seek(frame_index)
        frame_rgba = gif.convert("RGBA")
        pygame_image = pygame.image.fromstring(
            frame_rgba.tobytes(), frame_rgba.size, frame_rgba.mode
        )
        ret.append(pygame_image)
    return ret


def get_animation_sheet(path, frames):
    images = []
    img = pygame.image.load(path).convert_alpha()
    size = img.get_size()
    for i in range(frames):
        surface = pygame.Surface((size[0]/frames, size[1]))
        surface.blit(img, (size[0]/frames*i*-1, 0))
        images.append(surface)
    return images

def get_animation_sheet2(path, frames):
    images = []
    img = pygame.image.load(path).convert_alpha()
    size = img.get_size()
    for i in range(frames):
        images.append(img.subsurface(i * size[0]/frames, 0, size[0]/frames, size[1]))
    return images
