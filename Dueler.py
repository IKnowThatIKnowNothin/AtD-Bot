import re
import random

class Dueler:

	name = ""
	threshold = 0
	bonus = 0
	extradmg = 0
	dmg = 0
	continueFighting = True
	morale = 30
	startpoint = 30
	ignoreInjury = 0
	critThreshold = 20
	doubleCrit = False
	def __init__(self,name,threshold,bonus):
		self.name = name  
		self.threshold = threshold
		self.bonus = bonus
	def attack_roll(self):
		random.seed()
		return random.randint(1,20)
	def damage_roll(self):
		dmg = 0
		random.seed()
		for x in range(2):
			dmg +=  random.randint(1,5)
		dmg += self.extradmg
		if dmg < 1:
			dmg = 0
		return dmg
	def apply_injury(self):
		if self.ignoreInjury > 0:
			self.ignoreInjury -= 1
		else:
			self.bonus -= 2

