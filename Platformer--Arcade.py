#!/usr/bin/env python
import arcade

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 800
SCREEN_TITLE = 'Platformer'

MAX_SPEED = 4
FRICTION = 0.05


class Player(arcade.Sprite):

    def __init__(self, image, image_scaling):
        super(Player, self).__init__(image, image_scaling)

        self.direction = 0
        self.color = arcade.csscolor.BLUE
        self.speed_multiplier = 1

    def gravity(self):
        self.change_y -= 0.18 * self.speed_multiplier

        if self.top >= SCREEN_HEIGHT and self.change_y > 0:
            self.change_y = 0
            self.top = SCREEN_HEIGHT
        elif self.bottom <= 0 and self.change_y < 0:
            self.change_y = 0
            self.bottom = 0

    def jump(self):
        self.change_y = 7

    def swap_color(self):
        if self.color == arcade.csscolor.BLUE:
            self.color = arcade.csscolor.YELLOW
        else:
            self.color = arcade.color.BLUE

    def update(self):
        self.gravity()

        if (self.right >= SCREEN_WIDTH and self.change_x > 0) or (self.left <= 0 and self.change_x < 0):
            self.change_x = 0

        if self.direction == 1:
            if self.change_x > -MAX_SPEED:
                self.change_x -= 0.1 * self.speed_multiplier
        elif self.direction == 2:
            if self.change_x < MAX_SPEED:
                self.change_x += 0.1 * self.speed_multiplier
        else:
            if self.change_x > FRICTION * self.speed_multiplier:
                self.change_x -= FRICTION * self.speed_multiplier
            elif self.change_x < -FRICTION * self.speed_multiplier:
                self.change_x += FRICTION * self.speed_multiplier
            else:
                self.change_x = 0

        self.center_x += self.change_x * self.speed_multiplier
        self.center_y += self.change_y * self.speed_multiplier


class Game(arcade.Window):

    def __init__(self, width, height, title, update_rate):
        super().__init__(width, height, title, update_rate=update_rate)

        self.player_list = None
        self.player_sprite = None

        arcade.set_background_color(arcade.color.YELLOW)

    def setup(self):
        self.player_list = arcade.SpriteList()

        self.player_sprite = Player('WhitePlayer.png', 1)
        self.player_sprite.center_x = SCREEN_WIDTH // 2
        self.player_sprite.center_y = 20
        self.player_list.append(self.player_sprite)

    def on_draw(self):
        arcade.start_render()

        self.player_sprite.draw()

    def on_update(self, delta_time: float):
        self.player_sprite.update()

    def on_key_press(self, symbol: int, modifiers: int):
        if symbol == arcade.key.UP:
            self.player_sprite.jump()
        elif symbol == arcade.key.LEFT:
            self.player_sprite.direction = 1
        elif symbol == arcade.key.RIGHT:
            self.player_sprite.direction = 2
        elif symbol == arcade.key.SPACE:
            self.player_sprite.speed_multiplier = 0.2
            self.player_sprite.swap_color()
            if self.background_color == arcade.csscolor.BLUE:
                self.background_color = arcade.csscolor.YELLOW
            else:
                self.background_color = arcade.color.BLUE

    def on_key_release(self, symbol: int, modifiers: int):
        if symbol == arcade.key.RIGHT or symbol == arcade.key.LEFT:
            self.player_sprite.direction = 0
        elif symbol == arcade.key.SPACE:
            self.player_sprite.speed_multiplier = 1


def main():
    window = Game(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE, 1/120)
    window.setup()
    arcade.run()


if __name__ == '__main__':
    main()
