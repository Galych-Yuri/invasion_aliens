import sys
import pygame


class AlianInvasion:
    """Загальний клас, що керує ресурсами гри."""

    def __init__(self):
        """Ініціалізувати гру, створити ресурси гри."""
        pygame.init()

        self.screen = pygame.display.set_mode((1200, 800))
        pygame.display.set_caption("Alian Invasion")

    def run_game(self):
        """Розпочати головний цикл гри."""
        while True:
            # Слідкувати за подіями миші та клавіарути.
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

            # Показати останній намальований екран.
            pygame.display.flip()


if __name__ == '__main__':
    # Створити екземпляр гри та запустити гру
    ai = AlianInvasion()
    ai.run_game()
