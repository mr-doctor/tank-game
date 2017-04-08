import pygame, sys
import config
from pygame.locals import *

class Game():
	def __init__(self):
		self.background = (0, 0, 0)

		self.keybinds = {
			(KEYDOWN, K_h): self.hello_world,
			(KEYDOWN, K_ESCAPE): sys.exit,
			(QUIT, None): sys.exit
		}

	def update(self):
		for event in pygame.event.get():
			handler = self.keybinds.get((event.type, getattr(event, 'key', None)))
			if handler:
				handler()

	def hello_world(self):
		print('hello world')

	def draw(self, screen):
		pass


if __name__ == '__main__':
	pygame.init()
	screen = pygame.display.set_mode((int(config.width/2), int(config.height/2)))
	pygame.display.set_caption(config.title)
	g = Game()
	clock = pygame.time.Clock()
	while True:
		clock.tick(60)
		g.update()
		g.draw(screen)
		pygame.display.flip()