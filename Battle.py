import re
import random
import Army
import Globals
from math import ceil
class Battle:
        
       
        Globals.message = 1

        def run_round(self,army1,army2,roundCount):
               
                
                roundmessage = "##**Round {}** \n \n".format(roundCount)
              
                if False:
                        print("")
                        
                else:      
                        noDice = 2
                        number = 0
                        printedBonus = 0
                        numberBonus = 0
                        runningBonus = "("           
                        while(noDice != number):  
                            random.seed()
                            printed = random.randint(1,50)
                            printedBonus += printed
                            if (noDice - number == 1):
                                runningBonus += "{})".format(printed)
                            else:
                                runningBonus += "{} + ".format(printed)
                            number += 1   
                        roll1 = printedBonus + army1.bonus
                        
                        roundmessage += "**{}** Roll: {} ({}{:+})\n \n".format(army1.name,roll1,roll1-army1.bonus,army1.bonus)
                        if (army1.bonus > 0):
                            roundmessage += "\n\n {} + {} \n\n".format(runningBonus,army1.bonus)
                        elif (army1.bonus < 0):
                            roundmessage += "\n\n {} {} \n\n".format(runningBonus,army1.bonus)
                        elif (noDice > 1):
                            roundmessage += "\n\n {} \n\n".format(runningBonus)
                        else:
                            roundmessage += "\n\n *** \n\n"
                        
                        noDice = 2
                        number = 0
                        printedBonus = 0
                        numberBonus = 0
                        runningBonus = "("           
                        while(noDice != number):     
                            random.seed()
                            printed = random.randint(1,50)
                            printedBonus += printed
                            if (noDice - number == 1):
                                runningBonus += "{})".format(printed)
                            else:
                                runningBonus += "{} + ".format(printed)
                            number += 1   
                        roll2 = printedBonus + army2.bonus
                        
                        roundmessage += "**{}** Roll: {} ({}{:+})\n \n".format(army2.name,roll2,roll2-army2.bonus,army2.bonus)
                        if (army2.bonus > 0):
                            roundmessage += "\n\n {} + {} \n\n".format(runningBonus,army2.bonus)
                        elif (army2.bonus < 0):
                            roundmessage += "\n\n {} {} \n\n".format(runningBonus,army2.bonus)
                        elif (noDice > 1):
                            roundmessage += "\n\n {} \n\n".format(runningBonus)
                        else:
                            roundmessage += "\n\n *** \n\n"
                        
                        if True:
                                if(roll1>roll2):
                                        gap = roll1 - roll2                                       
                                        army2.morale -= gap
                                        army1.roundsWon += 1
                                        
                                        check = army2.startPoint + army2.threshold
                                        if(army2.morale <= 0 or army2.morale <= check):
                                                #Attacker Won
                                                #Logs that the army cannot fight, bringing the battle to an end.
                                                army2.continueFighting = False
                                                roundmessage += "{} defeats {}, bringing an end to the battle.\n \n".format(army1.name,army2.name)
                                                roundmessage += "**Winner: {}**\n \n".format(army1.name)
                                                roundmessage += "**Winner's Remaining Morale: {}**\n \n".format(army1.morale)
                                                roundmessage += "Rounds taken: {} \n \n".format(roundCount)
                                
                                elif(roll2>roll1):
                                        gap = roll2 - roll1                                       
                                        army1.morale -= gap
                                        army2.roundsWon += 1
                                         
                                        check = army1.startPoint + army1.threshold
                                        if(army1.morale <= 0 or army1.morale <= check):
                                                 #Defender Won
                                                army1.continueFighting = False
                                                roundmessage += "{} defeats {}, bringing an end to the battle.\n \n \n".format(army2.name,army1.name)
                                                roundmessage += "**Winner: {}**\n \n".format(army2.name)
                                                roundmessage += "**Winner's Remaining Morale: {}**\n \n".format(army2.morale)
                                                roundmessage += "Rounds taken: {} \n \n".format(roundCount)                               
                                 
            
                #Godamn python globals. Logs the phase to print out and calculate casualties. Each pass through will add casualties onto the previous, making the total.
                roundmessage += "*** \n\n The morale of the armies currently stand as the following \n\n"
                roundmessage += "**{}** Morale: {} \n \n".format(army1.name,army1.morale)
                roundmessage += "**{}** Morale: {} \n \n".format(army2.name,army2.morale)
                roundmessage += "--- \n \n"                        
                
                        
                return roundmessage
        
        def numberGen(self,maxCount):
                newMessage = random.randint(1,maxCount)
                while (newMessage == Globals.message):
                        newMessage = random.randint(1,maxCount)
                return newMessage
                        

        def run(self,battleInfo):
                roundCount = 1
                autosurrender = 0
                
                if(battleInfo.group(2)):
                        group2 = battleInfo.group(2)
                else:
                        group2 = 0

                if (battleInfo.group(3)):
                    group3 = battleInfo.group(3)
                else:
                    group3 = 0


                if(battleInfo.group(6)):
                        group6 = battleInfo.group(6)
                else:
                        group6 = 0

                if(battleInfo.group(8)):
                        group8 = battleInfo.group(8)
                else:
                        group8 = 0

                if (battleInfo.group(9)):
                    group9 = battleInfo.group(9)
                else:
                    group9 = 0

                if(battleInfo.group(12)):
                        group12 = battleInfo.group(12)
                else:
                        group12 = 0
                
                
                army1 = Army.Army(battleInfo.group(1), int(group2), battleInfo.group(4), int(battleInfo.group(5)), int(group6))
                army2 = Army.Army(battleInfo.group(7), int(group8), battleInfo.group(10), int(battleInfo.group(11)), int(group12))

                army1.morale += int(group3)
                army2.morale += int(group9)
                army1.startPoint += int(group3)
                army2.startPoint += int(group9)

                if(army1.power == 0):
                        autosurrender = 1
                elif(army2.power == 0):
                        autosurrender = 2
                elif(army1.power > army2.power and Globals.battleType == "Naval"):
                        difference = (army1.power / army2.power) - 1
                        difference *= 100
                        print(difference)
                        if(difference < 5):
                                army1.bonus += 0
                        else:
                                army1.bonus += ceil(difference / 40)
                        if(army1.bonus >= 31):
                                autosurrender = 2
                elif(army2.power > army1.power and Globals.battleType == "Naval"):
                        difference = (army2.power / army1.power) - 1
                        difference *= 100
                        print(difference)
                        if (difference < 5):
                                army2.bonus += 0
                        else:
                                army2.bonus += ceil(difference / 40)
                        if (army2.bonus >= 31):
                                autosurrender = 1
                elif(army1.power > army2.power and Globals.battleType != "Naval"):
                        difference = (army1.power / army2.power) - 1
                        difference *= 100
                        print(difference)
                        if (difference < 5):
                                army1.bonus += 0
                        else:
                                army1.bonus += ceil(difference / 20)
                        if (army1.bonus >= 31):
                             autosurrender = 2
                elif(army2.power > army1.power and Globals.battleType != "Naval"):
                        difference = (army2.power / army1.power) - 1
                        difference *= 100
                        print(difference)
                        if (difference < 5):
                                army2.bonus += 0
                        else:
                                army2.bonus += ceil(difference / 20)
                        if (army2.bonus >= 31):
                                autosurrender = 1

                
                if(Globals.battleType == "Naval"):
                        battlemessage = "#Naval Battle Between {} and {} \n \n".format(army1.name,army2.name)                       
                else:
                        battlemessage = "#Land Battle Between {} and {} \n \n".format(army1.name,army2.name)
                battlemessage += "--- \n \n"

                if(autosurrender == 1):
                        battlemessage += "The {} army cannot battle and surrender to the enemy force \n \n".format(army1.name)
                elif(autosurrender == 2):
                        battlemessage += "The {} army cannot battle and surrender to the enemy force \n \n".format(army2.name)
                else:
                        battlemessage += self.run_round(army1,army2,roundCount)
                        while(army1.continueFighting and army2.continueFighting):
                                roundCount += 1
                                battlemessage += self.run_round(army1,army2,roundCount)


                        battlemessage += "#**Casualties** \n \n".format(army1.name,army2.name)

                        army1cas, army1msg = self.casualties(army1, roundCount)
                        army2cas, army2msg = self.casualties(army2, roundCount)

                        if(army1.power > army2.power):
                                casualtyReduction = 1 - (0.05 * (army1.bonus - army1.miscBonus))
                                if (casualtyReduction < 0.5):
                                    casualtyReduction = 0.5
                                army1cas = army1cas * casualtyReduction
                                army1msg += " _[Reduced by {}%]_".format(casualtyReduction*100)
                        elif(army2.power > army1.power):
                                casualtyReduction = 1 - (0.05 * (army2.bonus - army2.miscBonus))
                                if(casualtyReduction < 0.5):
                                        casualtyReduction = 0.5
                                army2cas = army2cas * casualtyReduction
                                army2msg += " _[Reduced by {}%]_".format(round((1-casualtyReduction)*100, 2))


                        battlemessage += "{} Casualties = {}% \n\n {} \n\n {} Casualties = {}% \n\n {} \n\n _Please remember to manually calculate retreats and routs, and how they affect casualties_ \n\n".format(army1.name,army1cas,army1msg,army2.name,army2cas,army2msg)
                        battlemessage += "--- \n \n"
      
                return battlemessage
                print ("Finished battle")
                self.reset_battle_phase()

        def casualties(self, army, roundCount):
                noDice = roundCount - army.roundsWon
                number = 0
                printedBonus = roundCount
                runningBonus = "("
                while (noDice != number):
                        random.seed()
                        printed = random.randint(1, 3)
                        printedBonus += printed
                        if (noDice - number == 1):
                                runningBonus += "{})".format(printed)
                        else:
                                runningBonus += "{} + ".format(printed)
                        number += 1
                runningBonus += " + {}".format(roundCount)

                return printedBonus, runningBonus

        def reset_battle_phase(self):
                print("Reset")
