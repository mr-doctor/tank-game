import random
import pygame
import math

from pygame.locals import *
from pygame import draw
from pygame.math import Vector2
from pygame import gfxdraw
from pygame import font

from config import width, height
from entity import Entity
from hitscanner import SniperShot, Beam
from projectile import Bullet, Flame, Rocket, MicroMissile, GuidedMissile
from projectile import Pellet

from config import Player

class Weapon:

	def control(self, entity, target, point, buttons):
		pass

	def draw(self, screen, x, y, active):
		width = 140
		draw.rect(screen, (80, 0, 0), (x, y, width, 20))
		if active:
			draw.rect(screen, (255, 0, 0), (x, y, width, 20))
		my_font = pygame.font.Font(None, 20)
		name = my_font.render(self.name, 1, (50, 255, 50))
		pygame.Surface.blit(screen, name, (x + 7, y + 5))


class BasicGun(Weapon):

	def __init__(self, cooldown=50):
		self.max_cooldown = cooldown
		self.cooldown = 0
		self.name = 'Basic Gun'

	def control(self, entity, target, point, buttons):
		self.cooldown -= 1

		button1, button2, button3 = buttons
		
		if button1 and self.cooldown <= 0:
			bullet = Bullet(entity.position + Vector2(entity.width / 2, entity.height / 2), (target - entity.position).normalize(), entity, damage=10, size=5)
			entity.spawn.append(bullet)
			self.cooldown = self.max_cooldown




class BurstGun(Weapon):

	def __init__(self, cooldown=100, burst_cooldown=2, burst_deviation=1):
		self.max_cooldown = cooldown
		self.cooldown = 0

		self.bullets_left = 0
		self.max_burst_cooldown = burst_cooldown
		self.burst_cooldown = 0
		self.spread = burst_deviation

		self.secondary_bullets_left = 0
		self.name = 'Burst Gun'

	def control(self, entity, target, point, buttons):
		self.cooldown -= 1
		self.burst_cooldown -= 1

		button1, button2, button3 = buttons

		if button1 and self.cooldown <= 0:
			self.secondary_bullets_left = Player.max_secondary_bullets
			self.cooldown = self.max_cooldown

		if self.secondary_bullets_left > 0 and self.burst_cooldown <= 0:
			direction = (target - entity.position).normalize()
			bullet = Bullet(entity.position + Vector2(entity.width / 2, entity.height / 2), direction.rotate(random.uniform(-self.spread, self.spread)), entity,
				damage=2.5, size=2, speed=13)
			entity.spawn.append(bullet)
			self.secondary_bullets_left -= 1
			self.burst_cooldown = self.max_burst_cooldown


class Shotgun(Weapon):

	def __init__(self, cooldown=80, spread=6, pellets=10):
		self.max_cooldown = cooldown
		self.cooldown = 0

		self.spread = spread
		self.pellets = pellets

		self.name = 'Shotgun'

	def control(self, entity, target, point, buttons):
		self.cooldown -= 1

		button1, button2, button3 = buttons

		if button1 and self.cooldown <= 0:
			for i in range(self.pellets):
				direction = (target - entity.position).normalize()
				pellet = Pellet(entity.position + Vector2(entity.width / 2, entity.height / 2), direction.rotate(random.uniform(-self.spread, self.spread)), entity,
					damage=2.65, speed=random.uniform(11, 13))
				entity.spawn.append(pellet)
			self.cooldown = self.max_cooldown


class MachineGun(Weapon):

	def __init__(self, cooldown=4, max_deviation=10):
		self.max_cooldown = cooldown
		self.cooldown = 0

		self.spread = 0
		self.max_deviation = max_deviation

		self.name = 'Machine Gun (%d%%)' % int((self.spread / self.max_deviation) * 100)

	def control(self, entity, target, point, buttons):
		self.cooldown -= 1
		self.spread = max(self.spread - 0.2, 0)

		button1, button2, button3 = buttons

		if button1 and self.cooldown <= 0:
			direction = (target - entity.position).normalize()
			bullet = Bullet(entity.position + Vector2(entity.width/2, entity.height/2), direction.rotate(random.uniform(-self.spread, self.spread)), entity,
				damage=1.5, size=1, speed=12)
			entity.spawn.append(bullet)
			self.spread = min(self.spread + 1.2, self.max_deviation)
			self.cooldown = self.max_cooldown


