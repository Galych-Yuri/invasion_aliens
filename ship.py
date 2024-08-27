"""class Ship module. Керує майже всією поведінкою корабля"""

import pygame


class Ship:
    """class to control Ship in game"""

    def __init__(self, ai_game):
        """Ініціалізувати корабель та задати його початкову позицію."""
        self.screen = ai_game.screen
        self.screen.rect = ai_game.screen.get_rect()

        # Download ship image $ take him rect
        self.image = pygame.image.load("images/ship.png")
        self.rect = self.image.get_rect()

        # create any new ship crnter-bottom
        self.rect.midbottom = self.screen.rect.midbottom

    def blitme(self):
        """Намалювати корабель у його поточному розташуванні."""
        self.screen.blit(self.image, self.rect)
