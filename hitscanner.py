import pygame
from pygame.locals import *
from pygame import draw
from pygame.math import Vector2
from pygame import gfxdraw
import math

from entity import Entity
from tank import Tank

from config import width, height

class HitScanner(Entity):
	def __init__(self, position, direction, owner, damage, range=2000):
		super().__init__(position, collision_radius=1)
		self.direction = Vector2(direction)
		self.owner = owner
		self.damage = damage
		self.hitscan = True
		self.timer = 5
		self.range = range

	def update(self):

		if self.timer == 4:
			self.damage = 0
		if self.timer <= 0:
			self.remove = True
		self.timer -= 1

	def collide(self, other):
		E = Vector2(self.position)
		L = Vector2(self.position + (self.direction * self.range))
		C = Vector2(other.position.x + (other.width / 2), other.position.y + (other.height / 2))

		d = L - E
		f = E - C

		a = d.dot(d)
		b = 2 * f.dot(d)
		c = f.dot(f) - (other.width * other.width)

		discriminant = (b * b) - (4 * a * c)

		if discriminant >= 0:

			disc = math.sqrt(discriminant)

			t1 = (-b - disc) / (2 * a)
			t2 = (-b + disc) / (2 * a)

			if 0 <= t1 <= 1:
				self.hit(other)
			elif 0 <= t2 <= 1:
				self.hit(other)

	def hit(self, other):
		other.health = max(other.health - self.damage, 0)
		if other.health <= 0:
			for die_controller in other.controllers:
				die_controller.die(other, self)

	def draw(self, screen):
		pass

class SniperShot(HitScanner):
	def __init__(self, position, direction, owner, damage):
		super().__init__(position, direction, owner, damage=damage)
		self.width = self.collision_radius

	def draw(self, screen):
		P = Vector2(self.position)
		Q = Vector2(self.position + (self.direction * self.range))

		draw.lines(screen, (0, 255, 0), False, [(P.x, P.y), (Q.x, Q.y)])


class Beam(HitScanner):

	def __init__(self, position, direction, owner, damage, width, colour, range):
		super().__init__(position, direction, owner, damage=damage, range=range)
		self.width = width
		self.colour = colour

	def draw(self, screen):
		P = Vector2(self.position)
		Q = Vector2(self.position + (self.direction * self.range))

		draw.lines(screen, self.colour, False, [(P.x, P.y), (Q.x, Q.y)], self.width)