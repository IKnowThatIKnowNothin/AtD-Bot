import re
import random
import Army
import Globals
class Battle:
        
       
        Globals.message = 1

        def run_round(self,army1,army2,roundCount):
               
                
                roundmessage = "##**Round {}** \n \n".format(roundCount)
              
                if False:
                        print("")
                        
                else:      
                        noDice = 5
                        number = 0
                        printedBonus = 0
                        numberBonus = 0
                        runningBonus = "("           
                        while(noDice != number):  
                            random.seed()
                            printed = random.randint(1,20)
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
                        
                        noDice = 5
                        number = 0
                        printedBonus = 0
                        numberBonus = 0
                        runningBonus = "("           
                        while(noDice != number):     
                            random.seed()
                            printed = random.randint(1,20)
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
                                        
                                        check = 100 + army2.threshold                                      
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
                                         
                                        check = 100 + army1.threshold
                                        if(army1.morale <= 0 or army1.morale <= check):
                                                 #Defender Won
                                                army1.continueFighting = False
                                                roundmessage += "{} defeats {}, bringing an end to the battle.\n \n \n".format(army2.name,army1.name)
                                                roundmessage += "**Winner: {}**\n \n".format(army2.name)
                                                roundmessage += "**Winner's Remaining Morale: {}**\n \n".format(army2.morale)
                                                roundmessage += "Rounds taken: {} \n \n".format(roundCount)                               
                                 
            
                #Godamn python globals. Logs the phase to print out and calculate casualties. Each pass through will add casualties onto the previous, making the total.
                global attackcas
                global defendcas
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
                global attackcas
                global defendcas
                attackcas = 0
                defendcas = 0
                autosurrender = 0
                
                if(battleInfo.group(2)):
                        group2 = battleInfo.group(2)
                else:
                        group2 = 0
                if(battleInfo.group(6)):
                        group6 = battleInfo.group(6)
                else:
                        group6 = 0
                if(battleInfo.group(8)):
                        group8 = battleInfo.group(8)
                else:
                        group8 = 0
                if(battleInfo.group(12)):
                        group12 = battleInfo.group(12)
                else:
                        group12 = 0
                
                
                army1 = Army.Army(battleInfo.group(1), int(group2), battleInfo.group(4), int(battleInfo.group(5)), int(group6))
                army2 = Army.Army(battleInfo.group(7), int(group8), battleInfo.group(10), int(battleInfo.group(11)), int(group12))

                global extramorale1
                extramorale1 = 0
                global extramorale2
                extramorale2 = 0

                if(battleInfo.group(3) == " Inspiring1"):
                        army1.morale += 15
                elif(battleInfo.group(3) == " Inspiring2"):
                        army1.morale += 35
                elif(battleInfo.group(3) == " Inspiring3"):
                        army1.morale += 50
                        
                if(battleInfo.group(9) == " Inspiring1"):
                        army2.morale += 15
                if(battleInfo.group(9) == " Inspiring2"):
                        army2.morale += 35
                if(battleInfo.group(9) == " Inspiring3"):
                        army2.morale += 50

                if(army1.power == 0):
                        autosurrender = 1
                elif(army2.power == 0):
                        autosurrender = 2
                elif(army1.power > army2.power and Globals.battleType == "Naval"):
                        print("A1")
                        difference = (army1.power / army2.power) - 1
                        difference *= 100
                        print(difference)
                        if(difference <= 2.5):
                                army1.bonus += 0
                        elif(difference <= 20):
                                army1.bonus += 1
                        elif(difference <= 40):
                                army1.bonus += 2
                        elif(difference <= 60):
                                army1.bonus += 3
                        elif(difference <= 80):
                                army1.bonus += 4
                        elif(difference <= 100):
                                army1.bonus += 5
                        elif(difference <= 120):
                                army1.bonus += 6
                        elif(difference <= 140):
                                army1.bonus += 7
                        elif(difference <= 160):
                                army1.bonus += 8
                        elif(difference <= 180):
                                army1.bonus += 9
                        elif(difference <= 200):
                                army1.bonus += 10
                        elif(difference <= 220):
                                army1.bonus += 11
                        elif(difference <= 240):
                                army1.bonus += 12
                        elif(difference <= 260):
                                army1.bonus += 13
                        elif(difference <= 280):
                                army1.bonus += 14
                        elif(difference <= 300):
                                army1.bonus += 15
                        elif(difference <= 320):
                                army1.bonus += 16
                        elif(difference <= 340):
                                army1.bonus += 17
                        elif(difference <= 360):
                                army1.bonus += 18
                        elif(difference <= 380):
                                army1.bonus += 19
                        elif(difference <= 400):
                                army1.bonus += 20
                        elif(difference <= 420):
                                army1.bonus += 21
                        elif(difference <= 440):
                                army1.bonus += 22
                        elif(difference <= 460):
                                army1.bonus += 23
                        elif(difference <= 480):
                                army1.bonus += 24
                        elif(difference <= 500):
                                army1.bonus += 25
                        elif(difference <= 520):
                                army1.bonus += 26
                        elif(difference <= 540):
                                army1.bonus += 27
                        elif(difference <= 560):
                                army1.bonus += 28
                        elif(difference <= 580):
                                army1.bonus += 29
                        else:
                                army1.bonus += 30
                                #autosurrender = 2
                                print("")
                elif(army2.power > army1.power and Globals.battleType == "Naval"):
                        print("A2")
                        difference = (army2.power / army1.power) - 1
                        difference *= 100
                        print(difference)
                        if(difference <= 2.5):
                                army1.bonus += 0
                        elif(difference <= 20):
                                army1.bonus += 1
                        elif(difference <= 40):
                                army2.bonus += 2
                        elif(difference <= 60):
                                army2.bonus += 3
                        elif(difference <= 80):
                                army2.bonus += 4
                        elif(difference <= 100):
                                army2.bonus += 5
                        elif(difference <= 120):
                                army2.bonus += 6
                        elif(difference <= 140):
                                army2.bonus += 7
                        elif(difference <= 160):
                                army2.bonus += 8
                        elif(difference <= 180):
                                army2.bonus += 9
                        elif(difference <= 200):
                                army2.bonus += 10
                        elif(difference <= 220):
                                army2.bonus += 11
                        elif(difference <= 240):
                                army2.bonus += 12
                        elif(difference <= 260):
                                army2.bonus += 13
                        elif(difference <= 280):
                                army2.bonus += 14
                        elif(difference <= 300):
                                army2.bonus += 15
                        elif(difference <= 320):
                                army2.bonus += 16
                        elif(difference <= 340):
                                army2.bonus += 17
                        elif(difference <= 360):
                                army2.bonus += 18
                        elif(difference <= 380):
                                army2.bonus += 19
                        elif(difference <= 400):
                                army2.bonus += 20
                        elif(difference <= 420):
                                army2.bonus += 21
                        elif(difference <= 440):
                                army2.bonus += 22
                        elif(difference <= 460):
                                army2.bonus += 23
                        elif(difference <= 480):
                                army2.bonus += 24
                        elif(difference <= 500):
                                army2.bonus += 25
                        elif(difference <= 520):
                                army2.bonus += 26
                        elif(difference <= 540):
                                army2.bonus += 27
                        elif(difference <= 560):
                                army2.bonus += 28
                        elif(difference <= 580):
                                army2.bonus += 29
                        else:
                                army2.bonus += 30
                                #autosurrender = 1
                                print("")
                elif(army1.power > army2.power and Globals.battleType != "Naval"):
                        difference = (army1.power / army2.power) - 1
                        difference *= 100
                        print(difference)
                        if(difference <= 5):
                                army1.bonus += 0
                        elif(difference <= 20):
                                army1.bonus += 1
                        elif(difference <= 40):
                                army1.bonus += 2
                        elif(difference <= 60):
                                army1.bonus += 3
                        elif(difference <= 80):
                                army1.bonus += 4
                        elif(difference <= 100):
                                army1.bonus += 5
                        elif(difference <= 120):
                                army1.bonus += 6
                        elif(difference <= 140):
                                army1.bonus += 7
                        elif(difference <= 160):
                                army1.bonus += 8
                        elif(difference <= 180):
                                army1.bonus += 9
                        elif(difference <= 200):
                                army1.bonus += 10
                        elif(difference <= 220):
                                army1.bonus += 11
                        elif(difference <= 240):
                                army1.bonus += 12
                        elif(difference <= 260):
                                army1.bonus += 13
                        elif(difference <= 280):
                                army1.bonus += 14
                        elif(difference <= 300):
                                army1.bonus += 15
                        elif(difference <= 320):
                                army1.bonus += 16
                        elif(difference <= 340):
                                army1.bonus += 17
                        elif(difference <= 360):
                                army1.bonus += 18
                        elif(difference <= 380):
                                army1.bonus += 19
                        elif(difference <= 400):
                                army1.bonus += 20
                        elif(difference <= 420):
                                army1.bonus += 21
                        elif(difference <= 440):
                                army1.bonus += 22
                        elif(difference <= 460):
                                army1.bonus += 23
                        elif(difference <= 480):
                                army1.bonus += 24
                        elif(difference <= 500):
                                army1.bonus += 25
                        elif(difference <= 520):
                                army1.bonus += 26
                        elif(difference <= 540):
                                army1.bonus += 27
                        elif(difference <= 560):
                                army1.bonus += 28
                        elif(difference <= 580):
                                army1.bonus += 29
                        else:
                                army1.bonus += 30
                                #autosurrender = 2
                                print("")
                elif(army2.power > army1.power and Globals.battleType != "Naval"):
                        difference = (army2.power / army1.power) - 1
                        difference *= 100
                        print(difference)
                        if(difference <= 5):
                                army1.bonus += 0
                        elif(difference <= 20):
                                army1.bonus += 1
                        elif(difference <= 40):
                                army2.bonus += 2
                        elif(difference <= 60):
                                army2.bonus += 3
                        elif(difference <= 80):
                                army2.bonus += 4
                        elif(difference <= 100):
                                army2.bonus += 5
                        elif(difference <= 120):
                                army2.bonus += 6
                        elif(difference <= 140):
                                army2.bonus += 7
                        elif(difference <= 160):
                                army2.bonus += 8
                        elif(difference <= 180):
                                army2.bonus += 9
                        elif(difference <= 200):
                                army2.bonus += 10
                        elif(difference <= 220):
                                army2.bonus += 11
                        elif(difference <= 240):
                                army2.bonus += 12
                        elif(difference <= 260):
                                army2.bonus += 13
                        elif(difference <= 280):
                                army2.bonus += 14
                        elif(difference <= 300):
                                army2.bonus += 15
                        elif(difference <= 320):
                                army2.bonus += 16
                        elif(difference <= 340):
                                army2.bonus += 17
                        elif(difference <= 360):
                                army2.bonus += 18
                        elif(difference <= 380):
                                army2.bonus += 19
                        elif(difference <= 400):
                                army2.bonus += 20
                        elif(difference <= 420):
                                army2.bonus += 21
                        elif(difference <= 440):
                                army2.bonus += 22
                        elif(difference <= 460):
                                army2.bonus += 23
                        elif(difference <= 480):
                                army2.bonus += 24
                        elif(difference <= 500):
                                army2.bonus += 25
                        elif(difference <= 520):
                                army2.bonus += 26
                        elif(difference <= 540):
                                army2.bonus += 27
                        elif(difference <= 560):
                                army2.bonus += 28
                        elif(difference <= 580):
                                army2.bonus += 29
                        else:
                                army2.bonus += 30
                                #autosurrender = 1

                
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
                        if (Globals.battleType == "Naval"):
                                if(100 - army1.morale >= 100):
                                        attackcas += 50
                                        for x in range(6):
                                                attackcas += self.numberGen(7)
                                elif(100 - army1.morale >= 76):
                                        attackcas += 30
                                        for x in range(3):
                                                attackcas += self.numberGen(5)
                                elif(100 - army1.morale >= 61):
                                        attackcas += 20
                                        for x in range(2):
                                                attackcas += self.numberGen(5)
                                elif(100 - army1.morale >= 45):
                                        attackcas += 12
                                        for x in range(1):
                                                attackcas += self.numberGen(8)
                                elif(100 - army1.morale >= 31):
                                        attackcas += 8
                                        for x in range(1):
                                                attackcas += self.numberGen(4)
                                elif(100 - army1.morale >= 16):
                                        attackcas += 5
                                        for x in range(1):
                                                attackcas += self.numberGen(3)
                                elif(100 - army1.morale >= 6):
                                        attackcas += 3
                                        for x in range(1):
                                                attackcas += self.numberGen(2)
                                else:
                                        attackcas += 0
                                                
                                if(100 - army2.morale >= 100):
                                        defendcas += 50
                                        for x in range(6):
                                                defendcas += self.numberGen(7)
                                elif(100 - army2.morale >= 76):
                                        defendcas += 30
                                        for x in range(3):
                                                defendcas += self.numberGen(5)
                                elif(100 - army2.morale >= 61):
                                        defendcas += 20
                                        for x in range(2):
                                                defendcas += self.numberGen(5)
                                elif(100 - army2.morale >= 45):
                                        defendcas += 12
                                        for x in range(1):
                                                defendcas += self.numberGen(4)
                                elif(100 - army2.morale >= 31):
                                        defendcas += 8
                                        for x in range(1):
                                                defendcas += self.numberGen(4)
                                elif(100 - army2.morale >= 16):
                                        defendcas += 5
                                        for x in range(1):
                                                defendcas += self.numberGen(3)
                                elif(100 - army2.morale >= 6):
                                        defendcas += 3
                                        for x in range(1):
                                                defendcas += self.numberGen(2)
                                else:
                                        defendcas += 0
                                                
                        #Land Battle casualties          
                        else:
                                if(100 - army1.morale >= 100):
                                        attackcas += 35
                                        for x in range(3):
                                                attackcas += self.numberGen(5)
                                elif(100 - army1.morale >= 76):
                                        attackcas += 30
                                        for x in range(3):
                                                attackcas += self.numberGen(5)
                                elif(100 - army1.morale >= 61):
                                        attackcas += 20
                                        for x in range(2):
                                                attackcas += self.numberGen(5)
                                elif(100 - army1.morale >= 45):
                                        attackcas += 12
                                        for x in range(1):
                                                attackcas += self.numberGen(8)
                                elif(100 - army1.morale >= 31):
                                        attackcas += 8
                                        for x in range(1):
                                                attackcas += self.numberGen(4)
                                elif(100 - army1.morale >= 16):
                                        attackcas += 5
                                        for x in range(1):
                                                attackcas += self.numberGen(3)
                                elif(100 - army1.morale >= 6):
                                        attackcas += 3
                                        for x in range(1):
                                                attackcas += self.numberGen(2)
                                else:
                                        for x in range(1):
                                                attackcas += self.numberGen(3)
                                                
                                if(100 - army2.morale >= 100):
                                        defendcas += 35
                                        for x in range(3):
                                                defendcas += self.numberGen(5)
                                elif(100 - army2.morale >= 76):
                                        defendcas += 30
                                        for x in range(3):
                                                defendcas += self.numberGen(5)
                                elif(100 - army2.morale >= 61):
                                        defendcas += 20
                                        for x in range(2):
                                                defendcas += self.numberGen(5)
                                elif(100 - army2.morale >= 45):
                                        defendcas += 12
                                        for x in range(1):
                                                defendcas += self.numberGen(8)
                                elif(100 - army2.morale >= 31):
                                        defendcas += 8
                                        for x in range(1):
                                                defendcas += self.numberGen(4)
                                elif(100 - army2.morale >= 16):
                                        defendcas += 5
                                        for x in range(1):
                                                defendcas += self.numberGen(3)
                                elif(100 - army2.morale >= 6):
                                        defendcas += 3
                                        for x in range(1):
                                                defendcas += self.numberGen(2)
                                else:
                                        for x in range(1):
                                                defendcas += self.numberGen(3)                                 
                                                

                battlemessage += "{} Casualties = {}% \n\n {} Casualties = {}% \n\n _Please remember to manually complete the relative army size calculation for casualities_ \n\n".format(army1.name,attackcas,army2.name,defendcas)
                battlemessage += "--- \n \n"                                
      
                return battlemessage
                print ("Finished battle")
                self.reset_battle_phase()
                
        def reset_battle_phase(self):
               print("Reset")
