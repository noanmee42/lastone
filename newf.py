import arcade
import random

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

class GameObj:
    def __init__(self, Player, crystal, Enemy, cactus):
        self.Player = Player
        self.crystal = crystal
        self.Enemy = Enemy
        self.cactus = cactus

class Player(arcade.Sprite, GameObj):
    def __init__(self, Player):
        super().__init__(Player, ":resources:/images/animated_characters/female_person/femalePerson_idle.png")
        self.center_x = SCREEN_WIDTH / 2
        self.center_y = SCREEN_HEIGHT / 2
        self.speed = 4
    def reset(self):
        self.center_x = SCREEN_WIDTH / 2
        self.center_y = SCREEN_HEIGHT / 2

class Enemy(arcade.Sprite, GameObj):
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