import re
import random
import Dueler
import Globals

class Duel:
        
       
        Globals.message = 1

        def run_round(self,dueler1,dueler2,roundCount):
               
                
                roundmessage = "##**Round {}** \n \n".format(roundCount)
              
                if False:
                        print("")
                        
                else:      
                        raw1 = dueler1.attack_roll()
                        raw2 = dueler2.attack_roll()
                        roll1 = raw1 + dueler1.bonus
                        roll2 = raw2 + dueler2.bonus

                        roundmessage += "**{}** Roll: {} ({}{:+})\n \n".format(dueler1.name,roll1,raw1,dueler1.bonus)
                        roundmessage += "**{}** Roll: {} ({}{:+})\n \n".format(dueler2.name,roll2,raw2,dueler2.bonus)
                        roundmessage += "\n\n *** \n\n"
                        
                        if roll1 > roll2:
                                dmgDealt = dueler1.damage_roll()
                                dueler2.morale -= dmgDealt
                                roundmessage += "**Damage** Roll: {} ({}{:+})\n \n".format(dmgDealt,dmgDealt-dueler1.extradmg,dueler1.extradmg)
                                roundmessage += "\n\n *** \n\n"
                                roundmessage += "\n\n {} hits {}".format(dueler1.name,dueler2.name)
                        elif roll2 > roll1:
                                dmgDealt = dueler2.damage_roll()
                                dueler1.morale -= dmgDealt
                                roundmessage += "**Damage** Roll: {} ({}{:+})\n \n".format(dmgDealt,dmgDealt-dueler2.extradmg,dueler2.extradmg)
                                roundmessage += "\n\n *** \n\n"   
                                roundmessage += "\n\n {} hits {} \n\n".format(dueler2.name,dueler1.name)

                        
                        if raw1 == 1:
                                if dueler1.ignoreInjury > 0:
                                        dueler1.ignoreInjury -= 1
                                else:
                                        dueler1.bonus -= 2
                                roundmessage += "\n\n {} has a critical miss \n\n".format(dueler1.name)
                        elif (raw1 == 19 and dueler1.tier3 == 1) or (raw1 == 20):
                                if dueler2.ignoreInjury > 0:
                                        dueler2.ignoreInjury -= 1
                                else:
                                        if dueler1.tier3 == 3:
                                                dueler2.bonus -= 4
                                        else:
                                                dueler2.bonus -= 2
                                roundmessage += "\n\n {} has a critical hit \n\n".format(dueler1.name)
                        if raw2 == 1:
                                if dueler2.ignoreInjury > 0:
                                        dueler2.ignoreInjury -= 1
                                else:
                                        dueler2.bonus -= 2
                                roundmessage += "\n\n {} has a critical miss \n\n".format(dueler2.name)
                        elif (raw2 == 19 and dueler2.tier3 == 1) or (raw2 == 20):
                                if dueler1.ignoreInjury > 0:
                                        dueler1.ignoreInjury -= 1
                                else:
                                        if dueler2.tier3 == 3:
                                                dueler1.bonus -= 4
                                        else:
                                                dueler1.bonus -= 2
                                roundmessage += "\n\n {} has a critical hit \n\n".format(dueler2.name)

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
        
        def numberGen(self,maxCount):
                newMessage = random.randint(1,maxCount)
                while (newMessage == Globals.message):
                        newMessage = random.randint(1,maxCount)
                return newMessage
                        

        def run(self,duelInfo):
                roundCount = 1
                                
                dueler1 = Dueler.Dueler(duelInfo.group(1), int(duelInfo.group(2)), int(duelInfo.group(3)))
                dueler2 = Dueler.Dueler(duelInfo.group(5), int(duelInfo.group(6)), int(duelInfo.group(7)))
                

                if duelInfo.group(4) == "Masterwork":
                        dueler1.extradmg += 1
                elif duelInfo.group(4) == "VS":
                        dueler1.extradmg += 3
                elif duelInfo.group(4) == "Duelist1":
                        dueler1.bonus += 2
                elif duelInfo.group(4) == "Duelist2":
                        dueler1.bonus += 4
                elif duelInfo.group(4) == "Duelist3":
                        dueler1.bonus += 6
                        dueler1.tier3 = 1
                elif duelInfo.group(4) == "IronWill1":
                        dueler1.morale += 5
                        dueler1.ignoreInjury += 1
                elif duelInfo.group(4) == "IronWill2":
                        dueler1.morale += 10
                        dueler1.ignoreInjury += 1
                elif duelInfo.group(4) == "IronWill3":
                        dueler1.morale += 15
                        dueler1.ignoreInjury += 2
                        dueler1.bonus += 2
                elif duelInfo.group(4) ==  "Bulwark1":
                        dueler1.bonus -= 1
                        dueler1.extradmg += 2
                elif duelInfo.group(4) == "Bulwark2":
                        dueler1.extradmg += 2
                elif duelInfo.group(4) == "Bulwark3":
                        dueler1.extradmg += 2
                        dueler1.tier3 = 3
                dueler1.startpoint = dueler1.morale
                
                if duelInfo.group(8) == "Masterwork":
                        dueler2.extradmg += 1
                elif duelInfo.group(8) == "VS":
                        dueler2.extradmg += 3
                elif duelInfo.group(8) == "Duelist1":
                        dueler2.bonus += 2
                elif duelInfo.group(8) == "Duelist2":
                        dueler2.bonus += 4
                elif duelInfo.group(8) == "Duelist3":
                        dueler2.bonus += 6
                        dueler2.tier3 = 1
                elif duelInfo.group(8) == "IronWill1":
                        dueler2.morale += 5
                        dueler2.ignoreInjury += 1
                elif duelInfo.group(8) == "IronWill2":
                        dueler2.morale += 10
                        dueler2.ignoreInjury += 1
                elif duelInfo.group(8) == "IronWill3":
                        dueler2.morale += 15
                        dueler2.ignoreInjury += 2
                        dueler2.bonus += 2
                elif duelInfo.group(8) ==  "Bulwark1":
                        dueler2.bonus -= 1
                        dueler2.extradmg += 2
                elif duelInfo.group(8) == "Bulwark2":
                        dueler2.extradmg += 2
                elif duelInfo.group(8) == "Bulwark3":
                        dueler2.extradmg += 2
                        dueler2.tier3 = 3
                dueler2.startpoint = dueler2.morale

                print(dueler1.bonus)
                print(dueler2.bonus)
                
                battlemessage = "#Duel Between {} and {} \n \n".format(dueler1.name,dueler1.name)                       
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
