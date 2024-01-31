import re
import random

class Dueler:

        commanderName = ""
        threshold = 0
        name = ""
        power = 0
        bonus = 0
        continueFighting = True
        morale = 30
	
        def __init__(self, duelerName,threshold,name,power,bonus):

                self.duelerName = duelerName  
                self.threshold = threshold
                self.name = name
                self.bonus = bonus

        def attack_roll(self):
		
                random.seed()
                return random.randint(1,20) +self.bonus

	def damage_roll(self):

		dmg = 0
                random.seed()
		for x in range(2):
			dmg += random.randint(1,5)
                return dmg
