import re
import random
import Jouster
import Globals
class Joust:
        
        joustPhase = 0
        phaseDifference = 0
        Globals.message = 1
        
        
        def run_round(self,jouster1,jouster2,roundCount):
                
                roundmessage = "##**Tilt {}** \n \n".format(roundCount+1)
                roll1 = jouster1.attack_roll()
                roll2 = jouster2.attack_roll()
                unmodded1 = roll1-jouster1.bonus
                unmodded2 = roll2-jouster2.bonus
                roundmessage += "**{}** Roll: {} ({}{:+})\n \n".format(jouster1.name,roll1,unmodded1,jouster1.bonus)
                roundmessage += "--- \n \n"
                roundmessage += "**{}** Roll: {} ({}{:+})\n \n".format(jouster2.name,roll2,unmodded2,jouster2.bonus)
                roundmessage += "--- \n \n"

                if(roll1 > roll2):
                        difference = roll1-roll2
                        unmoddedDiff = unmodded1-unmodded2

                        
                        if(difference >= 18):
                                jouster2.continueFighting = False
                                jouster2.injury_roll()
                                roundmessage += "{} manages to unhorse their opponent, injuring them and bringing an end to the joust.\n \n".format(jouster1.name)
                                
                        elif(difference >= 15):
                                jouster2.continueFighting = False
                                roundmessage += "{} manages to unhorse their opponent, bringing an end to the joust.\n \n".format(jouster1.name)
                                
                        elif(difference >= 11):
                                jouster1.brokenLances += 1
                                jouster1.bonus += 3
                                if (jouster1.brokenLances >= 3):
                                        jouster2.continueFighting = False
                                        roundmessage += "{} breaks their final lance against {}, bringing an end to the joust.\n\n".format(jouster1.name,jouster2.name)
                                elif(jouster1.brokenLances >= 2):
                                        roundmessage += "{} breaks their second lance against {} \n\n".format(jouster1.name,jouster2.name)
                                else:
                                        roundmessage += "{} breaks their first lance against {} \n\n".format(jouster1.name,jouster2.name)

                        elif(difference >= 7):
                                jouster1.bonus += 2
                                roundmessage += "{} lands a strong hit on their opponent.\n \n".format(jouster1.name)
                                
                        elif(difference >= 3):
                                jouster1.bonus += 1
                                roundmessage += "{} lands a hit on their opponent.\n \n".format(jouster1.name)
                                                
                        else:
                                roundmessage += "Neither side land a hit on their opponent.\n \n"

                else:
                        difference = roll2-roll1
                        unmoddedDiff = unmodded2-unmodded1
                      
                       
                        if(difference >= 18):
                                jouster1.continueFighting = False
                                jouster1.injury_roll()
                                roundmessage += "{} manages to unhorse their opponent, injuring them and bringing an end to the joust.\n \n".format(jouster2.name)
                                
                        elif(difference >= 15):
                                jouster1.continueFighting = False
                                roundmessage += "{} manages to unhorse their opponent, bringing an end to the joust.\n \n".format(jouster2.name)
                                  
                        elif(difference >= 11):
                                jouster2.brokenLances += 1
                                jouster2.bonus += 3
                                if (jouster2.brokenLances >= 3):
                                        jouster1.continueFighting = False
                                        roundmessage += "{} breaks their final lance against {}, bringing an end to the joust.\n\n".format(jouster2.name,jouster1.name)
                                elif(jouster2.brokenLances >= 2):
                                        roundmessage += "{} breaks their second lance against {} \n\n".format(jouster2.name,jouster1.name)
                                else:
                                        roundmessage += "{} breaks their first lance against {} \n\n".format(jouster2.name,jouster1.name)
                      
                        elif(difference >= 7):
                                jouster2.bonus += 2
                                roundmessage += "{} lands a strong hit on their opponent.\n \n".format(jouster2.name)
                                
                        elif(difference >= 3):
                                jouster2.bonus += 1
                                roundmessage += "{} lands a hit on their opponent.\n \n".format(jouster2.name)
                                                
                        else:
                                roundmessage += "Neither side land a hit on their opponent.\n \n"
                                                                                          
                                                                                                            

                                
                roundmessage += "--- \n \n"
                roundmessage += "The number of broken lances currently stand as the following\n \n"
                roundmessage += "**{}** Broken Lances: {} \n \n".format(jouster1.name,jouster1.brokenLances)
                roundmessage += "**{}** Broken Lances: {} \n \n".format(jouster2.name,jouster2.brokenLances)
                roundmessage += "--- \n \n"
                return roundmessage


        def numberGen(self,maxCount):
                newMessage = random.randint(1,maxCount)
                message2 = Globals.message
                while (newMessage == message2):
                        newMessage = random.randint(1,maxCount)
                return newMessage
                        
        
        def run(self,joustInfo):
                roundCount = 0
                
                if(joustInfo.group(2)):
                        group2 = joustInfo.group(2)
                else:
                        group2 = 0
                if(joustInfo.group(4)):
                        group4 = joustInfo.group(4)
                else:
                        group4 = 0
                
                jouster1 = Jouster.Jouster(joustInfo.group(1), int(group2))
                jouster2 = Jouster.Jouster(joustInfo.group(3), int(group4))
                battlemessage = "#Joust Between {} and {} \n \n".format(jouster1.name,jouster2.name)
                battlemessage += "--- \n \n"
                notbattlemessage = ""
                roundOver = True
                while(jouster1.continueFighting and jouster2.continueFighting and roundOver):
                        if(Globals.resultsMode):
                                notbattlemessage += self.run_round(jouster1,jouster2,roundCount)
                                roundCount += 1
                                if(roundCount == 7):
                                        if(Globals.battleType != "Continued"):
                                                if(jouster1.continueFighting and jouster2.continueFighting):
                                                        roundOver = False
                        else:
                                battlemessage += self.run_round(jouster1,jouster2,roundCount)
                                roundCount += 1
                                if(roundCount == 7):
                                        if(Globals.battleType != "Continued"):
                                                if(jouster1.continueFighting and jouster2.continueFighting):
                                                        roundOver = False
                        
                if(not roundOver):
                        if(jouster1.brokenLances > jouster2.brokenLances):
                                jouster2.continueFighting = False
                        elif(jouster2.brokenLances > jouster1.brokenLances):
                                jouster1.continueFighting = False
                        else:
                                battlemessage += "**After seven tilts, the Joust ends in a draw.**\n \n"
                                battlemessage += "They broke an equal number of lances.\n \n"
                
                if(jouster1.continueFighting):
                        battlemessage += "**Winner: {}**\n \n".format(jouster1.name)
                else:
                        battlemessage += "**Winner: {}**\n \n".format(jouster2.name)
                battlemessage += "Tilts taken: {} \n \n".format(roundCount)

                if(jouster1.alive == False):
                        battlemessage += "{} is killed in the joust.\n\n".format(jouster1.name)
                elif(jouster2.alive == False):
                        battlemessage += "{} is killed in the joust.\n\n".format(jouster2.name)
                else:
                        
                        if(jouster1.injuryRoll != 0):
                                if(jouster1.permanentInjuries != "None"):
                                        if(jouster1.permanentInjuries == "Hand"):
                                                battlemessage += "{} suffers a permanent injury and loses a hand/arm in the joust.\n\n".format(jouster1.name)
                                        elif(jouster1.permanentInjuries == "Foot"):
                                                battlemessage += "{} suffers a permanent injury and loses a leg/foot in the joust.\n\n".format(jouster1.name)
                                        elif(jouster1.permanentInjuries == "Blinded"):
                                                battlemessage += "{} suffers a permanent injury and is permanently blinded in one eye from the joust.\n\n".format(jouster1.name)
                                        elif(jouster1.permanentInjuries == "Deafened"):
                                                battlemessage += "{} suffers a permanent injury and is partially/fully loses their hearing from the joust.\n\n".format(jouster1.name)
                                        elif(jouster1.permanentInjuries == "Internal"):
                                                battlemessage += "{} suffers a permanent injury and suffers internal organ damage from the joust.\n\n".format(jouster1.name)
                                        elif(jouster1.permanentInjuries == "Scar"):
                                                battlemessage += "{} suffers a permanent injury and gets intensely scarred from the joust.\n\n".format(jouster1.name)
                                        elif(jouster1.permanentInjuries == "Genital"):
                                                battlemessage += "{} suffers a permanent injury and suffers a genital wound from the joust.\n\n".format(jouster1.name)
                                else:
                                        battlemessage += "{} emerges from the joust with {} major, {} moderate and {} minor injuries.\n\n".format(jouster1.name,jouster1.majorInjuries,jouster1.moderateInjuries,jouster1.minorInjuries)

                        elif(jouster2.injuryRoll != 0):
                                if(jouster2.permanentInjuries != "None"):
                                        if(jouster2.permanentInjuries == "Hand"):
                                                battlemessage += "{} suffers a permanent injury and loses a hand/arm in the joust.\n\n".format(jouster2.name)
                                        elif(jouster2.permanentInjuries == "Foot"):
                                                battlemessage += "{} suffers a permanent injury and loses a leg/foot in the joust.\n\n".format(jouster2.name)
                                        elif(jouster2.permanentInjuries == "Blinded"):
                                                battlemessage += "{} suffers a permanent injury and is permanently blinded in one eye from the joust.\n\n".format(jouster2.name)
                                        elif(jouster2.permanentInjuries == "Deafened"):
                                                battlemessage += "{} suffers a permanent injury and is partially/fully loses their hearing from the joust.\n\n".format(jouster2.name)
                                        elif(jouster2.permanentInjuries == "Internal"):
                                                battlemessage += "{} suffers a permanent injury and suffers internal organ damage from the joust.\n\n".format(jouster2.name)
                                        elif(jouster2.permanentInjuries == "Scar"):
                                                battlemessage += "{} suffers a permanent injury and gets intensely scarred from the joust.\n\n".format(jouster2.name)
                                        elif(jouster2.permanentInjuries == "Genital"):
                                                battlemessage += "{} suffers a permanent injury and suffers a genital wound from the joust.\n\n".format(jouster2.name)
                                else:
                                        battlemessage += "{} emerges from the joust with {} major, {} moderate and {} minor injuries.\n\n".format(jouster2.name,jouster2.majorInjuries,jouster2.moderateInjuries,jouster2.minorInjuries)
                        


                        
                ##reset_duel_phase()
                self.joustPhase = 0
                return battlemessage
        
        def reset_joust_phase(self):
                self.joustPhase = 0