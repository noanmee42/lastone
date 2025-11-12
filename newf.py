import arcade
import random

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

WALLS_POSITIONS = [
  # снизу
  (SCREEN_WIDTH / 2 - 125, 12.5),
  (SCREEN_WIDTH / 2 - 250, 12.5),
  (25, 12.5),
  (SCREEN_WIDTH / 2, 12.5),
  (SCREEN_WIDTH / 2 + 125, 12.5),
  (SCREEN_WIDTH / 2 + 250, 12.5),
  (SCREEN_WIDTH - 25, 12.5),
  # верх
  (SCREEN_WIDTH / 2 - 125, SCREEN_HEIGHT - 12.5),
  (SCREEN_WIDTH / 2 - 250, SCREEN_HEIGHT - 12.5),
  (25, SCREEN_HEIGHT - 12.5),
  (SCREEN_WIDTH / 2, SCREEN_HEIGHT - 12.5),
  (SCREEN_WIDTH / 2 + 125, SCREEN_HEIGHT - 12.5),
  (SCREEN_WIDTH / 2 + 250, SCREEN_HEIGHT - 12.5),
  (SCREEN_WIDTH - 25, SCREEN_HEIGHT - 12.5),
  # слева
  (12.5, SCREEN_HEIGHT / 2 - 125),
  (12.5, SCREEN_HEIGHT / 2 - 250),
  (12.5, SCREEN_HEIGHT / 2),
  (12.5, SCREEN_HEIGHT / 2 + 125),
  (12.5, SCREEN_HEIGHT / 2 + 250),
  # справа
  (SCREEN_WIDTH - 12.5, SCREEN_HEIGHT / 2 - 125),
  (SCREEN_WIDTH - 12.5, SCREEN_HEIGHT / 2 - 250),
  (SCREEN_WIDTH - 12.5, SCREEN_HEIGHT / 2),
  (SCREEN_WIDTH - 12.5, SCREEN_HEIGHT / 2 + 125),
  (SCREEN_WIDTH - 12.5, SCREEN_HEIGHT / 2 + 250),
]

class GameObj(arcade.Sprite):
    def __init__(self, texture, scale):
       super().__init__(texture, scale)

class Player(GameObj):
    def __init__(self):
        super().__init__(":resources:/images/animated_characters/female_person/femalePerson_idle.png", 0.5)
        self.center_x = SCREEN_WIDTH / 2
        self.center_y = SCREEN_HEIGHT / 2
        self.speed = 4
    def reset(self):
        self.center_x = SCREEN_WIDTH / 2
        self.center_y = SCREEN_HEIGHT / 2

class Enemy(GameObj):
  # 1 - вправо, -1 - влево
  def __init__(self, wall_list, x, y, direction = 1):
    super().__init__(":resources:/images/alien/alienBlue_front.png", 0.5)
    self.center_x = x
    self.center_y = y
    self.speed = 5
    self.direction = direction
    self.direction *= -1
    self.default_values = {
      "direction": direction,
      "x": x,
      "y": y,
    }
    self.wall_list = wall_list

    self.create_walls()

  def create_walls(self):
    for x, y in WALLS_POSITIONS:
      wall = arcade.Sprite(":resources:/images/tiles/boxCrate.png")
      wall.center_x = x
      wall.center_y = y
      self.wall_list.append(wall)
    
  def update(self, delta_time):
    self.center_x += self.speed * self.direction
    self.center_y -= self.speed / self.direction
    hits = arcade.check_for_collision_with_list(self, self.wall_list)
    for wall in hits:
        self.direction *= -1
        def exclude_zero(start,stop,exclude):
          while True:
            number = random.randint(start, stop)
            if number != exclude:
              return number
        self.direction = exclude_zero(-5,5,0)

  def reset(self):
    self.center_x = self.default_values["x"]
    self.center_y = self.default_values["y"]
    self.direction = self.default_values["direction"]

