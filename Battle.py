import re
import random
import Army
import Globals
class Battle:
        
        battlePhase = 0
        Globals.message = 1

        def run_round(self,army1,army2,roundCount):
                phase = 'Even'
                
                roundmessage = "##**Round {}** \n \n".format(roundCount)

                if(roundCount == 0):
                        if(Globals.battleType == 'Naval'):
                                self.battlePhase = 0
                                Globals.message = random.randint(1,4)
                                #message = FlavourText.FlavourText(4)
                                if(Globals.message == 1):
                                        roundmessage += "{} notices {} ships on the horizon, preparing to attack!\n \n".format(army2.commanderName,army1.name)
                                elif(Globals.message == 2):
                                        roundmessage += "{} locks eyes with the enemy commander and orders the attack!\n \n".format(army1.commanderName)
                                elif(Globals.message == 3):
                                        roundmessage += "{} launches an attack on the {} ships!.\n \n".format(army1.commanderName,army2.name)
                                elif(Globals.message == 4):
                                        roundmessage += "The {} ships turn to face the enemy as they engage!\n \n".format(army2.name)
                        elif(Globals.battleType == 'Ambush'):
                                self.battlePhase = 999
                                army2.morale -= 2
                                Globals.message = random.randint(1,4)
                                if(Globals.message == 1):
                                        roundmessage += "{} notices {} troops rushing out to ambush them!\n \n".format(army2.commanderName,army1.name)
                                elif(Globals.message == 2):
                                        roundmessage += "{} watches their opponent from their hidden vantage and launches their attack!\n \n".format(army1.commanderName)
                                elif(Globals.message == 3):
                                        roundmessage += "The {} troops notice too late an enemy force rushing forward to attack!.\n \n".format(army2.name)
                                elif(Globals.message == 4):
                                        roundmessage += "The {} men wait for their enemy to pass before launching their attack!\n \n".format(army1.name)
                        elif(Globals.battleType == 'Assault'):
                                self.battlePhase = 999
                                Globals.message = random.randint(1,4)
                                if(Globals.message == 1):
                                        roundmessage += "{} gives the order to attack the {} walls!\n \n".format(army1.commanderName,army2.name)
                                elif(Globals.message == 2):
                                        roundmessage += "{} watches as the army below launch an assault on their walls!\n \n".format(army2.commanderName)
                                elif(Globals.message == 3):
                                        roundmessage += "The {} troops charge forward in an attempt to breach the {} walls!.\n \n".format(army1.name,army2.name)
                                elif(Globals.message == 4):
                                        roundmessage += "The {} men stand ready on the walls, ready to repel the invaders!\n \n".format(army2.name)
                        else:
                                self.battlePhase = 999
                                Globals.message = random.randint(1,4)
                                if(Globals.message == 1):
                                        roundmessage += "{} notices {} forces on the horizon, preparing to attack!\n \n".format(army2.commanderName,army1.name)
                                elif(Globals.message == 2):
                                        roundmessage += "{} locks eyes with the enemy commander and orders the attack!\n \n".format(army1.commanderName)
                                elif(Globals.message == 3):
                                        roundmessage += "{} launches an attack on the {} troops!.\n \n".format(army1.commanderName,army2.name)
                                elif(Globals.message == 4):
                                        roundmessage += "The {} men turn to face the enemy as they engage!\n \n".format(army2.name)
                                                

                else:              
                        roll1 = army1.attack_roll()
                        roll2 = army2.attack_roll()
                                        
                                        
                        roundmessage += "**{}** Roll: {} ({}{:+})\n \n".format(army1.name,roll1,roll1-army1.bonus,army1.bonus)
                        roundmessage += "**{}** Roll: {} ({}{:+})\n \n".format(army2.name,roll2,roll2-army2.bonus,army2.bonus)


                        #fun bit of code to determine which phase it is. Logs it in battlePhase, attacker winning adds numbers, defender subtracts with 0 being even
                        if(Globals.battleType=='Naval'):        
                                if(roll1 > roll2):
                                        difference = roll1-roll2

                                        if(difference >= 96):
                                                self.battlePhase += 10

                                        elif(difference >= 75):
                                                self.battlePhase += 2
                                                if(Globals.battleType == 'Naval'):
                                                        Globals.message = self.numberGen(4)
                                                        #message = random.randint(1,4)
                                                        if(Globals.message == 1):
                                                                roundmessage += "A {} ship rams into one of their opponent's ships, flooding the deck with men.\n \n".format(army1.name)
                                                        elif(Globals.message == 2):
                                                                roundmessage += "{} orders a volley upon one of the {} ships, bringing death to their opponent.\n \n".format(army1.commanderName,army2.name)
                                                        elif(Globals.message == 3):
                                                                roundmessage += "{} misjudges where the next attack will come from, leaving several {} ships undefended.\n \n".format(army2.commanderName,army2.name)
                                                        elif(Globals.message == 4):
                                                                roundmessage += "The {} ships come upon an isolated {} ship, and easily kill those aboard.\n \n".format(army1.name,army2.name)
                                                else:
                                                        Globals.message = self.numberGen(4)
                                                        if(Globals.message == 1):
                                                                roundmessage += "{} orders a charge, breaking through the {} troops.\n \n".format(army1.commanderName, army2.name)
                                                        elif(Globals.message == 2):
                                                                roundmessage += "The {} left flank leave themselves open, allowing their opponent to break through.\n \n".format(army2.name)
                                                        elif(Globals.message == 3):
                                                                roundmessage += "{} orders an ill fated charge, allowing the {} army to come down upon them.\n \n".format(army2.commanderName,army1.name)
                                                        elif(Globals.message == 4):
                                                                roundmessage += "The right flank of the {} army buckles, allowing their opponent to pour through.\n \n".format(army2.name)


                                        elif(difference >= 25):
                                                self.battlePhase += 1
                                                if(Globals.battleType == 'Naval'):
                                                        Globals.message = self.numberGen(4)
                                                        if(Globals.message == 1):
                                                                roundmessage += "{} maneuvers their ships to give them an advantage over the {}.\n \n".format(army1.commanderName,army2.name)
                                                        elif(Globals.message == 2):
                                                                roundmessage += "The {} ships push forward, outmaneuvering their opponents\n \n".format(army1.name)
                                                        elif(Globals.message == 3):
                                                                roundmessage += "{} makes a miscalculation, and leaves their ships in the line of the {} approach.\n \n".format(army2.commanderName,army1.name)
                                                        elif(Globals.message == 4):
                                                                roundmessage += "Several {} ships lag behind, allowing their opponent to get the upper hand.\n \n".format(army2.name)
                                                else:
                                                        Globals.message = self.numberGen(4)
                                                        if(Globals.message == 1):
                                                                roundmessage += "{} notices a gap in the {} line, and pushes against it.\n \n".format(army1.commanderName, army2.name)
                                                        elif(Globals.message == 2):
                                                                roundmessage += "The {} army pushes against their opponents, gaining ground.\n \n".format(army1.name)
                                                        elif(Globals.message == 3):
                                                                roundmessage += "{} misjudges an opening, losing ground to their opponent\n \n".format(army2.commanderName)
                                                        elif(Globals.message == 4):
                                                                roundmessage += "{} manages to stop the {} flank breaking but their opponent gains more ground.\n \n".format(army2.commanderName,army2.name)      


                                        else:

                                                if(Globals.battleType == 'Naval'):
                                                        Globals.message = self.numberGen(4)
                                                        if(Globals.message == 1):
                                                                roundmessage += "{} holds their ships back, waiting for their oppenent to make the next move.\n \n".format(army1.commanderName)
                                                        elif(Globals.message == 2):
                                                                roundmessage += "The {} ships hold their position, waiting for the {} ships to approach.\n \n".format(army1.name,army2.name)
                                                        elif(Globals.message == 3):
                                                                roundmessage += "{} orders a charge, but the {} ships are waiting to meet it.\n \n".format(army2.commanderName,army1.name)
                                                        elif(Globals.message == 4):
                                                                roundmessage += "The {} ships take stock, ready to meet their opponent.\n \n".format(army1.name)
                                                else:
                                                        Globals.message = self.numberGen(4)
                                                        if(Globals.message == 1):
                                                                roundmessage += "The {} army hold position, waiting for their opponent to make the next move\n \n".format(army1.name)
                                                        elif(Globals.message == 2):
                                                                roundmessage += "The {} army pushes against their opponents, but the {} army doesn't give an inch.\n \n".format(army1.name,army2.name)
                                                        elif(Globals.message == 3):
                                                                roundmessage += "{} changes the {} formation, to better fend off their opponent\n \n".format(army1.commanderName,army1.name)
                                                        elif(Globals.message == 4):
                                                                roundmessage += "{} notices a gap in the {} line, but {} quickly patches it with more men.\n \n".format(army1.commanderName,army2.name,army2.commanderName)


                                        if(self.battlePhase >= 3):
                                                #Attacker Won
                                                #Logs that the army cannot fight, bringing the battle to an end.
                                                army2.continueFighting = False
                                                roundmessage += "{} defeats {}, bringing an end to the battle.\n \n".format(army1.name,army2.name)
                                                roundmessage += "**Winner: {}**\n \n".format(army1.name)
                                                roundmessage += "Rounds taken: {} \n \n".format(roundCount)


                                elif(roll2 >= roll1):
                                        difference = roll2-roll1

                                        if(difference >= 96):
                                                self.battlePhase -= 10

                                        elif(difference >= 75):
                                                self.battlePhase -= 2
                                                if(Globals.battleType == 'Naval'):
                                                        Globals.message = self.numberGen(4)
                                                        if(Globals.message == 1):
                                                                roundmessage += "A {} ship rams into one of their opponent's ships, flooding the deck with men.\n \n".format(army2.name)
                                                        elif(Globals.message == 2):
                                                                roundmessage += "{} orders a volley upon one of the {} ships, bringing death to their opponent.\n \n".format(army2.commanderName,army1.name)
                                                        elif(Globals.message == 3):
                                                                roundmessage += "{} misjudges where the next attack will come from, leaving several {} ships undefended.\n \n".format(army1.commanderName,army1.name)
                                                        elif(Globals.message == 4):
                                                                roundmessage += "The {} ships come upon an isolated {} ship, and easily kill those aboard.\n \n".format(army2.name,army1.name)
                                                else:
                                                        Globals.message = self.numberGen(4)
                                                        if(Globals.message == 1):
                                                                roundmessage += "{} orders a charge, breaking through the {} troops.\n \n".format(army2.commanderName, army1.name)
                                                        elif(Globals.message == 2):
                                                                roundmessage += "The {} left flank leave themselves open, allowing their opponent to break through.\n \n".format(army1.name)
                                                        elif(Globals.message == 3):
                                                                roundmessage += "{} orders an ill fated charge, allowing the {} army to come down upon them.\n \n".format(army1.commanderName,army2.name)
                                                        elif(Globals.message == 4):
                                                                roundmessage += "The right flank of the {} army buckles, allowing their opponent to pour through.\n \n".format(army1.name)

                                        elif(difference >= 25):
                                                self.battlePhase -= 1
                                                if(Globals.battleType == 'Naval'):
                                                        Globals.message = self.numberGen(4)
                                                        if(Globals.message == 1):
                                                                roundmessage += "{} maneuvers their ships to give them an advantage over the {}.\n \n".format(army2.commanderName,army1.name)
                                                        elif(Globals.message == 2):
                                                                roundmessage += "The {} ships push forward, outmaneuvering their opponents\n \n".format(army2.name)
                                                        elif(Globals.message == 3):
                                                                roundmessage += "{} makes a miscalculation, and leaves their ships in the line of the {} approach.\n \n".format(army1.commanderName,army2.name)
                                                        elif(Globals.message == 4):
                                                                roundmessage += "Several {} ships lag behind, allowing their opponent to get the upper hand.\n \n".format(army1.name)
                                                else:
                                                        Globals.message = self.numberGen(4)
                                                        if(Globals.message == 1):
                                                                roundmessage += "{} notices a gap in the {} line, and pushes against it.\n \n".format(army2.commanderName, army1.name)
                                                        elif(Globals.message == 2):
                                                                roundmessage += "The {} army pushes against their opponents, gaining ground.\n \n".format(army2.name)
                                                        elif(Globals.message == 3):
                                                                roundmessage += "{} misjudges an opening, losing ground to their opponent\n \n".format(army1.commanderName)
                                                        elif(Globals.message == 4):
                                                                roundmessage += "{} manages to stop the {} flank breaking but their opponent gains more ground.\n \n".format(army1.commanderName,army1.name)      


                                        else:
                                                if(Globals.battleType == 'Naval'):
                                                        Globals.message = self.numberGen(4)
                                                        if(Globals.message == 1):
                                                                roundmessage += "{} holds their ships back, waiting for their oppenent to make the next move.\n \n".format(army2.commanderName)
                                                        elif(Globals.message == 2):
                                                                roundmessage += "The {} ships hold their position, waiting for the {} ships to approach.\n \n".format(army2.name,army1.name)
                                                        elif(Globals.message == 3):
                                                                roundmessage += "{} orders a charge, but the {} ships are waiting to meet it.\n \n".format(army1.commanderName,army2.name)
                                                        elif(Globals.message == 4):
                                                                roundmessage += "The {} ships take stock, ready to meet their opponent.\n \n".format(army2.name)
                                                else:
                                                        Globals.message = self.numberGen(4)
                                                        if(Globals.message == 1):
                                                                roundmessage += "The {} army hold position, waiting for their opponent to make the next move\n \n".format(army2.name)
                                                        elif(Globals.message == 2):
                                                                roundmessage += "The {} army pushes against their opponents, but the {} army doesn't give an inch.\n \n".format(army2.name,army1.name)
                                                        elif(Globals.message == 3):
                                                                roundmessage += "{} changes the {} formation, to better fend off their opponent\n \n".format(army2.commanderName,army2.name)
                                                        elif(Globals.message == 4):
                                                                roundmessage += "{} notices a gap in the {} line, but {} quickly patches it with more men.\n \n".format(army2.commanderName,army1.name,army1.commanderName)



                                        if(self.battlePhase <= -3):
                                                 #Defender Won
                                                army1.continueFighting = False
                                                roundmessage += "{} defeats {}, bringing an end to the battle.\n \n \n".format(army2.name,army1.name)
                                                roundmessage += "**Winner: {}**\n \n".format(army2.name)
                                                roundmessage += "Rounds taken: {} \n \n".format(roundCount)
                        

                        else: #Stannis Patch segment (lazy coding I know)
                                self.battlePhase = 999
                                if(roll1>roll2):
                                        army2.morale -= 1
                                        if(army2.morale == 1):
                                                Globals.message = self.numberGen(4)
                                                if(Globals.message == 1):
                                                        roundmessage += "{} orders a charge, breaking through the {} troops.\n \n".format(army1.commanderName, army2.name)
                                                elif(Globals.message == 2):
                                                        roundmessage += "The {} left flank leave themselves open, allowing their opponent to break through.\n \n".format(army2.name)
                                                elif(Globals.message == 3):
                                                        roundmessage += "{} orders an ill fated charge, allowing the {} army to come down upon them.\n \n".format(army2.commanderName,army1.name)
                                                elif(Globals.message == 4):
                                                        roundmessage += "The right flank of the {} army buckles, allowing their opponent to pour through.\n \n".format(army2.name)
                                        elif(army2.morale == 2):
                                                Globals.message = self.numberGen(4)
                                                if(Globals.message == 1):
                                                        roundmessage += "{} notices a gap in the {} line, and pushes against it.\n \n".format(army1.commanderName, army2.name)
                                                elif(Globals.message == 2):
                                                        roundmessage += "The {} army pushes against their opponents, gaining ground.\n \n".format(army1.name)
                                                elif(Globals.message == 3):
                                                        roundmessage += "{} misjudges an opening, losing ground to their opponent\n \n".format(army2.commanderName)
                                                elif(Globals.message == 4):
                                                        roundmessage += "{} manages to stop the {} flank breaking but their opponent gains more ground.\n \n".format(army2.commanderName,army2.name)                                                 
                                        else:
                                                Globals.message = self.numberGen(4)
                                                if(Globals.message == 1):
                                                        roundmessage += "The {} army hold position, waiting for their opponent to make the next move\n \n".format(army1.name)
                                                elif(Globals.message == 2):
                                                        roundmessage += "The {} army pushes against their opponents, but the {} army doesn't give an inch.\n \n".format(army1.name,army2.name)
                                                elif(Globals.message == 3):
                                                        roundmessage += "{} changes the {} formation, to better fend off their opponent\n \n".format(army1.commanderName,army1.name)
                                                elif(Globals.message == 4):
                                                        roundmessage += "{} notices a gap in the {} line, but {} quickly patches it with more men.\n \n".format(army1.commanderName,army2.name,army2.commanderName) 
                                        
                                        if(army2.morale == 0):
                                                #Attacker Won
                                                #Logs that the army cannot fight, bringing the battle to an end.
                                                army2.continueFighting = False
                                                roundmessage += "{} defeats {}, bringing an end to the battle.\n \n".format(army1.name,army2.name)
                                                roundmessage += "**Winner: {}**\n \n".format(army1.name)
                                                roundmessage += "**Winner's Remaining Morale: {}**\n \n".format(army1.morale)
                                                roundmessage += "Rounds taken: {} \n \n".format(roundCount)
                                
                                elif(roll2>roll1):
                                        army1.morale -= 1
                                        if(army1.morale == 1):
                                                Globals.message = self.numberGen(4)
                                                if(Globals.message == 1):
                                                        roundmessage += "{} orders a charge, breaking through the {} troops.\n \n".format(army2.commanderName, army1.name)
                                                elif(Globals.message == 2):
                                                        roundmessage += "The {} left flank leave themselves open, allowing their opponent to break through.\n \n".format(army1.name)
                                                elif(Globals.message == 3):
                                                        roundmessage += "{} orders an ill fated charge, allowing the {} army to come down upon them.\n \n".format(army1.commanderName,army2.name)
                                                elif(Globals.message == 4):
                                                        roundmessage += "The right flank of the {} army buckles, allowing their opponent to pour through.\n \n".format(army1.name)
                                        elif(army1.morale == 2):
                                                Globals.message = self.numberGen(4)
                                                if(Globals.message == 1):
                                                        roundmessage += "{} notices a gap in the {} line, and pushes against it.\n \n".format(army2.commanderName, army1.name)
                                                elif(Globals.message == 2):
                                                        roundmessage += "The {} army pushes against their opponents, gaining ground.\n \n".format(army2.name)
                                                elif(Globals.message == 3):
                                                        roundmessage += "{} misjudges an opening, losing ground to their opponent\n \n".format(army1.commanderName)
                                                elif(Globals.message == 4):
                                                        roundmessage += "{} manages to stop the {} flank breaking but their opponent gains more ground.\n \n".format(army1.commanderName,army1.name)                                                 
                                        else:
                                                Globals.message = self.numberGen(4)
                                                if(Globals.message == 1):
                                                        roundmessage += "The {} army hold position, waiting for their opponent to make the next move\n \n".format(army2.name)
                                                elif(Globals.message == 2):
                                                        roundmessage += "The {} army pushes against their opponents, but the {} army doesn't give an inch.\n \n".format(army2.name,army1.name)
                                                elif(Globals.message == 3):
                                                        roundmessage += "{} changes the {} formation, to better fend off their opponent\n \n".format(army2.commanderName,army2.name)
                                                elif(Globals.message == 4):
                                                        roundmessage += "{} notices a gap in the {} line, but {} quickly patches it with more men.\n \n".format(army2.commanderName,army1.name,army2.commanderName) 
                                        
                                        if(army1.morale == 0):
                                                 #Defender Won
                                                army1.continueFighting = False
                                                roundmessage += "{} defeats {}, bringing an end to the battle.\n \n \n".format(army2.name,army1.name)
                                                roundmessage += "**Winner: {}**\n \n".format(army2.name)
                                                roundmessage += "**Winner's Remaining Morale: {}**\n \n".format(army2.morale)
                                                roundmessage += "Rounds taken: {} \n \n".format(roundCount)                               
                                 
            
                #Godamn python globals. Logs the phase to print out and calculate casualties. Each pass through will add casualties onto the previous, making the total.
                global attackcas
                global defendcas
                if(self.battlePhase == 999):
                        roundmessage += "**{}** Morale: {} \n \n".format(army1.name,army1.morale)
                        roundmessage += "**{}** Morale: {} \n \n".format(army2.name,army2.morale)
                        roundmessage += "--- \n \n"                        
                elif(self.battlePhase >= 3 and self.battlePhase != 999):
                        phase = 'Defender Routing'
                        roundmessage += "##**Phase - Defender Routing** \n \n".format(phase)
                        roundmessage += "--- \n \n"
                        attackcas += 0
                        if(Globals.battleType == "Naval"):
                                defendcas += 8
                        else:
                                defendcas += 25
                elif(self.battlePhase == 2):
                        phase = 'Defender Breaking'
                        roundmessage += "##**Phase - {}** \n \n".format(phase)
                        roundmessage += "--- \n \n"
                        attackcas += 0.25
                        defendcas += 4
                elif(self.battlePhase == 1):
                        phase = 'Defender Losing'
                        roundmessage += "##**Phase - {}** \n \n".format(phase)
                        roundmessage += "--- \n \n"
                        attackcas += 0.5
                        defendcas += 2
                elif(self.battlePhase == 0):
                        phase = 'Even'
                        roundmessage += "##**Phase - {}** \n \n".format(phase)
                        roundmessage += "--- \n \n"
                        attackcas += 1
                        defendcas += 1
                elif(self.battlePhase == -1):
                        phase = 'Attacker Losing'
                        roundmessage += "##**Phase - {}** \n \n".format(phase)
                        roundmessage += "--- \n \n"
                        attackcas += 2
                        defendcas += 0.5
                elif(self.battlePhase == -2):
                        phase = 'Attacker Breaking'
                        roundmessage += "##**Phase - {}** \n \n".format(phase)
                        roundmessage += "--- \n \n"
                        attackcas += 4
                        defendcas += 0.25
                elif(self.battlePhase <= -3):
                        phase = 'Attacker Routing'
                        roundmessage += "##**Phase - Attacker Routing** \n \n".format(phase)
                        roundmessage += "--- \n \n"
                        defendcas += 0
                        if(Globals.battleType == "Naval"):
                                attackcas += 8
                                print("Navy")
                        else:
                                attackcas += 25

                #never happened in the sims but just in case casualties reach 100% or higher
                            
                if(attackcas >= 100):
                        attackcas = 100
                        army1.continueFighting = False
                        roundmessage += "{} eliminates all the {} troops, completely destroying the army.\n \n \n".format(army2.name,army1.name)
                        roundmessage += "**Winner: {}**\n \n".format(army2.name)
                        roundmessage += "Rounds taken: {} \n \n".format(roundCount)
                if(defendcas >= 100):
                        defendcas = 100
                        army2.continueFighting = False
                        roundmessage += "{} eliminates all the {} troops, completely destroying the army.\n \n \n".format(army1.name,army2.name)
                        roundmessage += "**Winner: {}**\n \n".format(army1.name)
                        roundmessage += "Rounds taken: {} \n \n".format(roundCount)
                        
                return roundmessage
        
        def numberGen(self,maxCount):
                newMessage = random.randint(1,maxCount)
                while (newMessage == Globals.message):
                        newMessage = random.randint(1,maxCount)
                return newMessage
                        

        def run(self,battleInfo):
                roundCount = 0
                global attackcas
                global defendcas
                attackcas = 0
                defendcas = 0
                autosurrender = 0
                
                if(battleInfo.group(2)):
                        group2 = battleInfo.group(2)
                else:
                        group2 = 0
                if(battleInfo.group(5)):
                        group5 = battleInfo.group(5)
                else:
                        group5 = 0
                if(battleInfo.group(7)):
                        group7 = battleInfo.group(7)
                else:
                        group7 = 0
                if(battleInfo.group(9)):
                        group10 = battleInfo.group(10)
                else:
                        group10 = 0
                
                
                army1 = Army.Army(battleInfo.group(1), int(group2), battleInfo.group(3), int(battleInfo.group(4)), int(group5))
                army2 = Army.Army(battleInfo.group(6), int(group7), battleInfo.group(8), int(battleInfo.group(9)), int(group10))


                if(army1.power == 0):
                        autosurrender = 1
                elif(army2.power == 0):
                        autosurrender = 2
                elif(army1.power > army2.power and Globals.battleType == "Naval"):
                        difference = (army1.power / army2.power) - 1
                        difference *= 100
                        print(difference)
                        if(difference <= 15):
                                army1.bonus +=1
                        elif(difference <= 35):
                                army1.bonus += 2
                        elif(difference <= 50):
                                army1.bonus += 3
                        elif(difference <= 65):
                                army1.bonus += 4
                        elif(difference <= 75):
                                army1.bonus += 5
                        elif(difference <= 85):
                                army1.bonus += 6
                        elif(difference <= 100):
                                army1.bonus += 7
                        elif(difference <= 130):
                                army1.bonus += 8
                        elif(difference <= 160):
                                army1.bonus += 9
                        elif(difference <= 200):
                                army1.bonus += 10
                        elif(difference <= 250):
                                army1.bonus += 11
                        elif(difference <= 300):
                                army1.bonus += 12
                        elif(difference <= 330):
                                army1.bonus += 13
                        elif(difference <= 370):
                                army1.bonus += 14
                        elif(difference <= 400):
                                army1.bonus += 15
                        elif(difference <= 450):
                                army1.bonus += 16
                        elif(difference <= 500):
                                army1.bonus += 17
                        elif(difference <= 600):
                                army1.bonus += 18
                        elif(difference <= 750):
                                army1.bonus += 19
                        elif(difference <= 900):
                                army1.bonus += 20
                        elif(difference <= 1399):
                                army1.bonus += 21
                        else:
                                autosurrender = 2

                elif(army2.power > army1.power and Globals.battleType == "Naval"):
                        difference = (army2.power / army1.power) - 1
                        difference *= 100
                        print(difference)
                        if(difference <= 15):
                                army2.bonus +=1
                        elif(difference <= 35):
                                army2.bonus += 2
                        elif(difference <= 50):
                                army2.bonus += 3
                        elif(difference <= 65):
                                army2.bonus += 4
                        elif(difference <= 75):
                                army2.bonus += 5
                        elif(difference <= 85):
                                army2.bonus += 6
                        elif(difference <= 100):
                                army2.bonus += 7
                        elif(difference <= 130):
                                army2.bonus += 8
                        elif(difference <= 160):
                                army2.bonus += 9
                        elif(difference <= 200):
                                army2.bonus += 10
                        elif(difference <= 250):
                                army2.bonus += 11
                        elif(difference <= 300):
                                army2.bonus += 12
                        elif(difference <= 330):
                                army2.bonus += 13
                        elif(difference <= 370):
                                army2.bonus += 14
                        elif(difference <= 400):
                                army2.bonus += 15
                        elif(difference <= 450):
                                army2.bonus += 16
                        elif(difference <= 500):
                                army2.bonus += 17
                        elif(difference <= 600):
                                army2.bonus += 18
                        elif(difference <= 750):
                                army2.bonus += 19
                        elif(difference <= 900):
                                army2.bonus += 20
                        elif(difference <= 1399):
                                army2.bonus += 21
                        else:
                                autosurrender = 1
                elif(army1.power > army2.power and Globals.battleType != "Naval"):
                        difference = (army1.power / army2.power) - 1
                        difference *= 100
                        print(difference)
                        if(difference <= 25):
                                army1.bonus += 2
                        elif(difference <= 50):
                                army1.bonus += 6
                        elif(difference <= 100):
                                army1.bonus += 10
                        elif(difference <= 150):
                                army1.bonus += 14
                        elif(difference <= 200):
                                army1.bonus += 18
                        elif(difference <= 300):
                                army1.bonus += 22
                        elif(difference <= 400):
                                army1.bonus += 26
                        elif(difference <= 500):
                                army1.bonus += 30
                        elif(difference <= 600):
                                army1.bonus += 34
                        elif(difference <= 700):
                                army1.bonus += 38
                        elif(difference <= 800):
                                army1.bonus += 42
                        elif(difference <= 900):
                                army1.bonus += 46
                        elif(difference <= 1000):
                                army1.bonus += 50
                        else:
                                autosurrender = 2
                elif(army2.power > army1.power and Globals.battleType != "Naval"):
                        difference = (army2.power / army1.power) - 1
                        difference *= 100
                        print(difference)
                        if(difference <= 25):
                                army2.bonus += 2
                        elif(difference <= 50):
                                army2.bonus += 6
                        elif(difference <= 100):
                                army2.bonus += 10
                        elif(difference <= 150):
                                army2.bonus += 14
                        elif(difference <= 200):
                                army2.bonus += 18
                        elif(difference <= 300):
                                army2.bonus += 22
                        elif(difference <= 400):
                                army2.bonus += 26
                        elif(difference <= 500):
                                army2.bonus += 30
                        elif(difference <= 600):
                                army2.bonus += 34
                        elif(difference <= 700):
                                army2.bonus += 38
                        elif(difference <= 800):
                                army2.bonus += 42
                        elif(difference <= 900):
                                army2.bonus += 46
                        elif(difference <= 1000):
                                army2.bonus += 50
                        else:
                                autosurrender = 1

                
                if(Globals.battleType == "Naval"):
                        battlemessage = "#Naval Battle Between {} and {} \n \n".format(army1.name,army2.name)
                elif(Globals.battleType == "Ambush"):
                        battlemessage = "#Ambush Battle Between {} and {} \n \n".format(army1.name,army2.name)
                elif(Globals.battleType == "Assault"):
                        battlemessage = "#{} Assault On {} \n \n".format(army1.name,army2.name)
                        attackcas += 5
                else:
                        battlemessage = "#Land Battle Between {} and {} \n \n".format(army1.name,army2.name)
                battlemessage += "*I am a bot managed and run by the r/CenturyOfBlood modteam. Please upvote my comments so I can respond quicker and run faster.* \n \n"
                battlemessage += "\n \n"
                battlemessage += "Credits: skulkdan, dino_king88 \n \n"
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
                                battlemessage += "{} Casualties = {}% \n \n{} Casualties = {}%\n \n".format(army1.name,attackcas,army2.name,defendcas)
                                battlemessage += "--- \n \n"
                        else:
                                if(army2.morale == 0):
                                        if(army1.morale == 4):
                                                for x in range(2):
                                                        attackcas += self.numberGen(3)
                                                attackcas += 1
                                                for x in range(14):
                                                        defendcas += self.numberGen(3)
                                                defendcas += 9
                                        elif(army1.morale == 3):
                                                for x in range(4):
                                                        attackcas += self.numberGen(3)
                                                attackcas += 3
                                                for x in range(11):
                                                        defendcas += self.numberGen(3)
                                                defendcas += 7
                                        elif(army1.morale == 2):
                                                for x in range(5):
                                                        attackcas += self.numberGen(3)
                                                attackcas += 4
                                                for x in range(9):
                                                        defendcas += self.numberGen(3)
                                                defendcas += 6 
                                        elif(army1.morale == 1):
                                                for x in range(6):
                                                        attackcas += self.numberGen(3)
                                                attackcas += 5
                                                for x in range(7):
                                                        defendcas += self.numberGen(3)
                                                defendcas += 5
                                                
                                elif(army1.morale == 0):
                                        if(army2.morale == 4):
                                                for x in range(2):
                                                        defendcas += self.numberGen(3)
                                                defendcas += 1
                                                for x in range(14):
                                                        attackcas += self.numberGen(3)
                                                attackcas += 9
                                        elif(army2.morale == 3):
                                                for x in range(4):
                                                        defendcas += self.numberGen(3)
                                                defendcas += 3
                                                for x in range(11):
                                                        attackcas += self.numberGen(3)
                                                attackcas += 7
                                        elif(army2.morale == 2):
                                                for x in range(5):
                                                        defendcas += self.numberGen(3)
                                                defendcas += 4
                                                for x in range(9):
                                                        attackcas += self.numberGen(3)
                                                attackcas += 6 
                                        elif(army2.morale == 1):
                                                for x in range(6):
                                                        defendcas += self.numberGen(3)
                                                defendcas += 5
                                                for x in range(7):
                                                        attackcas += self.numberGen(3)
                                                attackcas += 5                                 
                                                
                                
                                
                                if (army1.commanderBonus >= 9):
                                        attcas = attackcas*0.8
                                        if (army2.commanderBonus >= 9):
                                                defcas = defendcas*0.8
                                                battlemessage += "{} Casualties = {}% ({}*0.8) \n \n{} Casualties = {}% ({}*0.8)\n \n".format(army1.name,attcas,attackcas,army2.name,defcas,defendcas)
                                                battlemessage += "--- \n \n"
                                        elif (army2.commanderBonus == 6):
                                                defcas = defendcas*0.9
                                                battlemessage += "{} Casualties = {}% ({}*0.8) \n \n{} Casualties = {}% ({}*0.9)\n \n".format(army1.name,attcas,attackcas,army2.name,defcas,defendcas)
                                                battlemessage += "--- \n \n"
                                        elif (army2.commanderBonus == 3):
                                                defcas = defendcas*0.95
                                                battlemessage += "{} Casualties = {}% ({}*0.8) \n \n{} Casualties = {}% ({}*0.95)\n \n".format(army1.name,attcas,attackcas,army2.name,defcas,defendcas)
                                                battlemessage += "--- \n \n"
                                        else:
                                                battlemessage += "{} Casualties = {}% ({}*0.8) \n \n{} Casualties = {}%\n \n".format(army1.name,attcas,attackcas,army2.name,defendcas)
                                                battlemessage += "--- \n \n"
                                                
                                elif (army1.commanderBonus == 6):
                                        attcas = attackcas*0.9
                                        if (army2.commanderBonus >= 9):
                                                defcas = defendcas*0.8
                                                battlemessage += "{} Casualties = {}% ({}*0.9) \n \n{} Casualties = {}% ({}*0.8)\n \n".format(army1.name,attcas,attackcas,army2.name,defcas,defendcas)
                                                battlemessage += "--- \n \n"
                                        elif (army2.commanderBonus == 6):
                                                defcas = defendcas*0.9
                                                battlemessage += "{} Casualties = {}% ({}*0.9) \n \n{} Casualties = {}% ({}*0.9)\n \n".format(army1.name,attcas,attackcas,army2.name,defcas,defendcas)
                                                battlemessage += "--- \n \n"
                                        elif (army2.commanderBonus == 3):
                                                defcas = defendcas*0.95
                                                battlemessage += "{} Casualties = {}% ({}*0.9) \n \n{} Casualties = {}% ({}*0.95)\n \n".format(army1.name,attcas,attackcas,army2.name,defcas,defendcas)
                                                battlemessage += "--- \n \n"
                                        else:
                                                battlemessage += "{} Casualties = {}% ({}*0.9) \n \n{} Casualties = {}% \n \n".format(army1.name,attcas,attackcas,army2.name,defendcas)
                                                battlemessage += "--- \n \n"
                                                
                                elif (army1.commanderBonus == 3):
                                        attcas = attackcas*0.95
                                        if (army2.commanderBonus >= 9):
                                                defcas = defendcas*0.8
                                                battlemessage += "{} Casualties = {}% ({}*0.95) \n \n{} Casualties = {}% ({}*0.8)\n \n".format(army1.name,attcas,attackcas,army2.name,defcas,defendcas)
                                                battlemessage += "--- \n \n"
                                        elif (army2.commanderBonus == 6):
                                                defcas = defendcas*0.9
                                                battlemessage += "{} Casualties = {}% ({}*0.95) \n \n{} Casualties = {}% ({}*0.9)\n \n".format(army1.name,attcas,attackcas,army2.name,defcas,defendcas)
                                                battlemessage += "--- \n \n"
                                        elif (army2.commanderBonus == 3):
                                                defcas = defendcas*0.95
                                                battlemessage += "{} Casualties = {}% ({}*0.95) \n \n{} Casualties = {}% ({}*0.95)\n \n".format(army1.name,attcas,attackcas,army2.name,defcas,defendcas)
                                                battlemessage += "--- \n \n"
                                        else:
                                                battlemessage += "{} Casualties = {}% ({}*0.95) \n \n{} Casualties = {}% \n \n".format(army1.name,attcas,attackcas,army2.name,defendcas)
                                                battlemessage += "--- \n \n"
                                                
                                else:
                                        if (army2.commanderBonus >= 9):
                                                defcas = defendcas*0.8
                                                battlemessage += "{} Casualties = {}% \n \n{} Casualties = {}% ({}*0.8)\n \n".format(army1.name,attackcas,army2.name,defcas,defendcas)
                                                battlemessage += "--- \n \n"
                                        elif (army2.commanderBonus == 6):
                                                defcas = defendcas*0.9
                                                battlemessage += "{} Casualties = {}% \n \n{} Casualties = {}% ({}*0.9)\n \n".format(army1.name,attackcas,army2.name,defcas,defendcas)
                                                battlemessage += "--- \n \n"
                                        elif (army2.commanderBonus == 3):
                                                defcas = defendcas*0.95
                                                battlemessage += "{} Casualties = {}% \n \n{} Casualties = {}% ({}*0.95)\n \n".format(army1.name,attackcas,army2.name,defcas,defendcas)
                                                battlemessage += "--- \n \n"
                                        else:
                                                battlemessage += "{} Casualties = {}% \n \n{} Casualties = {}% \n \n".format(army1.name,attackcas,army2.name,defendcas)
                                                battlemessage += "--- \n \n"
       
                battlemessage += "**REMINDER** that casualties of the larger army is affected by relative size, this must be calculated manually \n \n"
                battlemessage += "--- \n \n" 
                
                return battlemessage
                print ("Finished battle")
                self.reset_battle_phase()
                
        def reset_battle_phase(self):
                self.battlePhase = 0
