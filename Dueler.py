import re
import random
class Dueler:
        name = ""
        bonus = 0
        masterwork = False
        continueFighting = True
        ableToFight = True
        blockedInjuries = 0
        minorInjuries = 0
        moderateInjuries = 0
        majorInjuries = 0
        permanentInjuries = "None"
        alive = True
        def __init__(self,name,bonus,masterwork):
                self.name = name
                self.bonus = bonus
                self.masterwork = masterwork
        def attack_roll(self):
                return random.randint(1,100) + self.bonus
        def modify_bonus(self,mod):
                self.bonus += mod
        def injury_roll(self):
                injuryRoll = random.randint(1,20)
                if(injuryRoll > 15):
                        self.moderateInjuries += 1
                        return 5
                elif(injuryRoll > 5):
                        self.minorInjuries += 1
                        return 2
                else:
                        return 0
        def death_roll(self):
                deathRoll = random.randint(1,20)
                if(deathRoll > 10):
                        self.continueFighting = False
                        self.ableToFight = False
                        return 0
                elif(deathRoll > 5):
                        self.majorInjuries += 1
                        self.continueFighting = False
                        self.ableToFight = False
                        return 15
                else:
                        self.continueFighting = False
                        self.ableToFight = False
                        permanentRoll = random.randint(1,100)
                        if (permanentRoll <= 25):
                                self.alive = False
                        elif (permanentRoll <= 40):
                                self.permanentInjuries = "Hand"
                        elif (permanentRoll <= 55):
                                self.permanentInjuries = "Foot"
                        elif (permanentRoll <= 65):
                                self.permanentInjuries = "Blinded"
                        elif (permanentRoll <= 75):
                                self.permanentInjuries = "Defeaned"
                        elif (permanentRoll <= 40):
                                self.permanentInjuries = "Internal"
                        elif (permanentRoll <= 40):
                                self.permanentInjuries = "Scar"
                        else:
                                self.permanentInjuries = "Genital"
                        print(permanentRoll)
                        print(self.permanentInjuries)
                        return 0
		
        def broken_roll(self):
                brokenRoll = random.randint(1,20)
                if(brokenRoll > 18):
                        self.majorInjuries += 1
                        self.continueFighting = False
                        return 15
                else:
                        self.continueFighting = False
                        self.ableToFight = False
                        return 0
		
        def blunted_roll(self):
                self.continueFighting = False
                self.ableToFight = False
                return 0

