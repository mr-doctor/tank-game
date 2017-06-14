	
class Enemies:
	health = 20


class Player:
	health = 80
	max_secondary_bullets = 8

width, height = 1920, 1080


class EasyDifficulty:
	index = 0
	num_enemies = 8
	num_motherships = 2
	num_light_enemies = 2
	num_shotgunner_enemies = 1
	num_beamer_enemies = 0
	num_healer_enemies = 0
	num_scanner_enemies = 0
	speed_mod = 1


class NormalDifficulty:
	index = 1
	num_enemies = 8
	num_motherships = 2
	num_light_enemies = 2
	num_shotgunner_enemies = 2
	num_beamer_enemies = 1
	num_healer_enemies = 0
	num_scanner_enemies = 1
	speed_mod = 1.3


class HardDifficulty:
	index = 2
	num_enemies = 8
	num_motherships = 3
	num_light_enemies = 5
	num_shotgunner_enemies = 3
	num_beamer_enemies = 2
	num_healer_enemies = 0
	num_scanner_enemies = 2
	speed_mod = 1.8

#num_enemies = 0
#num_motherships = 0
#num_light_enemies = 0
#num_shotgunner_enemies = 0
#num_beamer_enemies = 0
#num_healer_enemies = 0
#num_scanner_enemies = 0

mothership_spawn_cooldown = 180 // 100

title = 'T4NKS 4 NUFF1N M8'