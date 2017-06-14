from pygame.locals import *
from pygame import draw
from pygame.math import Vector2
from pygame import gfxdraw
import spritesheet

class Entity:
	def __init__(self, pos, sprite_coords=((0, 0, 40, 40), (40, 0, 40, 40), (0, 255, 0)), collision_radius=0):
		self.position = Vector2(pos)
		self.collision_radius = collision_radius
		self.remove = False
		self.projectile = False
		self.hitscan = False
		self.to_add = []
		self.spawn = []
		self.controllers = []
		# self.ss = spritesheet.spritesheet(('Sprites.png', 'Basic Turret.png'))
		self.sprite_coords = sprite_coords
		self.sprite = self.get_sprite()
		self.rotated_sprite = self.sprite

	def draw(self, screen):
		pass

	def update(self):
		pass

	def should_collide(self, other):
		return False

	def collide(self, other):
		if not other.hitscan:
			return ((self.position + Vector2(self.width/2, self.height/2)) - (other.position + Vector2(other.width/2, other.height/2))).length() < \
				(self.collision_radius + other.collision_radius)
		else:
			other.collide(self)

	def handle_collision(self, other):
		pass

	def get_sprite(self):
		pass
		# return self.ss.image_at(self.ss.body_sheet, self.sprite_coords[0], self.sprite_coords[2])

	def view_world(self, world):
		pass

	def get_centre(self):
		return Vector2(self.position.x + self.collision_radius, self.position.y + self.collision_radius)

