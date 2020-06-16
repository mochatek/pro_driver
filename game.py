import arcade
import random

SCREEN_WIDTH = 640
SCREEN_HEIGHT = 640
TITLE = "Pro Driver"
SCALE = 0.5

PLAYER_SPEED = 5

class Car(arcade.Sprite):
    def __init__(self, car, side):
        super().__init__('res\{}{}.png'.format(car,side), SCALE)
        self.textures = []
        texture = arcade.load_texture('res\{}{}.png'.format(car,side))
        self.textures.append(texture)
        texture = arcade.load_texture('res\{}B.png'.format(car))
        self.textures.append(texture)
        #self.scale = 0.5
        self.set_texture(0)
        self.side = side
        self.change_angle = 0
        if side == 'R':
            self.left = random.randint(320, 403)
            self.bottom = random.randint(700, 800)
            self.change_x = 0
            self.change_y = random.randint(-6, -2)
        elif side == 'L':
            self.right = random.randint(227, 320)
            self.bottom = random.choice([random.randint(-160, -60), random.randint(700, 800)])
            if self.bottom > 0:
                self.change_y = random.randint(-6, -2)
            else:
                self.change_y = random.randint(2, 6)

    def update(self):
        self.angle += self.change_angle
        self.center_y += self.change_y
        self.center_x += self.change_x
        if self.change_x != 0:
            self.texture = self.textures[1]
        if (self.bottom < 0 and self.change_y < 0) or (self.bottom > 640 and self.change_y > 0) or self.right < 192 or self.left > 448:
            self.remove_from_sprite_lists()


class Player(arcade.Sprite):
    def __init__(self, obj):
        super().__init__("res\car_blueL.png", SCALE)
        self.sprite_lists = obj.sprite_lists
        self._texture = obj._texture
        self.textures = obj.textures
        self._points = obj._points
        self.texture_transform = obj.texture_transform
        self.center_x = SCREEN_HEIGHT / 2
        self.center_y = SCREEN_HEIGHT / 2
        self.change_x = 0
        self.change_y = 0

    def update(self):
        self.center_x += self.change_x
        self.center_y += self.change_y
        if self.left < 192:
            self.left = 192
        elif self.right > 448:
            self.right = 448
        elif self.top > 384:
            self.top = 384
        elif self.bottom < 256:
            self.bottom = 256


class MyGame(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, TITLE)
        self.score = None
        self.frame = None
        self.frame_threshold = None
        self.player = None
        self.player_list = None
        self.road_list = None
        self.wall_list = None
        self.car_list = None
        self.game = None

    def setup(self):
        self.score = 0
        self.frame = 0
        self.frame_threshold = 40
        self.player_list = arcade.SpriteList()
        self.road_list = arcade.SpriteList()
        self.wall_list = arcade.SpriteList()
        self.car_list = arcade.SpriteList()
        map = arcade.tilemap.read_tmx("map.tmx")
        self.player = Player(arcade.tilemap.process_layer(map,'Car', SCALE)[0])
        self.player_list = arcade.SpriteList()
        self.player_list.append(self.player)
        self.road_list = arcade.tilemap.process_layer(map,'Road', SCALE)
        self.wall_list = arcade.tilemap.process_layer(map,'Border', SCALE)

    def on_draw(self):
        arcade.start_render()
        self.road_list.draw()
        self.wall_list.draw()
        self.car_list.draw()
        self.player_list.draw()
        arcade.draw_text("Distance : {} KM".format(self.score//100),32,600, arcade.color.WHITE,15, bold=True)
        if self.game == 'Over':
            texture =  arcade.load_texture('res\game_over.png')
            arcade.draw_lrwh_rectangle_textured(192,256,256,128,texture)



    def on_update(self,delta_time):
        if self.game == 'Running':
            self.score += 1
            self.car_list.update()
            self.player_list.update()
            self.frame += 1
            if len(self.car_list) < 4:
                if self.frame > self.frame_threshold:
                    car_clr = [random.choice(['car_yellow', 'car_blue', 'car_green']) for _ in range(2)]
                    side = random.sample(['L','R'], 2)
                    for i in range(2):
                        car = Car(car_clr[i], side[i])
                        self.car_list.append(car)
                    self.frame = 0
                    self.frame_threshold = random.randint(40, 70)

            for car in self.car_list:
                hit_list = arcade.check_for_collision_with_list(car, self.car_list)
                for car in hit_list:
                    car.change_x = random.randint(-5, 5)
                    car.change_angle = random.randrange(0,30)

            player_hit_list = arcade.check_for_collision_with_list(self.player, self.car_list)
            if len(player_hit_list) > 0:
                self.game = 'Over'
        else:
            pass

    def on_key_press(self, symbol, modifiers):
        if symbol == arcade.key.RIGHT:
            self.player.change_x = PLAYER_SPEED
        elif symbol == arcade.key.LEFT:
            self.player.change_x = -PLAYER_SPEED
        if symbol == arcade.key.UP:
            self.player.change_y = PLAYER_SPEED
        elif symbol == arcade.key.DOWN:
            self.player.change_y = -PLAYER_SPEED
        elif symbol == arcade.key.ENTER:
            self.game = 'Running'

    def on_key_release(self, symbol, modifiers):
        if symbol == arcade.key.RIGHT or symbol == arcade.key.LEFT:
            self.player.change_x = 0
        if symbol == arcade.key.UP or symbol == arcade.key.DOWN:
            self.player.change_y = 0

def main():
    window = MyGame()
    window.setup()
    arcade.run()

if __name__ == "__main__":
    main()