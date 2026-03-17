import prawcore
import praw
import os
import re
import Battle
import Duel
import MultiDuel
import Joust
import time
import Army
import random
import Globals
import TP
from movementcalculator import land_movement
from movementcalculator import naval_movement
import traceback


reddit = praw.Reddit(user_agent=os.environ['AGENT_NAME'] ,
                     client_id=os.environ['PRAW_ID'] ,
                     client_secret=os.environ['PRAW_SECRET'] ,
                     password=os.environ['REDDIT_PW'] ,
                     username=os.environ['REDDIT_USER']
)

print(reddit.user.me())
print("---\n")


subreddit = reddit.subreddit('AfterTheDance+AfterTheDanceMods+awoiafpowers+NinePennyKings+NinePennyKingsMods+FireAndBlood+FireAndBloodMods+CrownedStag+MandarinB2')
for comment in subreddit.stream.comments(skip_existing=True):
    try:
        comment.refresh()

        if((re.search('/u/botofmanyfaces',comment.body,re.IGNORECASE) or re.search('u/botofmanyfaces',comment.body,re.IGNORECASE))): #Make sure we're tagged in order to run. Non caps-sensitive.

            if(re.search("Roll",comment.body,re.IGNORECASE)):
              try:
                  battleInfo = re.findall("(\d+)([d])(\d+)([\+\-]?\d*)(.*)",comment.body)
                  if(battleInfo):
                      roundmessage= ""
                      for j in battleInfo:
                          bonus = 0
                          noDice = int(j[0])
                          sizeDice = int(j[2])
                          if (j[3]):
                              bonus = int(j[3])
                          else:
                              bonus = 0
                          name = j[4]
                          number = 0
                          printedBonus = 0
                          numberBonus = 0
                          runningBonus = "("

                          while(noDice != number):
                              random.seed()
                              printed = random.randint(1,sizeDice)
                              printedBonus += printed
                              print("Rolling", name, "\n")
                              if (noDice - number == 1):
                                  runningBonus += "{})".format(printed)
                              else:
                                  runningBonus += "{} + ".format(printed)
                              number += 1


                          printedBonus += bonus

                          if (bonus > 0):
                              roundmessage += "{}d{}+{} {}: **{}**".format(noDice,sizeDice,bonus,name,printedBonus)
                              roundmessage += "\n\n {} + {} \n\n *** \n\n".format(runningBonus,bonus)
                          elif (bonus < 0):
                              roundmessage += "{}d{}{} {}: **{}**".format(noDice,sizeDice,bonus,name,printedBonus)
                              roundmessage += "\n\n {} {} \n\n *** \n\n".format(runningBonus,bonus)
                          elif (noDice > 1):
                              roundmessage += "{}d{} {}: **{}**".format(noDice,sizeDice,name,printedBonus)
                              roundmessage += "\n\n {} \n\n *** \n\n".format(runningBonus)
                          else:
                              roundmessage += "{}d{} {}: **{}**".format(noDice,sizeDice,name,printedBonus)
                              roundmessage += "\n\n *** \n\n"

                  comment.reply(roundmessage)
                  print("---\n")


              except:
                print ("Improperly formatted roll\n---\n")
                comment.reply("Improperly formatted Roll.")
              time.sleep(60)


            elif(re.search("Naval Battle",comment.body,re.IGNORECASE)):
                Globals.battleType = "Naval"
                battleInfo = re.match("(.*) ([\-]?\d+) ([\+\-]?\d*)\n+(.*) (\d+) ([\+\-]?\d*)\n+(.*) ([\-]?\d+) ([\+\-]?\d*)\n+(.*) (\d+) ([\+\-]?\d*)",comment.body)
                if(battleInfo):
                    print ("Running Naval battle\n")
                    battle = Battle.Battle()
                    print ("Quick Mode\n")
                    comment.reply(battle.run(battleInfo))

                    print("---\n")
                else:
                    print ("Improperly formatted battle\n---\n")
                    comment.reply("Improperly formatted battle info.")
                time.sleep(60)

            elif(re.search("Land Battle",comment.body,re.IGNORECASE)):
                Globals.battleType = "Land"
                battleInfo = re.match("(.*) ([\-]?\d+) ([\+\-]?\d*)\n+(.*) (\d+) ([\+\-]?\d*)\n+(.*) ([\-]?\d+) ([\+\-]?\d*)\n+(.*) (\d+) ([\+\-]?\d*)",comment.body)
                if(battleInfo):
                    print ("Running Land battle\n")
                    battle = Battle.Battle()
                    print ("Quick Mode\n")
                    comment.reply(battle.run(battleInfo))#Post all at once
                    print("---\n")
                else:
                    print ("Improperly formatted battle\n---\n")
                    comment.reply("Improperly formatted battle info.")
                time.sleep(60)


            elif(re.search("Joust",comment.body,re.IGNORECASE)):
                Globals.battleType = "Joust"
                joustInfo = re.match("(.*) ([\+\-]?\d*)\n+(.*) ([\+\-]?\d*)",comment.body)
                if(joustInfo):
                    print ("Running Joust\n")
                    joust = Joust.Joust()

                    Globals.resultsMode = False
                    print ("Quick Mode\n")
                    comment.reply(joust.run(joustInfo))

                    print("--- \n")
                else:
                    print ("Improperly formatted joust\n---\n")
                    comment.reply("Improperly formatted joust info.")
                time.sleep(60)

            elif(re.search("Multi-Person Duel",comment.body,re.IGNORECASE)):
                is_blunted = bool(re.search("Blunted Multi-Person Duel", comment.body, re.IGNORECASE))

                multiduel = MultiDuel.MultiDuel()

                if is_blunted:
                    multiduel.LIVE_STEEL = False
                    print ("Running Blunted Multi-Person Duel\n")
                else:
                    multiduel.LIVE_STEEL = True
                    print ("Running Live Multi-Person Duel\n")

                Globals.resultsMode = False
                print ("Quick Mode\n")
                result = multiduel.run(comment.body)

                comment.reply(result)

                print("--- \n")
                time.sleep(60)

            elif(re.search("Blunted Duel",comment.body,re.IGNORECASE) or re.search("Duel",comment.body,re.IGNORECASE)):
                is_blunted = bool(re.search("Blunted Duel", comment.body, re.IGNORECASE))

                duelInfo = re.match(
                    r"(.*) ([\-]?\d+) ([\+\-]?\d*) ([\+\-]?\d*) ([\+\-]?\d*)(?: ([\+]?\d+))?\n+"
                    r"(.*) ([\-]?\d+) ([\+\-]?\d*) ([\+\-]?\d*) ([\+\-]?\d*)(?: ([\+]?\d+))?",
                    comment.body
                )

                if(duelInfo):
                    duel = Duel.Duel()

                    if is_blunted:
                        duel.LIVE_STEEL = False
                        print ("Running Blunted Duel\n")
                    else:
                        duel.LIVE_STEEL = True
                        print ("Running Live Duel\n")

                    Globals.resultsMode = False
                    print ("Quick Mode\n")
                    result = duel.run(duelInfo)

                    comment.reply(result)

                    print("--- \n")
                else:
                    print ("\nImproperly formatted duel\n--- \n")
                    comment.reply("Improperly formatted duel info.")

                time.sleep(60)


            elif(re.search("TP", comment.body, re.IGNORECASE)):
                try:
                    handler = TP.TPHandler(comment)
                    handler.handle()
                    print("Handled TP\n---\n")
                except Exception as e:
                    print("Error in TP handler:", e)
                    comment.reply("An error occurred while processing your TP request. Please double-check your format.")
                time.sleep(60)

            elif re.search("Land Movement", comment.body, re.IGNORECASE):
                try:
                    reply_text = land_movement.parse_land_movement_comment(comment)
                    print("Handled Land Movement\n---\n")
                    comment.reply(reply_text)
                except ValueError as ve:
                        comment.reply(str(ve))
                except Exception as e:
                    print(f"[ERROR] Land Movement handler: {e}")
                    traceback.print_exc()
                    comment.reply(f"Unexpected error occurred:\n\n{e}\n\nPlease verify your format.")
                time.sleep(60)

            elif re.search("Naval Movement", comment.body, re.IGNORECASE):
                try:
                    reply_text = naval_movement.parse_naval_movement_comment(comment)
                    if reply_text:
                        print("Handled Naval Movement\n---\n")
                        comment.reply(reply_text)
                except ValueError as ve:
                        comment.reply(str(ve))
                except Exception as e:
                    print(f"[ERROR] Naval Movement handler: {e}")
                    traceback.print_exc()
                    comment.reply(f"Unexpected error occurred:\n\n{e}\n\nPlease verify your format.")
                time.sleep(60)


            else:
                comment.reply("Improperly formatted info. Please state which function you wish to use.")
                print("Improperly formatted info\n---\n")

    except praw.exceptions.ClientException as excep:
    print('SKIPPING due to ClientException:')
    print(excep)
    continue
    except prawcore.exceptions.ServerError as excep:
    print('SKIPPING due to Reddit ServerError (500):')
    print(excep)
    time.sleep(30)
    continue
    except prawcore.exceptions.RequestException as excep:
    print('SKIPPING due to RequestException:')
    print(excep)
    time.sleep(30)
    continue
    except prawcore.exceptions.ResponseException as excep:
    print('SKIPPING due to ResponseException:')
    print(excep)
    time.sleep(30)
    continue


