#import the pygame module, and the
#sys module for exiting the window we create
import pygame, sys
import random, pdb

#import some useful constants
from pygame.locals import *
from pygame import draw
from pygame import gfxdraw
from pygame.math import Vector2
from pygame import mouse
from pygame import font

import weapons
import projectile
from tank import Tank
from projectile import Projectile
from tank import Tank
import factories

from config import width, height, num_enemies, num_motherships, num_light_enemies, num_shotgunner_enemies, num_beamer_enemies
import config


class World:
	
	def __init__(self):
		self.player = None
		enemies = [factories.create_basic_enemy(Vector2(random.randint(0, width - 100), random.randint(0, height - 100))) for i in range(num_enemies)]
		motherships = [factories.create_mothership(Vector2(random.randint(0, width - 100), random.randint(0, height - 100))) for i in range(num_motherships)]
		light_enemies = [factories.create_light_enemy(Vector2(random.randint(0, width - 100), random.randint(0, height - 100))) for i in range(num_light_enemies)]
		shotgunner_enemies = [factories.create_shotgunner_enemy(Vector2(random.randint(0, width - 100), random.randint(0, height - 100))) for i in  range(num_shotgunner_enemies)]
		beamer_enemies = [factories.create_beamer_enemy(Vector2(random.randint(0, width - 100), random.randint(0, height - 100))) for i in range(num_beamer_enemies)]
		scanner_enemies = [factories.create_scanner_enemy(Vector2(random.randint(0, width - 100), random.randint(0, height - 100))) for i in range(config.num_scanner_enemies)]
		self.entities = (enemies + motherships + light_enemies + shotgunner_enemies + beamer_enemies + scanner_enemies)

		self.all_weapons = [
			weapons.BasicGun(),
			weapons.BurstGun(),
			weapons.Shotgun(),
			weapons.MachineGun(),
			weapons.SniperRifle(),
			weapons.BeamGun(),
			weapons.Flamethrower(),
			weapons.RocketLauncher(),
			weapons.MissileBarrage(),
			weapons.GuidedMissileLauncher()
		]

	def spawn_enemies(self):
		enemies = [factories.create_basic_enemy(Vector2(random.randint(100, width - 100), random.randint(100, height - 100))) for i in range(num_enemies)]
		motherships = [factories.create_mothership(Vector2(random.randint(100, width - 100), random.randint(100, height - 100))) for i in range(num_motherships)]
		light_enemies = [factories.create_light_enemy(Vector2(random.randint(100, width - 100), random.randint(100, height - 100))) for i in range(num_light_enemies)]
		shotgunner_enemies = [factories.create_shotgunner_enemy(Vector2(random.randint(100, width - 100), random.randint(100, height - 100))) for i in range(num_shotgunner_enemies)]
		beamer_enemies = [factories.create_beamer_enemy(Vector2(random.randint(100, width - 100), random.randint(100, height - 100))) for i in range(num_beamer_enemies)]
		scanner_enemies = [factories.create_scanner_enemy(Vector2(random.randint(100, width - 100), random.randint(100, height - 100))) for i in range(config.num_scanner_enemies)]
		self.entities += (enemies + motherships + light_enemies + shotgunner_enemies + beamer_enemies + scanner_enemies)


class Game():
	def __init__(self):
		self.background = (0, 0, 0)
		self.world = World()
		self.paused = True
		self.weapon_select = True
		self.chosen_weapons = []
		for i in range(10):
			self.chosen_weapons.append(False)

		self.keybinds = {
			(KEYDOWN, K_ESCAPE): sys.exit,
			(QUIT, None): sys.exit,
			(KEYDOWN, K_q): pdb.set_trace,
			(KEYDOWN, K_p): self.world.spawn_enemies,
			(KEYDOWN, K_o): self.spawn_player,
			(KEYDOWN, K_F11): self.fullscreen,
			(KEYDOWN, K_SPACE): self.toggle_pause,
			(KEYDOWN, K_RETURN): self.start,
		}

		for i, key in enumerate([K_1, K_2, K_3, K_4, K_5, K_6, K_7, K_8, K_9, K_0]):
			self.keybinds[(KEYDOWN, key)] = self.choose_weapon(i)

	def update(self):

		# iterate all events
		for event in pygame.event.get():
			handler = self.keybinds.get((event.type, getattr(event, 'key', None)))
			if handler:
				handler()

		if not self.paused:

			for entity in self.world.entities:
				entity.view_world(self.world)

			for entity in self.world.entities:
				entity.update()

			self.do_collisions()

			for entity in self.world.entities:
				self.world.entities += entity.spawn
				entity.spawn = []
			# cull entities tagged to be removed
			i = 0
			while i < len(self.world.entities):
				if self.world.entities[i].remove:
					self.world.entities.pop(i)
					i -= 1
				i += 1

	def draw(self, screen):
		screen.fill(self.background)
		if not self.weapon_select:
			for entity in self.world.entities:
				entity.draw(screen)
				if entity is self.world.player:
					draw.rect(screen, (80, 0, 0), (700, 0, 80, 20))
					my_font = pygame.font.Font(None, 20)
					name = my_font.render('Kills: %d' % entity.kills, 1, (50, 255, 50))
					pygame.Surface.blit(screen, name, (700 + 3, 0 + 5))

			for i, weapon in enumerate(self.world.player.weapons):
				weapon.draw(screen, (i + 1)*130, 0, i == self.world.player.current_weapon)
		else:
			self.draw_weapon_select(screen)

	def spawn_player(self):
		if self.world.player.remove:
			self.world.player = factories.create_player(Vector2(1, 1), self.chosen_weapons)
			self.world.entities.append(self.world.player)

	def do_collisions(self):
		for entity in self.world.entities:
			for other in self.world.entities:
				if entity is not other and entity.should_collide(other) and entity.collide(other):
					entity.handle_collision(other)

	def draw_weapon_select(self, screen):
		for i in range(10):
			self.world.all_weapons[i].draw(screen, 100, (i + 1) * 50 + 20, self.chosen_weapons[i])

	def fullscreen(self):
		pygame.display.set_mode((width, height), pygame.FULLSCREEN)

	def toggle_pause(self):
		self.paused = not self.paused

	def choose_weapon(self, num):
		def choose():
			if self.weapon_select:
				self.chosen_weapons[num] = not self.chosen_weapons[num]

		return choose

	def start(self):
		num_weapons = 0
		for i in range(10):
			if self.chosen_weapons[i]:
				num_weapons += 1
		if num_weapons > 0:
			self.weapon_select = False
			self.world.player = factories.create_player(Vector2(1, 1), self.chosen_weapons)
			self.world.entities.append(self.world.player)


if __name__ == '__main__':
	pygame.init()
	screen = pygame.display.set_mode((width, height))
	pygame.display.set_caption(config.title)
	g = Game()
	clock = pygame.time.Clock()
	while True:
		clock.tick(60)
		g.update()		
		g.draw(screen)        
		pygame.display.flip()