import re
import random
class Jouster:
        name = ""
        bonus = 0
        injuryRoll = 0
        continueFighting = True
        ableToFight = True
        brokenLances = 0
        minorInjuries = 0
        moderateInjuries = 0
        majorInjuries = 0
        permanentInjuries = "None"
        alive = True
        def __init__(self,name,bonus):
                self.name = name
                self.bonus = bonus
        def attack_roll(self):
                random.seed()
                return random.randint(1,20)
        def modify_bonus(self,mod):
                self.bonus += mod
        def injury_roll(self):
                random.seed()
                injuryRoll = random.randint(1,20)
                if(injuryRoll >= 10):
                        self.minorInjuries += 1
                        self.continueFighting = False
                        self.ableToFight = False
                        return 0
                elif(injuryRoll >= 7):
                        self.moderateInjuries += 1
                        self.continueFighting = False
                        self.ableToFight = False
                        return 0
                else:
                        self.majorInjuries += 1
                        self.continueFighting = False
                        self.ableToFight = False
                        return 0
        def death_roll(self):
                injuryRoll = random.randint(1,20)
                if (injuryRoll <= 5 and injuryRoll >= 2):
                        self.minorInjuries += 1
                        self.continueFighting = False
                        self.ableToFight = False
                        return 0
                elif (injuryRoll == 1):
                        critRoll = random.randint(1, 20)
                        if(critRoll >= 6):
                                self.moderateInjuries += 1
                                self.continueFighting = False
                                self.ableToFight = False
                                return 0
                        elif (critRoll <= 5 and critRoll >= 2):
                                self.majorInjuries += 1
                                self.continueFighting = False
                                self.ableToFight = False
                                return 0
                        elif (critRoll == 1):
                                self.alive = False
                                self.continueFighting = False
                                self.ableToFight = False
                                return 0