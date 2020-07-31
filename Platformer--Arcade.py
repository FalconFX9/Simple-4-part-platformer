import arcade

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 800
SCREEN_TITLE = 'Platformer'

MAX_SPEED = 4
FRICTION = 0.05


class Player(arcade.Sprite):

    def __init__(self, image, image_scaling):
        super().__init__(image, image_scaling)

        self.direction = 0

    def gravity(self):
        self.change_y -= 0.18

        if self.top >= SCREEN_HEIGHT and self.change_y > 0:
            self.change_y = 0
            self.top = SCREEN_HEIGHT
        elif self.bottom <= 0 and self.change_y < 0:
            self.change_y = 0
            self.bottom = 0

    def jump(self):
        self.change_y = 7

    def update(self):
        self.gravity()

        if (self.right >= SCREEN_WIDTH and self.change_x > 0) or (self.left <= 0 and self.change_x < 0):
            self.change_x = 0

        if self.direction == 1:
            if self.change_x > -MAX_SPEED:
                self.change_x -= 0.1
        elif self.direction == 2:
            if self.change_x < MAX_SPEED:
                self.change_x += 0.1
        else:
            if self.change_x > FRICTION:
                self.change_x -= FRICTION
            elif self.change_x < -FRICTION:
                self.change_x += FRICTION
            else:
                self.change_x = 0

        print(self.center_y)

        self.center_x += self.change_x
        self.center_y += self.change_y


class Game(arcade.Window):

    def __init__(self, width, height, title, update_rate):
        super().__init__(width, height, title, update_rate=update_rate)

        self.player_list = None
        self.player_sprite = None

        arcade.set_background_color(arcade.color.BLACK)

    def setup(self):
        self.player_list = arcade.SpriteList()

        self.player_sprite = Player('Player.png', 1)
        self.player_sprite.center_x = SCREEN_WIDTH // 2
        self.player_sprite.center_y = 20
        self.player_list.append(self.player_sprite)

    def on_draw(self):
        arcade.start_render()

        self.player_list.draw()

    def on_update(self, delta_time: float):
        self.player_list.update()

    def on_key_press(self, symbol: int, modifiers: int):
        if symbol == arcade.key.UP:
            self.player_sprite.jump()
        elif symbol == arcade.key.LEFT:
            self.player_sprite.direction = 1
        elif symbol == arcade.key.RIGHT:
            self.player_sprite.direction = 2

    def on_key_release(self, symbol: int, modifiers: int):
        if symbol == arcade.key.RIGHT or symbol == arcade.key.LEFT:
            self.player_sprite.direction = 0


def main():
    window = Game(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE, 1/120)
    window.setup()
    arcade.run()


if __name__ == '__main__':
    main()
