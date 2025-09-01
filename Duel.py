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
                
                if(raw1 == 20 and raw2 == 1):
                        # Dueler 1 has won
                        dueler2.continueFighting = False
                        roundmessage += "{} defeats {}, bringing an end to the duel.\n \n".format(dueler1.name,dueler2.name)
                        roundmessage += "**Winner: {}**\n \n".format(dueler1.name)
                        roundmessage += "**Winner's Remaining Morale: {}**\n \n".format(dueler1.morale)
                        roundmessage += "Rounds taken: {} \n \n".format(roundCount)
                        return roundmessage
                if(raw2 == 20 and raw1 == 1):
                        # Dueler 2 has won
                        dueler1.continueFighting = False
                        roundmessage += "{} defeats {}, bringing an end to the duel.\n \n".format(dueler2.name,dueler1.name)
                        roundmessage += "**Winner: {}**\n \n".format(dueler2.name)
                        roundmessage += "**Winner's Remaining Morale: {}**\n \n".format(dueler2.morale)
                        roundmessage += "Rounds taken: {} \n \n".format(roundCount)
                        return roundmessage

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
                        roundmessage += "\n\n {} has a critical hit \n\n".format(winner.name)
                        loser.apply_injury()
                        if(winner.doubleCrit):
                                roundmessage += "\n \n As a T3 Bulwark they deal double damage! \n\n"
                                dmgDealt *= 2
                loser.morale -= dmgDealt
                roundmessage += "\n\n *** \n\n"   
                roundmessage += "\n\n {} hits {} \n\n".format(winner.name,loser.name)

                if raw1 == 1:
                        roundmessage += "\n\n {} has a critical miss \n\n".format(dueler1.name)
                        dueler1.apply_injury()
                if raw2 == 1:
                        roundmessage += "\n\n {} has a critical miss \n\n".format(dueler2.name)
                        dueler2.apply_injury()

                roundmessage += "\n\n The morale of the duellists currently stand as the following \n\n"
                roundmessage += "**{}** Morale: {} \n \n".format(dueler1.name,dueler1.morale)
                roundmessage += "**{}** Morale: {} \n \n".format(dueler2.name,dueler2.morale)
                roundmessage += "--- \n \n"  

                if (dueler2.morale <= 0) or (dueler2.morale <= (dueler2.startpoint + dueler2.threshold)) or (dueler2.continueFighting == False):
                        #Dueler 1 has won
                        dueler2.continueFighting = False
                        roundmessage += "{} defeats {}, bringing an end to the duel.\n \n".format(dueler1.name,dueler2.name)
                        roundmessage += "**Winner: {}**\n \n".format(dueler1.name)
                        roundmessage += "**Winner's Remaining Morale: {}**\n \n".format(dueler1.morale)
                        roundmessage += "Rounds taken: {} \n \n".format(roundCount)

                elif (dueler1.morale <= 0) or (dueler1.morale <= (dueler1.startpoint + dueler1.threshold)) or (dueler1.continueFighting == False):
                        #Dueler 2 has won
                        dueler1.continueFighting = False
                        roundmessage += "{} defeats {}, bringing an end to the duel.\n \n".format(dueler2.name,dueler1.name)
                        roundmessage += "**Winner: {}**\n \n".format(dueler2.name)
                        roundmessage += "**Winner's Remaining Morale: {}**\n \n".format(dueler2.morale)
                        roundmessage += "Rounds taken: {} \n \n".format(roundCount)
        
                return roundmessage

        def run(self,duelInfo):
                roundCount = 1
                                
                dueler1 = Dueler.Dueler(duelInfo.group(1), int(duelInfo.group(2)), int(duelInfo.group(3)))
                dueler2 = Dueler.Dueler(duelInfo.group(6), int(duelInfo.group(7)), int(duelInfo.group(8))) ##
                
                dueler1.morale += int(duelInfo.group(4))
                dueler1.extradmg += int(duelInfo.group(5))
                dueler2.morale += int(duelInfo.group(9))
                dueler2.extradmg += int(duelInfo.group(10))


                dueler1.startpoint += dueler1.morale
                dueler2.startpoint += dueler2.morale

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
