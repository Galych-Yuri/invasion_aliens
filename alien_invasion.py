import sys
from time import sleep
import pygame

from settings import Settings
from game_stats import GameStats
from button import Button
from ship import Ship
from bullet import Bullet
from alien_zombie import AlienZombie


class AlienInvasion:
    """Загальний клас, що керує ресурсами гри."""

    def __init__(self):
        """Ініціалізувати гру, створити ресурси гри."""
        pygame.init()
        self.settings = Settings()

        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height
        pygame.display.set_caption("Alian Invasion")

        # Створити екземпляр для збереження ігрової статистики.
        self.stats = GameStats(self)

        self.ship = Ship(self)
        self.aliens = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()
        self._create_fleet()
        # Задати колір фону.
        self.bg_color = self.settings.bg_color

        # Create PlayButton
        self.play_button = Button(self, "Зіграти")

    def run_game(self):
        """Розпочати головний цикл гри."""
        while True:
            self._check_events()
            if self.stats.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()
            self._update_screen()

    def _create_fleet(self):
        """Create fleet zombie"""
        alien = AlienZombie(self)
        alien_width, alien_height = alien.rect.size
        alien_width = alien.rect.width
        available_space_x = self.settings.screen_width - (2 * alien_width)
        number_alians_x = available_space_x // (2 * alien_width)
        # Визначити яка кількість рядів поміщається на екрані.
        ship_height = self.ship.rect.height
        available_space_y = (self.settings.screen_height -
                             (3 * alien_height) - ship_height)
        number_rows = available_space_y // (2 * alien_height)
        # Створити повний набір зомбаків.
        for row_number in range(number_rows):
            for alien_number in range(number_alians_x):
                self._create_alien(alien_number, row_number)

    def _create_alien(self, alien_number, row_number):
        """Створити прибульця та поставити його до ряду."""
        alien = AlienZombie(self)
        alien_width, alien_height = alien.rect.size
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
        self.aliens.add(alien)

    def _check_fleet_edges(self):
        """
        Реагує відповідно до того, чи досяг котрийсь
        із прибульців краю екрана.
        """
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _check_aliens_bottom(self):
        """Перевірити, чи не досяг якийсь зомбач нижнього краю екрана."""
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                # Зреагувати так ніби корабель підбито.
                self._ship_hit()
                break

    def _change_fleet_direction(self):
        """Спуск всього флоту та зміна його напрямку."""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _check_events(self):
        """Слідкувати за подіями миші та клавіарути."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)

    def _check_play_button(self, mouse_pos):
        """Розпочати нову гру, коли користувач натисне кнопку 'Зіграти'."""
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if self.play_button.rect.collidepoint(mouse_pos):
            # Анулювати ігрову статистику.
            self.stats.reset_stats()
            self.stats.game_active = True

            # Позбавитися надлишку зомбаків та куль.
            self.aliens.empty()
            self.bullets.empty()

            # Створити новий флот та відцентрувати корабель.
            self._create_fleet()
            self.ship.center_ship()

            # Hide mouse cursor
            self.mouse.set_visible(False)

    def _check_keydown_events(self, event):
        """Реагувати на натискання клавіш."""
        if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
            # Перемістити корабель праворуч або ліворуч
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
            self.ship.moving_left = True
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()

    def _check_keyup_events(self, event):
        """Реагувати коли клавіша не натиснута."""
        if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
            self.ship.moving_left = False

    def _fire_bullet(self):
        """Створити нову кулю та додати її до групи куль."""
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _update_bullets(self):
        """Оновити позицію куль та позбавитися старих куль."""
        # Оновити позиції куль
        self.bullets.update()

        # Позбавитися старих куль.
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

        self._check_bullet_alien_collisions()

    def _check_bullet_alien_collisions(self):
        """Реакція на зіткнення куль з зомбаками."""
        # Видалити всі кулі та зомбаків, що зіткнулися.
        collisions = pygame.sprite.groupcollide(
            self.bullets, self.aliens, True, True)
        if not self.aliens:
            # Знищити наявні кулі та створити новий флот зомбаків.
            self.bullets.empty()
            self._create_fleet()

    def _update_aliens(self):
        """
        Перевірити, чи флот знаходиться на краю,
        тоді оновити позиції всіх прибульців флоту.
        """
        self._check_fleet_edges()
        self.aliens.update()

        # Шукати зіткнення ракет з зомбаками.
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()

        # Шукати, чи котрийсь із зомбаків досяг краю екрана.
        self._check_aliens_bottom()

    def _ship_hit(self):
        """Реагувати на зіткення корабля з зомбаком."""
        if self.stats.ships_left > 0:
            # Зменшити ships_left.
            self.stats.ships_left -= 1

            # Позбавитися надлишку зомбаків та куль.
            self.aliens.empty()
            self.bullets.empty()

            # Створити новий флот та відцентрувати корабель.
            self._create_fleet()
            self.ship.center_ship()

            # Sleep.
            sleep(0.5)
        else:
            self.stats.game_active = False
            pygame.mouse.set_visible(True)

    def _update_screen(self):
        """
        Наново перемалювати екран на кожній ітерації циклу.
        Показати останній намальований екран.
        """
        self.screen.fill(self.settings.bg_color)
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.aliens.draw(self.screen)
        self.ship.blitme()
        # Намалювати кнопку "Зіграти" коли гра неактивна.
        if not self.stats.game_active:
            self.play_button.draw_button()
        pygame.display.flip()


if __name__ == '__main__':
    # Створити екземпляр гри та запустити гру
    ai = AlienInvasion()
    ai.run_game()

# Задані параметри вікна (1200, 800) in __init__
# self.screen = pygame.display.set_mode(
#     (self.settings.screen_width, self.settings.screen_height)
# )
