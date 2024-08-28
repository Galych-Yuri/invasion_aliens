import sys
import pygame

from settings import Settings
from ship import Ship


class AlienInvasion:
    """Загальний клас, що керує ресурсами гри."""

    def __init__(self):
        """Ініціалізувати гру, створити ресурси гри."""
        pygame.init()
        self.settings = Settings()

        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height)
        )
        pygame.display.set_caption("Alian Invasion")

        self.ship = Ship(self)

        # Задати колір фону.
        self.bg_color = (230, 230, 230)

    def run_game(self):
        """Розпочати головний цикл гри."""
        while True:
            self._check_events()
            self._update_screen()

    def _check_events(self):
        """Слідкувати за подіями миші та клавіарути."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    # Перемістити корабель праворуч
                    self.ship.rect.x += 1

    def _update_screen(self):
        """
        Наново перемалювати екран на кожній ітерації циклу.
        Показати останній намальований екран.
        """
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()
        pygame.display.flip()


if __name__ == '__main__':
    # Створити екземпляр гри та запустити гру
    ai = AlienInvasion()
    ai.run_game()
