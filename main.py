import os
import sys
from io import BytesIO

import pygame
from api_library import get_static


class BigMap:
    def __init__(self):
        self.image = None
        self.ll = 60.153191, 55.156353
        self.layer = 'map'
        self.z = 17
        self.update_map()

    def update_map(self):
        map_params = {
            "ll": ",".join(map(str, self.ll)),
            'z': self.z,
            "l": "map",
            'size': '650,450'
        }
        image = BytesIO(get_static(**map_params))
        self.image = pygame.image.load(image)

    def event_hendler(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_PAGEUP:
                self.z = min(self.z + 1, 21)
            if event.key == pygame.K_PAGEDOWN:
                self.z = max(self.z - 1, 0)
            self.update_map()

    def draw(self, surf):
        surf.blit(self.image, (0, 0))


pygame.init()
FPS = 50
SIZE = WIDTH, HEIGHT = 650, 450
screen = pygame.display.set_mode(SIZE)
clock = pygame.time.Clock()

all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()

app = BigMap()

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        app.event_hendler(event)
    screen.fill('black')
    app.draw(screen)
    pygame.display.flip()
    clock.tick(FPS)
