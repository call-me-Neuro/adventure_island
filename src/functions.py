import sys

import pygame
from PIL import Image


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

if __name__ == '__main__':
    l = split_animated_gif(f'../{MEDIA}/animations/character/__Run.gif')
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    screen.fill((0, 0, 0))
    i = 0
    clock = pygame.time.Clock()
    while True:
        screen.fill((0, 0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
        screen.blit(l[i%len(l)], l[i%len(l)].get_rect())
        i+=1
        clock.tick(60)
        pygame.display.update()