class crystal(GameObj):
   def __init__(self, x, y):
      super().__init__(":resources:images/items/gemBlue.png", 0.75)
      self.center_x = x
      self.center_y = y
      self.default_values = {
      "x": x,
      "y": y,
    }

class cactus(GameObj):
   def __init__(self,x,y):
      super.__init__(":resources:images/items/coinSilver.png", 0.75)
      self.center_x = x
      self.center_y = y
      self.default_values = {
        "x": x,
        "y": y,
        }

class MyGame(arcade.Window):
  def __init__(self):
    super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, "мини игра")
    arcade.set_background_color(arcade.color.AMAZON)

    self.player_list = arcade.SpriteList()
    self.wall_list = arcade.SpriteList()
    self.crystal_list = arcade.SpriteList()
    self.enemy_list = arcade.SpriteList()
    self.cactus_list = arcade.SpriteList()
    
    self.player = Player()
    self.enemy = Enemy(self.wall_list, 300, 150)
    self.player_list.append(self.player)
    self.enemy_list.append(self.enemy)
    self.cactus = cactus(200,150)
    self.crystal = crystal(300,150)
    self.cactus_list.append(self.cactus)
    self.crystal_list.append(self.crystal)

    def reset(self, create_diamonds = True):
        self.score = 0
        self.player.reset()
        self.enemy.reset()

    def on_draw(self):
        self.clear()
        
        # Рисуем все спрайты
        self.crystal_list.draw()
        self.cactus_list.draw()
        self.enemy_list.draw()
        self.player_list.draw()
        
        # Рисуем UI
        arcade.draw_text(f"Уровень: {self.level}", 10, SCREEN_HEIGHT - 30, arcade.color.WHITE, 20)
        arcade.draw_text(f"Кристаллы: {self.score}/{self.diamonds_to_collect}", 10, SCREEN_HEIGHT - 60, arcade.color.WHITE, 20)
        arcade.draw_text("R - Сброс игры", SCREEN_WIDTH - 150, SCREEN_HEIGHT - 30, arcade.color.WHITE, 16)
    def on_update(self, delta_time):
        self.enemy_list.update()
        # Проверяем игрока по оси x
        self.player.center_x += self.player.change_x
        hits = arcade.check_for_collision_with_list(self.player, self.wall_list)
        for wall in hits:
            if self.player.change_x > 0:
                self.player.right = wall.left
            elif self.player.change_x < 0:
                self.player.left = wall.right

        # Проверяем игрока по оси y
        self.player.center_y += self.player.change_y
        hits = arcade.check_for_collision_with_list(self.player, self.wall_list)
        for wall in hits:
            if self.player.change_y > 0:
                self.player.top = wall.bottom
            elif self.player.change_y < 0:
                self.player.bottom = wall.top

        # Проверяем игрока на поднятие монет
        hit_diamonds = arcade.check_for_collision_with_list(self.player, self.diamond_list)
        for diamond in hit_diamonds:
            diamond.remove_from_sprite_lists()
            self.score += 1
            arcade.play_sound(arcade.load_sound(":resources:sounds/coin1.wav"))

        # Проверяем игрока на столкновение с врагом
        enemy_hits = arcade.check_for_collision_with_list(self.player, self.enemy_list)
        for _ in enemy_hits:
            self.reset()

        # Проверяем игрока на столкновение с шипами
        spike_list = arcade.check_for_collision_with_list(self.player, self.spike_list)
        for _ in spike_list:
            self.reset()

        self.check_win()

  def on_key_press(self, key, modifiers):
    match key:
      case arcade.key.A:
        self.player.change_x = -self.player.speed
      case arcade.key.D:
        self.player.change_x = self.player.speed
      case arcade.key.W:
        self.player.change_y = self.player.speed
      case arcade.key.S:
        self.player.change_y = -self.player.speed

  def on_key_release(self, key, modifiers):
    match key:
      case arcade.key.A | arcade.key.D:
        self.player.change_x = 0
      case arcade.key.W | arcade.key.S:
        self.player.change_y = 0

window = MyGame()
arcade.run()
