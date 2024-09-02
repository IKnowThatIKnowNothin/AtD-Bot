import re
import random
import Dueler
import Globals

class Duel:
        def run_round(self,dueler1,dueler2,roundCount):
                roundmessage = "##**Round {}** \n \n".format(roundCount)
                raw1 = dueler1.attack_roll()
                raw2 = dueler2.attack_roll()
                roll1 = raw1 + dueler1.bonus
                roll2 = raw2 + dueler2.bonus

                roundmessage += "**{}** Roll: {} ({}{:+})\n \n".format(dueler1.name,roll1,raw1,dueler1.bonus)
                roundmessage += "**{}** Roll: {} ({}{:+})\n \n".format(dueler2.name,roll2,raw2,dueler2.bonus)
                roundmessage += "\n\n *** \n\n"
                
                if roll1 > roll2:
                        winner = dueler1
                        loser = dueler2
                        win_raw = raw1
                elif roll2 > roll1:
                        winner = dueler2
                        loser = dueler1
                        win_raw = raw2
                else:
                        roundmessage += "Neither duelist can land a hit! \n\n"
                        return roundmessage

                dmgDealt = winner.damage_roll()
                roundmessage += "**Damage** Roll: {} ({}{:+})\n \n".format(dmgDealt,dmgDealt-winner.extradmg,winner.extradmg)
                if (win_raw >= winner.critThreshold):
                        loser.apply_injury()
                        roundmessage += "\n\n {} has a critical hit \n\n".format(winner.name)
                        if(winner.doubleCrit):
                                roundmessage += "\n \n As a T3 Bulwark they deal double damage! \n\n"
                                dmgDealt *= 2
                loser.morale -= dmgDealt
                roundmessage += "\n\n *** \n\n"   
                roundmessage += "\n\n {} hits {} \n\n".format(winner.name,loser.name)

                if raw1 == 1:
                        dueler1.apply_injury()
                        roundmessage += "\n\n {} has a critical miss \n\n".format(dueler1.name)
                if raw2 == 1:
                        dueler2.apply_injury()
                        roundmessage += "\n\n {} has a critical miss \n\n".format(dueler2.name)

                roundmessage += "\n\n The morale of the duellists currently stand as the following \n\n"
                roundmessage += "**{}** Morale: {} \n \n".format(dueler1.name,dueler1.morale)
                roundmessage += "**{}** Morale: {} \n \n".format(dueler2.name,dueler2.morale)
                roundmessage += "--- \n \n"  

                if (dueler2.morale <= 0) or (dueler2.morale <= dueler2.startpoint + dueler2.threshold):
                        #Dueler 1 has won
                        dueler2.continueFighting = False
                        roundmessage += "{} defeats {}, bringing an end to the battle.\n \n".format(dueler1.name,dueler2.name)
                        roundmessage += "**Winner: {}**\n \n".format(dueler1.name)
                        roundmessage += "**Winner's Remaining Morale: {}**\n \n".format(dueler1.morale)
                        roundmessage += "Rounds taken: {} \n \n".format(roundCount)

                elif (dueler1.morale <= 0) or (dueler1.morale <= dueler1.startpoint + dueler1.threshold):
                        #Dueler 2 has won
                        dueler1.continueFighting = False
                        roundmessage += "{} defeats {}, bringing an end to the battle.\n \n".format(dueler2.name,dueler1.name)
                        roundmessage += "**Winner: {}**\n \n".format(dueler2.name)
                        roundmessage += "**Winner's Remaining Morale: {}**\n \n".format(dueler2.morale)
                        roundmessage += "Rounds taken: {} \n \n".format(roundCount)
        
                return roundmessage

        def run(self,duelInfo):
                roundCount = 1
                                
                dueler1 = Dueler.Dueler(duelInfo.group(1), int(duelInfo.group(2)), int(duelInfo.group(3)))
                dueler2 = Dueler.Dueler(duelInfo.group(6), int(duelInfo.group(7)), int(duelInfo.group(8))) ##
                
                print(duelInfo.group(4))
                print(duelInfo.group(5))
                print(duelInfo.group(9)) ##
                print(duelInfo.group(10)) ##

                for i in range(4, 6):
                        if duelInfo.group(i) == "Masterwork":
                                dueler1.extradmg += 1
                        elif duelInfo.group(i) == "VS":
                                dueler1.extradmg += 3
                        elif duelInfo.group(i) == "Duelist1":
                                dueler1.bonus += 2
                        elif duelInfo.group(i) == "Duelist2":
                                dueler1.bonus += 4
                        elif duelInfo.group(i) == "Duelist3":
                                dueler1.bonus += 6
                                dueler1.critThreshold = 19
                        elif duelInfo.group(i) == "IronWill1":
                                dueler1.morale += 8
                                dueler1.ignoreInjury += 1
                        elif duelInfo.group(i) == "IronWill2":
                                dueler1.morale += 25
                                dueler1.ignoreInjury += 2
                        elif duelInfo.group(i) == "IronWill3":
                                dueler1.morale += 65
                                dueler1.ignoreInjury += 3
                                dueler1.bonus += 1
                        elif duelInfo.group(i) ==  "Bulwark1":
                                dueler2.bonus -= 1
                                dueler1.extradmg += 2
                        elif duelInfo.group(i) == "Bulwark2":
                                dueler2.bonus -= 2
                                dueler1.extradmg += 3
                        elif duelInfo.group(i) == "Bulwark3":
                                dueler2.bonus -= 3
                                dueler1.extradmg += 3
                                dueler1.doubleCrit = True
                        elif duelInfo.group(i) == "Blunted":
                                dueler1.extradmg -= 3
                        dueler1.startpoint = dueler1.morale


                for j in range(9, 11):
                        if duelInfo.group(j) == "Masterwork": ##
                                dueler2.extradmg += 1
                        elif duelInfo.group(j) == "VS": ##
                                dueler2.extradmg += 3
                        elif duelInfo.group(j) == "Duelist1": ##
                                dueler2.bonus += 2
                        elif duelInfo.group(j) == "Duelist2": ##
                                dueler2.bonus += 4
                        elif duelInfo.group(j) == "Duelist3": ##
                                dueler2.bonus += 6
                                dueler2.critThreshold = 19
                        elif duelInfo.group(j) == "IronWill1": ##
                                dueler2.morale += 8
                                dueler2.ignoreInjury += 1
                        elif duelInfo.group(j) == "IronWill2": ##
                                dueler2.morale += 25
                                dueler2.ignoreInjury += 2
                        elif duelInfo.group(j) == "IronWill3": ##
                                dueler2.morale += 35
                                dueler2.ignoreInjury += 3
                                dueler2.bonus += 1
                        elif duelInfo.group(j) ==  "Bulwark1": ##
                                dueler1.bonus -= 1
                                dueler2.extradmg += 1
                        elif duelInfo.group(j) == "Bulwark2": ##
                                dueler1.bonus -= 2
                                dueler2.extradmg += 3
                        elif duelInfo.group(j) == "Bulwark3": ##
                                dueler1.bonus -= 3
                                dueler2.extradmg += 3
                                dueler2.doubleCrit = True
                        elif duelInfo.group(j) == "Blunted": ##
                                dueler2.extradmg -= 3
                        dueler2.startpoint = dueler2.morale

                print(dueler1.doubleCrit)
                print(dueler2.doubleCrit)
                
                battlemessage = "#Duel Between {} and {} \n \n".format(dueler1.name,dueler2.name)                       
                battlemessage += "--- \n \n"

                battlemessage += self.run_round(dueler1,dueler2,roundCount)
                while(dueler1.continueFighting and dueler2.continueFighting):
                        roundCount += 1
                        battlemessage += self.run_round(dueler1,dueler2,roundCount)                               
                                                                                
      
                return battlemessage
                print ("Finished Duel")
                self.reset_battle_phase()
                
        def reset_battle_phase(self):
               print("Reset")
