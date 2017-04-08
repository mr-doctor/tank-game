from pygame.math import Vector2
from pygame import gfxdraw

from config import width, height
from config import Player
from entity import Entity
from projectile import Projectile
from tank import Tank


class HealthPack(Entity):

	def __init__(self, position, health_power=5, collision_radius=9):
		super().__init__(position, collision_radius=collision_radius)
		self.collision_radius = collision_radius
		self.size = collision_radius
		self.width = self.size
		self.height = self.size
		self.health_power = health_power

	def draw(self, screen):
		gfxdraw.aacircle(screen, int(self.position.x), int(self.position.y), self.size, (200, 0, 100))
		gfxdraw.filled_circle(screen, int(self.position.x), int(self.position.y), self.size, (200, 0, 100))

	def should_collide(self, other):
		return isinstance(other, Tank) and other.is_player

	def handle_collision(self, other):
		if isinstance(other, Tank) and other.is_player:
			other.health = min(other.health + self.health_power, Player.health)
			self.remove = True