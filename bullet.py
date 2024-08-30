import pygame
from pygame.sprite import Sprite


class Bullet(Sprite):
    """a class to control bullets."""

    def __init__(self, ai_game):
        """Створити обʼєкт bullet у поточній позиції корябля."""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        # self.color = self.settings.bullet_color
        self.image = pygame.image.load("images/patriot_red.png")
        self.image = pygame.transform.scale(self.image, (80, 80))
        self.rect = self.image.get_rect()
        # self.rect = pygame.Rect(
        #     0, 0, self.settings.bullet_width, self.settings.bullet_height
        # )
        self.rect.midtop = ai_game.ship.rect.midtop
        self.y = float(self.rect.y)

    def update(self):
        """Посунути кулю нагору екраном."""
        # Оновити десяткову позицію кулі.
        self.y -= self.settings.bullet_speed
        # Оновити позицию rect.
        self.rect.y = self.y

    def draw_bullet(self):
        """Налаштувати кулю на екрані."""
        self.screen.blit(self.image, self.rect)
