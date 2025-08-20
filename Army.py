import re
import random
class Army:

        commanderName = ""
        threshold = 0
        name = ""
        power = 0
        bonus = 0
        miscBonus = 0
        roundsWon = 0
        continueFighting = True
        morale = 100
        startPoint = 100
        def __init__(self,commanderName,threshold,name,power,miscBonus):
                if (commanderName == "None"):
                        self.commanderName = "The {} Commander".format(name)
                else:
                        self.commanderName = commanderName
                        
                self.threshold = threshold
                self.name = name
                self.power = power
                self.armyBonus = miscBonus
                self.bonus = self.armyBonus
        def attack_roll(self):
                random.seed()
                return random.randint(1,100) +self.bonus
