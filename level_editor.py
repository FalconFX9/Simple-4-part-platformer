"""
TODO: BUGTEST LEVEL EDITOR
      Test on different platforms
      Add playtesting to the level editor? -- optional
"""
import arcade
from arcade.gui import UIFlatButton, UIInputBox, UIManager
from PIL import ImageColor
from time import time


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

    def setup(self):
        load_img_btn = UIFlatButton('Load custom platform image', 1200, 100, 375, 50, id='loadimgbtn')
        load_img_btn.set_style_attrs(
            border_color_hover=arcade.color.WHITE,
            border_color_press=arcade.color.WHITE
        )

        @load_img_btn.event('on_click')
        def load_img():
            from tkinter.filedialog import askopenfilename
            import tkinter
            tkinter.Tk().withdraw()
            filename = askopenfilename()
            if filename.endswith('.jpg') or filename.endswith('.jpeg') or filename.endswith('.png'):
                self.img = arcade.load_texture(filename)

        self.ui_manager.add_ui_element(load_img_btn)

        pl_size_box = UIInputBox(1200, 730, 200, 40, "150", 'pl_size')

        self.ui_manager.add_ui_element(pl_size_box)

        @pl_size_box.event('on_enter')
        def update_size():
            text_box = self.ui_manager.find_by_id('pl_size')
            try:
                self.rect_size = int(text_box.text)
                if 10 > self.rect_size:
                    text_box.text = 'Must be over 10'
                    self.rect_size = 150
            except ValueError:
                text_box.text = 'Must be an integer'
                self.rect_size = 150
            self.ui_manager.find_by_id('platform').width = self.rect_size

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
            except ValueError:
                text_box.text = 'Must be an integer'
                color = '0xFF0000'
            color = color[2:]
            self.rect_color = ImageColor.getcolor("#" + color, 'RGB')
            self.ui_manager.find_by_id('platform').set_style_attrs(
                border_color=self.rect_color,
                border_color_hover=self.rect_color,
                border_color_press=self.rect_color,
                bg_color=self.rect_color,
                bg_color_hover=self.rect_color,
                bg_color_press=self.rect_color,
            )

        platform_btn = UIFlatButton("", 1200, 500, width=self.rect_size, height=10, id='platform')
        platform_btn.set_style_attrs(
            border_color=self.rect_color,
            border_color_hover=self.rect_color,
            border_color_press=self.rect_color,
            bg_color=self.rect_color,
            bg_color_hover=self.rect_color,
            bg_color_press=self.rect_color
        )
        self.ui_manager.add_ui_element(platform_btn)

        @platform_btn.event('on_click')
        def select_pl():
            self.placing_pl = True

        save_btn = UIFlatButton("Save level", 1200, 50, 150, 40, id='save')
        self.ui_manager.add_ui_element(save_btn)

        @save_btn.event('on_click')
        def save():
            file = open('level'+str(self.lvl_num)+'.dat', 'w')
            for platform in self.pl_list:
                file.writelines('platform ' + str(platform[0]) + ' ' + str(800 - platform[1]) + ' ' + str(platform[2]) + ' ' + str('#%02x%02x%02x' % tuple(platform[4])) + '\n')
            file.close()
            self.timer = time()
            self.save_msg = True

    def on_show_view(self):
        self.setup()

    def on_mouse_motion(self, x: float, y: float, dx: float, dy: float):
        self.mouse_x = x
        self.mouse_y = y

    def on_mouse_press(self, x: float, y: float, button: int, modifiers: int):
        if 0 < x < 999 - (self.rect_size/2) and 0 < y < 800 and button==1 and self.placing_pl:
            self.placing_pl = False
            self.pl_list.append((x, y, self.rect_size, 10, self.rect_color))

        for coords in self.pl_list:
            offset_x = coords[2]/2
            if coords[0] - offset_x < x < coords[0] + offset_x and coords[1] - 10 < y < coords[1] + 10 and not self.placing_pl and button==4:
                self.pl_list.remove(coords)

    def on_draw(self):
        arcade.start_render()
        arcade.draw_line(1000, 0, 1000, 800, arcade.color.WHITE)
        arcade.draw_text("Platform size (pixels)", 1200, 760, arcade.color.WHITE, 30, anchor_x='center')
        arcade.draw_text("Platform color (hex)", 1200, 650, arcade.color.WHITE, 30, anchor_x='center')
        arcade.draw_text("Platform:", 1200, 520, arcade.color.WHITE, 30, anchor_x='center')
        self.ui_manager.find_by_id('platform').width = self.rect_size
        for platform in self.pl_list:
            arcade.draw_rectangle_filled(platform[0], platform[1], platform[2], platform[3], platform[4])
        if self.placing_pl:
            arcade.draw_rectangle_filled(self.mouse_x, self.mouse_y, self.rect_size, 10, self.rect_color)
        if self.save_msg:
            if self.timer + 2 > time():
                arcade.draw_text("Saved!", 500, 400, arcade.color.WHITE, 50, anchor_x='center')
            else:
                self.save_msg = False


screen = arcade.Window(1400, 800, "Level Editor", update_rate=1 / 120)
screen.show_view(LevelEditor(screen))
arcade.run()
