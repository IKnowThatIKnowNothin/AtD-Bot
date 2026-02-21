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
    dead = False

    skill_count = 0

    def __init__(self, name, threshold, bonus, skill_count=0):
        self.name = name
        self.threshold = threshold
        self.bonus = bonus
        self.skill_count = skill_count

    def attack_roll(self):
        random.seed()
        return random.randint(1, 20)

    def damage_roll(self):
        dmg = 0
        random.seed()
        for _ in range(2):
            dmg += random.randint(1, 5)
        dmg += self.extradmg
        if dmg < 1:
            dmg = 0
        return dmg

    def apply_injury(self, roundmessage):
        random.seed()
        raw = random.randint(1, 20)
        total = raw + int(self.skill_count)

        roundmessage += "**Injury** Roll: {} (1d20={} + Skills={})\n \n".format(total, raw, self.skill_count)

        if total <= 2:
            roundmessage += "{} is killed!\n \n".format(self.name)
            self.continueFighting = False
            return roundmessage

        if total <= 4:
            roundmessage += "{} suffers a critical injury!\n \n".format(self.name)
            self.continueFighting = False
            return roundmessage

        if self.ignoreInjury > 0:
            self.ignoreInjury -= 1
            roundmessage += "{} shrugs off the injury malus (Wine of Courage).\n \n".format(self.name)
        else:
            self.bonus -= 2
            if total <= 8:
                roundmessage += "{} suffers a major injury (-2 to duel rolls for rest of duel).\n \n".format(self.name)
            else:
                roundmessage += "{} suffers a minor injury (-2 to duel rolls for rest of duel).\n \n".format(self.name)

        return roundmessage
