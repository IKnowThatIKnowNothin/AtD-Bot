import praw
import os
import re
import Battle
import Duel
import Joust
import time
import Army
import random
import Globals

reddit = praw.Reddit(user_agent=os.environ['AGENT_NAME'] ,
                     client_id=os.environ['PRAW_ID'] ,
                     client_secret=os.environ['PRAW_SECRET'] ,
                     password=os.environ['REDDIT_PW'] ,
                     username=os.environ['REDDIT_USER']
)

print(reddit.user.me())
print("---\n")

subreddit = reddit.subreddit('AfterTheDance+AfterTheDanceMods+awoiafpowers+NinePennyKings+NinePennyKingsMods')
for comment in subreddit.stream.comments(skip_existing=True):
    try:
        comment.refresh()
    
        if((re.search('/u/modbotshit',comment.body,re.IGNORECASE) or re.search('u/modbotshit',comment.body,re.IGNORECASE)) and comment.id not in comments_replied_to): #Make sure we're tagged in order to run. Non caps-sensitive.
            comments_replied_to.append(comment.id)
    
            if(re.search("Roll",comment.body,re.IGNORECASE)):
              try:
                  battleInfo = re.findall("(\d+)([d])(\d+)([\+\-]?\d*)(.*)",comment.body)
                  if(battleInfo):
                      roundmessage= ""
                      for j in battleInfo:
                          bonus = 0
                          noDice = int(j[0]) #(battleInfo.group(1))
                          sizeDice = int(j[2]) #(battleInfo.group(3))
                          if (j[3]):
                              bonus = int(j[3]) #(battleInfo.group(4))
                          else:
                              bonus = 0
                          name = j[4] #battleInfo.group(5)
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

                  comment.reply(roundmessage)#Post all at once
                  print("---\n")
              
        
              except:
                print ("Improperly formatted roll\n---\n")
                comment.reply("Improperly formatted Roll.")
              time.sleep(60) #We sleep for 3 minutes after each battle so we don't get screwed by rate limits. Delete this when karma is high enough.
                
                
            elif(re.search("Naval Battle",comment.body,re.IGNORECASE)):
                Globals.battleType = "Naval"
                battleInfo = re.match("(.*) ([\-]?\d+)(.*)\n+(.*) (\d+) ([\+\-]?\d*)\n+(.*) ([\-]?\d+)(.*)\n+(.*) (\d+) ([\+\-]?\d*)",comment.body)
                if(battleInfo):
                    print ("Running Naval battle\n")
                    battle = Battle.Battle()
                    print ("Quick Mode\n")
                    comment.reply(battle.run(battleInfo))#Post all at once

                    print("---\n")
                else:
                    print ("Improperly formatted battle\n---\n")
                    comment.reply("Improperly formatted battle info.")
                time.sleep(60) #We sleep for 3 minutes after each battle so we don't get screwed by rate limits. Delete this when karma is high enough.



                        
            elif(re.search("Land Battle",comment.body,re.IGNORECASE)):
                Globals.battleType = "Land"
                battleInfo = re.match("(.*) ([\-]?\d+)(.*)\n+(.*) (\d+) ([\+\-]?\d*)\n+(.*) ([\-]?\d+)(.*)\n+(.*) (\d+) ([\+\-]?\d*)",comment.body)
                if(battleInfo):
                    print ("Running Land battle\n")
                    battle = Battle.Battle()
                    print ("Quick Mode\n")
                    comment.reply(battle.run(battleInfo))#Post all at once
                    print("---\n")
                else:
                    print ("Improperly formatted battle\n---\n")
                    comment.reply("Improperly formatted battle info.")
                time.sleep(60) #We sleep for 3 minutes after each battle so we don't get screwed by rate limits. Delete this when karma is high enough.
           
            elif(re.search("Joust",comment.body,re.IGNORECASE)):
                Globals.battleType = "Joust"
                joustInfo = re.match("(.*) ([\+\-]?\d*)\n+(.*) ([\+\-]?\d*)",comment.body)
                if(joustInfo):
                    print ("Running Joust\n")
                    joust = Joust.Joust()
                    
                    Globals.resultsMode = False
                    print ("Quick Mode\n")
                    comment.reply(joust.run(joustInfo))#Post all at once

                    print("--- \n")
                else:
                    print ("Improperly formatted joust\n---\n")
                    comment.reply("Improperly formatted joust info.")
                time.sleep(60) #We sleep for 3 minutes after each duel so we don't get screwed by rate limits. Delete this when karma is high enough.


            elif(re.search("Duel",comment.body,re.IGNORECASE)):
                duelInfo = re.match("(.*) ([\-]?\d+) ([\+\-]?\d*) (.*) (.*)\n+(.*) ([\-]?\d+) ([\+\-]?\d*) (.*) (.*)",comment.body)
                if(duelInfo):
                    print ("Running Live Duel\n")
                    duel = Duel.Duel()

                    Globals.resultsMode = False
                    print ("Quick Mode\n")
                    result = duel.run(duelInfo)
                    #print(result)
                    comment.reply(result)#Post all at once

                    print("--- \n")
                else:
                    print ("\nImproperly formatted duel\n--- \n")
                    comment.reply("Improperly formatted duel info.")
                time.sleep(60) #We sleep for 3 minutes after each duel so we don't get screwed by rate limits. Delete this when karma is high enough
                
            else:
                comment.reply("Improperly formatted info. Please state which function you wish to use.")
                print("Improperly formatted info\n---\n")

    except praw.exceptions.ClientException as excep:  # fix for deleted comments
        print('SKIPPING due to ClientException:')
        print(excep)
        continue

    
