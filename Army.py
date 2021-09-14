import re
import random
class Army:

        commanderName = ""
        commanderBonus = 0
        name = ""
        power = 0
        bonus = 0
        continueFighting = True
        morale = 100
        def __init__(self,commanderName,commanderBonus,name,power,bonus):
                if (commanderName == "None"):
                        self.commanderName = "The {} Commander".format(name)
                else:
                        self.commanderName = commanderName
                        
                self.commanderBonus = commanderBonus
                self.name = name
                self.power = power
                self.armyBonus = bonus
                self.bonus = self.armyBonus
        def attack_roll(self):
                return random.randint(1,100) +self.bonus
