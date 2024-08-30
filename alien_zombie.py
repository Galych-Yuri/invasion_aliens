import pygame
from pygame.sprite import Sprite


class AlienZombie(Sprite):
    """Клас, що представляє одного прибульця з навали."""
    def __init__(self, ai_game):
        """Ініціалізувати зомбі та задати його початкову позицію."""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings

        # Завантажити зображення та визначити його rect
        self.image = pygame.image.load("images/zombie-russ/zombie_1_red.png")
        self.image = pygame.transform.scale(self.image, (70, 70))
        self.rect = self.image.get_rect()

        # Start each new zombie near the top left of the screen.
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # Store the zombie exact horizontal position
        self.x = float(self.rect.x)

    def check_edges(self):
        """Повертає істину,якщо зобак знаходиться на краю екрана."""
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right or self.rect.left <= 0:
            return True

    def update(self):
        """Змістити зомбаків праворуч."""
        self.x += (self.settings.alien_speed * self.settings.fleet_direction)
        self.rect.x = self.x


