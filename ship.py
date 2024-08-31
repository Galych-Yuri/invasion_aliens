"""class Ship module. Керує майже всією поведінкою корабля"""

import pygame
from pygame.sprite import Sprite


class Ship(Sprite):
    """class to control Ship in game"""

    def __init__(self, ai_game):
        """Ініціалізувати корабель та задати його початкову позицію."""
        super().__init__()
        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()
        self.settings = ai_game.settings

        # Download ship image $ take him rect
        self.image = pygame.image.load("images/f-16_red.png")
        # self.image = pygame.transform.scale(self.image, (0, 0))
        # self.image = pygame.transform.rotate(self.image, 270.0)
        self.rect = self.image.get_rect()

        # create any new ship center-bottom
        self.rect.midbottom = self.screen_rect.midbottom

        # Зберегти десяткове значення для позиції корабля по горизонталі.
        self.x = float(self.rect.x)

        # Індикатори руху.
        self.moving_right = False
        self.moving_left = False

    def update(self):
        """
        Оновити поточну позицію корабля на
        основі індикатора руху.
        """
        # Оновити значення x корабля, а не rect.
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.ship_speed
        if self.moving_left and self.rect.left > 0:
            self.x -= self.settings.ship_speed

        # Оновити обʼєкт rect з self.x.
        self.rect.x = self.x

    def blitme(self):
        """Намалювати корабель у його поточному розташуванні."""
        self.screen.blit(self.image, self.rect)

    def center_ship(self):
        """Відцентрувати корабель на екрані."""
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)

    def resize_ship(self, scale=(40, 40)):
        """Змінити розмір корабля для відображення життів."""
        self.image = pygame.transform.scale(self.image, scale)
        self.rect = self.image.get_rect()