class SniperRifle(Weapon):

	def __init__(self, cooldown=200):
		self.max_cooldown = cooldown
		self.cooldown = 0
		self.name = 'Sniper Rifle (%d)' % self.cooldown

	def control(self, entity, target, point, buttons):
		self.cooldown = max(self.cooldown - 1, 0)

		button1, button2, button3 = buttons

		if button1 and self.cooldown <= 0:
			shot = SniperShot(entity.position + Vector2(entity.width/2, entity.height/2), (target - entity.position).normalize(), entity,
			    damage=40)
			entity.spawn.append(shot)
			self.cooldown = self.max_cooldown


class BeamGun(Weapon):

	def __init__(self, cooldown=1):
		self.max_cooldown = cooldown
		self.cooldown = 0
		self.name = 'Beam Gun'

	def control(self, entity, target, point, buttons):
		self.cooldown = max(self.cooldown - 1, 0)

		button1, button2, button3 = buttons

		if button1 and self.cooldown <= 0:
			beam = Beam(entity.position + Vector2(entity.width / 2, entity.height / 2), (target - entity.position).normalize(), entity,
					damage=1, colour=(20, 255, 100), width=5, range=200)
			entity.spawn.append(beam)
			self.cooldown += 2
			self.cooldown = self.max_cooldown


class Flamethrower(Weapon):

	def __init__(self, cooldown=3, max_deviation=4):
		self.max_cooldown = cooldown
		self.cooldown = 0

		self.spread = max_deviation

		self.name = 'Flamethrower'

	def control(self, entity, target, point, buttons):

		self.cooldown -= 1

		button1, button2, button3 = buttons

		if button1 and self.cooldown <= 0:
			target.rotate_ip(random.uniform(-self.spread, self.spread))
			fire = Flame(entity.position + Vector2(entity.width/2, entity.height/2), (target - entity.position).normalize(), entity,
				damage=0.6, size=3, speed=10)
			entity.spawn.append(fire)
			self.cooldown = self.max_cooldown


class RocketLauncher(Weapon):

	def __init__(self, cooldown=80):
		self.max_cooldown = cooldown
		self.cooldown = 0
		self.name = 'Rocket Launcher'

	def control(self, entity, target, point, buttons):

		self.cooldown -= 1

		button1, button2, button3 = buttons

		if button1 and self.cooldown <= 0:
			rocket = Rocket(entity.position + Vector2(entity.width/2, entity.height/2), (target - entity.position).normalize(), entity)
			entity.spawn.append(rocket)
			self.cooldown = self.max_cooldown


class MissileBarrage(Weapon):

	def __init__(self, cooldown=10):
		self.max_cooldown = cooldown
		self.cooldown = 0
		self.spread = 0
		self.max_deviation = 150

		self.name = 'Missile Barrage (%d%%)' % int((self.spread / self.max_deviation)*100)

	def control(self, entity, target, point, buttons):

		from controllers import TargeterController

		self.cooldown -= 1

		button1, button2, button3 = buttons

		if not button1 and self.cooldown <= 0:
			self.spread = max(self.spread - 0.4, 0)

		if button1 and self.cooldown <= 0:
			direction = (target - entity.position).normalize()
			deviation = 1
			if random.uniform(1, -1) < 0:
				deviation = -1
			start_direction = direction.rotate(50*deviation)
			rocket = MicroMissile(entity.position + Vector2(entity.width/2, entity.height/2), point, TargeterController(target=point, start_direction=start_direction, deviation=self.spread),
			                      direction, entity)
			entity.spawn.append(rocket)
			self.spread = min(self.spread + 2.5, self.max_deviation)
			self.cooldown = self.max_cooldown


class GuidedMissileLauncher(Weapon):

	def __init__(self, cooldown=150):
		self.max_cooldown = cooldown
		self.cooldown = 0
		self.name = 'Guided Missile'

	def control(self, entity, target, point, buttons):

		from controllers import EnemyHunterController

		self.cooldown -= 1
		button1, button2, button3 = buttons
		if button1 and self.cooldown <= 0:
			rocket = GuidedMissile(entity.position + Vector2(entity.width / 2, entity.height / 2), EnemyHunterController(target=point), (target - entity.position).normalize(), entity)
			entity.spawn.append(rocket)
			self.cooldown = self.max_cooldown
