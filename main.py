from io import BytesIO
import pygame_gui

import pygame
from api_library import *

KEYS = [pygame.K_PAGEUP, pygame.K_PAGEDOWN, pygame.K_RIGHT,
        pygame.K_LEFT, pygame.K_DOWN, pygame.K_UP, pygame.K_RETURN]


class BigMap:
    options = ['map', 'sat', 'sat,skl']

    def __init__(self):
        self.image = None
        self.lon, self.lat = get_toponym_coord(get_toponym(geocoder('Миасс')))
        self.layer = 'map'
        self.z = 17
        self.point = None

        self.manager = pygame_gui.UIManager(SIZE)
        self.layers_select = (pygame_gui.elements.UIDropDownMenu(self.options, self.options[0],
                                                                 pygame.Rect(440, 10, 200, 30),
                                                                 self.manager))
        self.search_field = pygame_gui.elements.UITextEntryLine(pygame.Rect(175, 410, 300, 30), self.manager)
        self.error_field = pygame_gui.elements.UILabel(
            pygame.Rect(150, 380, 450, 30), '', self.manager)
        # self.error_field.bg_colour = 'black'
        # self.error_field.text_colour = 'black'
        # self.error_field.disabled_text_colour = 'black'
        # self.error_field.text_shadow_colour = 'black'
        self.update_map()

    def update_map(self):
        map_params = {
            "ll": ",".join(map(str, (self.lon, self.lat))),
            'z': self.z,
            "l": self.layer,
            'size': '650,450'
        }
        if self.point is not None:
            map_params['pt'] = ','.join(map(str, self.point)) + ',flag'
        image = BytesIO(get_static(**map_params))
        self.image = pygame.image.load(image)

    def event_handler(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_PAGEUP:
                self.z = min(self.z + 1, 21)
            if event.key == pygame.K_PAGEDOWN:
                self.z = max(self.z - 1, 0)
            if event.key == pygame.K_LEFT:
                self.lon = (self.lon + 180 - 200 * 2 ** (-self.z)) % 360 - 180
            if event.key == pygame.K_RIGHT:
                self.lon = (self.lon + 180 + 200 * 2 ** (-self.z)) % 360 - 180
            if event.key == pygame.K_UP:
                self.lat = min(self.lat + 70 * 2 ** (-self.z), 89)
            if event.key == pygame.K_DOWN:
                self.lat = max(self.lat - 70 * 2 ** (-self.z), -89)
            if event.key == pygame.K_RETURN:
                text = self.search_field.get_text()
                if text:
                    try:
                        self.lon, self.lat = get_toponym_coord(get_toponym(geocoder(text)))
                        self.error_field.set_text('')
                        self.point = self.lon, self.lat
                    except IndexError:
                        self.error_field.set_text('Ничего не найдено!')
            if event.key in KEYS:
                self.update_map()
        self.manager.process_events(event)

    def gui_event_handler(self, event):
        if event.type == pygame_gui.UI_DROP_DOWN_MENU_CHANGED:
            if event.ui_element == self.layers_select:
                self.layer = event.text
                self.update_map()

    def draw(self, surf):
        surf.blit(self.image, (0, 0))
        self.manager.draw_ui(surf)

    def update_gui(self, delta):
        self.manager.update(delta)


pygame.init()
SIZE = WIDTH, HEIGHT = 650, 450
screen = pygame.display.set_mode(SIZE)
clock = pygame.time.Clock()

app = BigMap()

running = True

while running:
    time_delta = clock.tick(60) / 1000.0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        app.event_handler(event)
        app.gui_event_handler(event)
    screen.fill('black')
    app.update_gui(time_delta)
    app.draw(screen)
    pygame.display.flip()
pygame.quit()
