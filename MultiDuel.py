import re
import random
import Dueler
import Globals


class MultiDuel:
    LIVE_STEEL = True

    def run(self, comment_body):
        dueler_pattern = re.compile(
            r"^(.*?) ([\-]?\d+) ([\+\-]?\d*) ([\+\-]?\d*) ([\+\-]?\d*)(?: ([\+]?\d+))?$"
        )

        side1_lines = []
        side2_lines = []
        on_side2 = False

        for line in comment_body.strip().split('\n'):
            line = line.strip()
            if re.search(r"^vs$", line, re.IGNORECASE):
                on_side2 = True
                continue
            if on_side2:
                side2_lines.append(line)
            else:
                side1_lines.append(line)

        def parse_dueler(line):
            m = dueler_pattern.match(line)
            if not m:
                return None
            name        = m.group(1)
            threshold   = int(m.group(2))
            bonus       = int(m.group(3)) if m.group(3) else 0
            morale_mod  = int(m.group(4)) if m.group(4) else 0
            extra_dmg   = int(m.group(5)) if m.group(5) else 0
            skill_count = int(m.group(6)) if m.group(6) else 0

            d = Dueler.Dueler(name, threshold, bonus, skill_count)
            d.morale           = 30 + morale_mod
            d.extradmg         = extra_dmg
            d.startpoint       = d.morale
            d.continueFighting = True
            return d

        side1 = []
        for l in side1_lines:
            d = parse_dueler(l)
            if d:
                side1.append(d)

        side2 = []
        for l in side2_lines:
            d = parse_dueler(l)
            if d:
                side2.append(d)

        if not side1 or not side2:
            return "Improperly formatted Multi-Person Duel info."

        s1_names = ", ".join(d.name for d in side1)
        s2_names = ", ".join(d.name for d in side2)

        battlemessage = "#Multi-Person Duel: {} vs {} \n \n".format(s1_names, s2_names)
        battlemessage += "--- \n \n"

        roundCount = 1
        battlemessage += self.run_round(side1, side2, roundCount)

        while (any(d.continueFighting for d in side1) and any(d.continueFighting for d in side2)):
            side1 = [d for d in side1 if d.continueFighting]
            side2 = [d for d in side2 if d.continueFighting]
            if not side1 or not side2:
                break
            roundCount += 1
            battlemessage += self.run_round(side1, side2, roundCount)

        surviving1 = [d for d in side1 if d.continueFighting]
        surviving2 = [d for d in side2 if d.continueFighting]

        if surviving1 and not surviving2:
            winners = ", ".join(d.name for d in surviving1)
            battlemessage += "\n\n**Side 1 wins!** Survivors: {}\n \n".format(winners)
        elif surviving2 and not surviving1:
            winners = ", ".join(d.name for d in surviving2)
            battlemessage += "\n\n**Side 2 wins!** Survivors: {}\n \n".format(winners)
        else:
            battlemessage += "\n\nThe duel ends with no clear winner.\n \n"

        return battlemessage

    def run_round(self, side1, side2, roundCount):
        roundmessage = "##**Round {}** \n \n".format(roundCount)

        rolls = {}
        for d in side1 + side2:
            raw = d.attack_roll()
            rolls[d] = (raw, raw + d.bonus)

        roundmessage += "**Side 1**\n \n"
        for d in side1:
            raw, total = rolls[d]
            roundmessage += "**{}** Roll: {} ({}{:+})\n \n".format(d.name, total, raw, d.bonus)

        roundmessage += "**Side 2**\n \n"
        for d in side2:
            raw, total = rolls[d]
            roundmessage += "**{}** Roll: {} ({}{:+})\n \n".format(d.name, total, raw, d.bonus)

        roundmessage += "\n\n *** \n\n"

        # each attacker targets the highest rolling opponent they can beat that hasnt been hit yet
        # if everyone hittable has already been hit, pile onto the highest hittable one
        def assign_targets(attackers, defenders):
            already_hit = set()
            targets = {}
            for attacker in sorted(attackers, key=lambda d: rolls[d][1], reverse=True):
                att_total = rolls[attacker][1]
                hittable = [d for d in defenders if rolls[d][1] < att_total]
                hittable.sort(key=lambda d: rolls[d][1], reverse=True)

                not_yet_hit = [d for d in hittable if d not in already_hit]
                if not_yet_hit:
                    target = not_yet_hit[0]
                elif hittable:
                    target = hittable[0]
                else:
                    target = None

                targets[attacker] = target
                if target:
                    already_hit.add(target)
            return targets

        s1_targets = assign_targets(side1, side2)
        s2_targets = assign_targets(side2, side1)

        def apply_hit(attacker, target, roundmessage):
            att_raw = rolls[attacker][0]
            tgt_raw = rolls[target][0]

            if att_raw == 20 and tgt_raw == 1:
                target.continueFighting = False
                roundmessage += "{} deals a **Finishing Blow** to {}, instantly defeating them!\n \n".format(attacker.name, target.name)
                return roundmessage

            dmgDealt = attacker.damage_roll()
            roundmessage += "**Damage** Roll: {} ({}{:+})\n \n".format(dmgDealt, dmgDealt - attacker.extradmg, attacker.extradmg)

            if att_raw == 20:
                roundmessage += "\n\n {} has a critical hit on {} \n\n".format(attacker.name, target.name)
                if self.LIVE_STEEL:
                    roundmessage = target.apply_injury(roundmessage)
                if attacker.doubleCrit:
                    roundmessage += "\n \n As a T3 Bulwark they deal double damage! \n\n"
                    dmgDealt *= 2

            target.morale -= dmgDealt
            roundmessage += "\n\n {} hits {} \n\n".format(attacker.name, target.name)
            return roundmessage

        for attacker, target in s1_targets.items():
            if target is not None:
                roundmessage = apply_hit(attacker, target, roundmessage)
            else:
                roundmessage += "{} cannot land a hit on anyone this round.\n \n".format(attacker.name)

        roundmessage += "\n\n *** \n\n"

        for attacker, target in s2_targets.items():
            if target is not None:
                roundmessage = apply_hit(attacker, target, roundmessage)
            else:
                roundmessage += "{} cannot land a hit on anyone this round.\n \n".format(attacker.name)

        roundmessage += "\n\n *** \n\n"

        roundmessage += "\n\n The morale of the duellists currently stand as the following \n\n"
        roundmessage += "**Side 1** \n\n"
        for d in side1:
            roundmessage += "**{}** Morale: {} \n \n".format(d.name, d.morale)
        roundmessage += "**Side 2** \n\n"
        for d in side2:
            roundmessage += "**{}** Morale: {} \n \n".format(d.name, d.morale)
        roundmessage += "--- \n \n"

        for d in side1 + side2:
            if (d.morale <= 0) or (d.morale <= (d.startpoint + d.threshold)) or (d.continueFighting == False):
                if (d.morale <= 0):
                    print("A1")
                if (d.morale <= (d.startpoint + d.threshold)):
                    print("A2")
                    print(d.startpoint, " ", d.threshold)
                if (d.continueFighting == False):
                    print("A3")
                d.continueFighting = False
                roundmessage += "**{}** has been defeated!\n \n".format(d.name)

        return roundmessage

    def reset_battle_phase(self):
        print("Reset")
