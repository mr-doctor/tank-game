import random

from pygame.locals import *
from pygame import draw
from pygame.math import Vector2
from pygame import transform
from pygame import image
from pygame import gfxdraw
from pygame import transform

from config import width, height
from entity import Entity
from projectile import Projectile, Flame

import config

class Tank(Entity):
	def __init__(self, position, controllers, size=20, max_health=20, high_colour=(255, 0, 0), low_colour=(100, 0, 100), collision_radius=10, weapons=[], is_player =False,
	             sprite_coords=((0, 0, 40, 40), (40, 0, 40, 40),(0, 255, 0))):
		super().__init__(position, sprite_coords=sprite_coords, collision_radius=collision_radius)
		self.direction = Vector2(random.uniform(-1, 1), random.uniform(-1, 1)).normalize()
		self.health = max_health
		self.is_player = is_player
		self.on_fire = False
		self.fire_resist = 85
		self.fire_time = self.fire_resist

		self.width = size
		self.height = size
		self.max_health = max_health
		self.kills = 0
		self.high_colour = high_colour
		self.low_colour = low_colour
		self.controllers = controllers
		self.weapons = weapons
		self.current_weapon = 0
		self.angle = 0
		self.aim_angle = 90
		self.turret_sprite = self.get_turret_sprite()
		self.rotated_turret_sprite = self.turret_sprite

	def view_world(self, world):
		for controller in self.controllers:
			controller.view_world(self, world)

	def update(self):
		for controller in self.controllers:
			controller.control(self)
		if self.on_fire:
			self.handle_fire()

	def draw(self, screen):
		# self.sprite = transform.scale(self.sprite, (self.width, self.height))
		# self.turret_sprite = transform.scale(self.turret_sprite, (135, 27))
		# old_rect = self.sprite.get_rect(center = (self.position.x + self.width/2, self.position.y + self.height/2))
		# rotate_rect = self.turret_sprite.get_rect(center = ((self.position.x + 25), (self.position.y + 29)))
		#
		# self.rotated_turret_sprite, old_turret_rect = self.rotate_center(self.turret_sprite, rotate_rect, self.aim_angle)
		# self.rotated_sprite, new_rect = self.rotate_center(self.sprite, old_rect, self.angle)
		# screen.blit(self.rotated_sprite, new_rect)
		# screen.blit(self.rotated_turret_sprite, old_turret_rect)
		draw.rect(screen, self.high_colour, (self.position.x, self.position.y, self.width, self.height))

		self.draw_health_bar(screen)

	def rotate_by_angle(self, image, angle, rotations={}):
		r = rotations.get(image, 0) + angle
		rotations[image] = r
		return transform.rotate(image, r)

	def rotate_center(self, image, rect, angle):
		rot_image = transform.rotate(image, angle)
		rot_rect = rot_image.get_rect(center=rect.center)
		return rot_image,rot_rect

	def draw_health_bar(self, screen):
		health_percent = self.health / self.max_health
		low_colour = self.low_colour
		high_colour = self.high_colour
		colour = list(low_colour)
		for i in range(3):
			colour[i] += health_percent * (high_colour[i] - colour[i])
			if colour[i] < 0:
				colour[i] = 0
			if colour[i] > 255:
				colour[i] = 255
		draw.rect(screen, colour, (self.position.x + self.width / 2 - 26, self.position.y - 13, health_percent * 50, 5))

	def get_turret_sprite(self):
		pass
		# return self.ss.image_at(self.ss.turret_sheet, (0, 0, 90, 18), (0, 255, 0))

	def should_collide(self, other):
		if (other.projectile or other.hitscan) and other.owner is not self:
			if not other.owner.is_player and not self.is_player:
				return False
			return True
		return False

	def handle_collision(self, other):
		if other.projectile or other.hitscan:
			if other.projectile and not other.penetrate and not other.explosive:
				other.remove = True
			flame_mod = 1
			if other.projectile and other.flame:
				self.on_fire = True
				self.fire_time = 150
			if other.explosive and not other.exploding:
				other.explode()

			self.health = max(self.health - (other.damage + other.blast_damage), 0)
			if self.health <= 0:
				for die_controller in self.controllers:
					die_controller.die(self, other)
				other.owner.kills += 1

	def handle_fire(self):
		self.fire_time = max(self.fire_time - 1, 0)

		if self.fire_time <= 0:
			self.on_fire = False
			self.fire_time = self.fire_resist
		else:
			self.health = max(self.health - 0.1, 0)
			if self.fire_time % 5 == 0:
				flame = Flame(Vector2(random.uniform(self.position.x, self.position.x + self.width), random.uniform(self.position.y, self.position.y + self.height)),
					self.direction.reflect(self.direction), self, damage=0, size=1, speed=3, is_flame=False)
				self.spawn.append(flame)
				if self.health <= 0:
					for die_controller in self.controllers:
						die_controller.die(self, flame)
					flame.owner.kills += 1
