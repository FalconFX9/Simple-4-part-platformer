"""
TODO: BUGTEST LEVEL EDITOR
      Test on different platforms
      Add playtesting to the level editor? -- optional
"""
import arcade
from arcade.gui import UIFlatButton, UIInputBox, UIManager
from PIL import ImageColor
from time import time
from os import path


class Button:

    def __init__(self, centerx, centery, width, height):
        self.centerx = centerx
        self.centery = centery
        self.width = width
        self.height = height
        self.x = self.centerx - (self.width / 2)
        self.y = self.centery - (self.height / 2)

    def update(self):
        self.x = self.centerx - (self.width / 2)
        self.y = self.centery - (self.height / 2)


class LevelEditor(arcade.View):

    def __init__(self, window: arcade.Window):
        super().__init__()
        self.window = window
        self.img = None
        self.ui_manager = UIManager(window)
        self.rect_size = 150
        self.rect_color = (255, 0, 0)
        self.placing_pl = False
        self.mouse_x = 0
        self.mouse_y = 0
        self.pl_list = []
        self.lvl_num = 0
        self.timer = None
        self.save_msg = False
        self.platform_btn = None
        self.error_msg = None

    def setup(self):

        pl_size_box = UIInputBox(1200, 730, 200, 40, "150", 'pl_size')

        self.ui_manager.add_ui_element(pl_size_box)

        @pl_size_box.event('on_enter')
        def update_size():
            text_box = self.ui_manager.find_by_id('pl_size')
            try:
                self.rect_size = int(text_box.text)
                if 10 > self.rect_size:
                    self.error_msg = 'Must be over 10'
                    self.rect_size = 150
            except ValueError:
                self.error_msg = 'Must be an integer'
                self.rect_size = 150
                text_box.text = "150"
            self.platform_btn.width = self.rect_size
            self.platform_btn.update()

        pl_color_box = UIInputBox(1200, 620, 200, 40, "#FF0000", 'pl_color')

        self.ui_manager.add_ui_element(pl_color_box)

        @pl_color_box.event('on_enter')
        def update_color():
            text_box = self.ui_manager.find_by_id('pl_color')
            try:
                color = text_box.text
                color = color[1:]
                color = '0x' + color
                color = hex(int(color, 16))
                color = color[2:]
                self.rect_color = ImageColor.getcolor("#" + color, 'RGB')
            except ValueError:
                text_box.text = '#FF0000'
                self.error_msg = 'Must be hex'

        self.platform_btn = Button(1200, 500, self.rect_size, 10)

        lvl_number = UIInputBox(1200, 400, 200, 40, '0', 'lvl_num')

        @lvl_number.event('on_enter')
        def update_lvl():
            text_box = self.ui_manager.find_by_id('lvl_num')

            try:
                num = int(text_box.text)
                self.lvl_num = num
                self.error_msg = 'Level number changed!'
            except ValueError:
                text_box.text = '0'
                self.error_msg = 'Must be integer'
                self.lvl_num = 0

        self.ui_manager.add_ui_element(lvl_number)

        save_btn = UIFlatButton("Save level", 1200, 50, 150, 40, id='save')
        self.ui_manager.add_ui_element(save_btn)

        @save_btn.event('on_click')
        def save():
            file = open('level' + str(self.lvl_num) + '.dat', 'w')
            for platform in self.pl_list:
                file.writelines(
                    'platform ' + str(platform[0]) + ' ' + str(800 - platform[1]) + ' ' + str(platform[2]) + ' ' + str(
                        '#%02x%02x%02x' % tuple(platform[4])) + '\n')
            file.close()
            self.timer = time()
            self.save_msg = True

    def on_show_view(self):
        self.setup()

    def on_mouse_motion(self, x: float, y: float, dx: float, dy: float):
        self.mouse_x = x
        self.mouse_y = y

    def on_mouse_press(self, x: float, y: float, button: int, modifiers: int):
        if self.platform_btn.x < x < self.platform_btn.x + self.platform_btn.width and \
                self.platform_btn.y < y < self.platform_btn.y + self.platform_btn.height and \
                button == 1:
            self.placing_pl = True

        if 0 < x < 999 - (self.rect_size / 2) and 0 < y < 800 and button == 1 and self.placing_pl:
            self.placing_pl = False
            self.pl_list.append((x, y, self.rect_size, 10, self.rect_color))

        for coords in self.pl_list:
            offset_x = coords[2] / 2
            if coords[0] - offset_x < x < coords[0] + offset_x and coords[1] - 10 < y < coords[
                1] + 10 and not self.placing_pl and button == 4:
                self.pl_list.remove(coords)

    def on_draw(self):
        arcade.start_render()
        arcade.draw_line(1000, 0, 1000, 800, arcade.color.WHITE)
        arcade.draw_text("Platform size (pixels)", 1200, 760, arcade.color.WHITE, 30, anchor_x='center')
        arcade.draw_text("Platform color (hex)", 1200, 650, arcade.color.WHITE, 30, anchor_x='center')
        arcade.draw_text("Level number", 1200, 430, arcade.color.WHITE, 30, anchor_x='center')
        arcade.draw_text("Platform:", 1200, 520, arcade.color.WHITE, 30, anchor_x='center')
        arcade.draw_rectangle_filled(self.platform_btn.centerx,
                                     self.platform_btn.centery,
                                     self.rect_size, 10,
                                     self.rect_color)
        arcade.draw_rectangle_filled(500, 775, 1000, 50, arcade.color.GREEN)
        for platform in self.pl_list:
            arcade.draw_rectangle_filled(platform[0], platform[1], platform[2], platform[3], platform[4])
        if self.placing_pl:
            arcade.draw_rectangle_filled(self.mouse_x, self.mouse_y, self.rect_size, 10, self.rect_color)
        if self.save_msg:
            if self.timer + 2 > time():
                arcade.draw_text("Saved!", 500, 400, arcade.color.WHITE, 50, anchor_x='center')
            else:
                self.save_msg = False
                self.timer = None

        if self.error_msg:
            if self.timer:
                if self.timer + 2 > time():
                    arcade.draw_text(self.error_msg, 500, 400, arcade.color.WHITE, 50, anchor_x='center')
                else:
                    self.error_msg = None
                    self.timer = None
            else:
                self.timer = time()


screen = arcade.Window(1400, 800, "Level Editor", update_rate=1 / 120)
screen.show_view(LevelEditor(screen))
arcade.run()
