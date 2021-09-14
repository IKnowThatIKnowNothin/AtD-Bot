import praw
import os
import re
import Battle
#import Duel
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

print("---\n")

with open("comments_replied_to.txt", "r") as f:
    comments_replied_to = f.read()
    comments_replied_to = comments_replied_to.split("\n")
    comments_replied_to = list(filter(None, comments_replied_to))
subreddit = reddit.subreddit('AfterTheDance+AfterTheDanceMods+awoiafpowers')
for comment in subreddit.stream.comments(skip_existing=True):
    try:
        comment.refresh()
    
        if((re.search('/u/modbotshit',comment.body,re.IGNORECASE) or re.search('u/modbotshit',comment.body,re.IGNORECASE)) and comment.id not in comments_replied_to): #Make sure we're tagged in order to run. Non caps-sensitive.
            comments_replied_to.append(comment.id)
    
            if(re.search("Roll",comment.body,re.IGNORECASE)):
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
                    with open("comments_replied_to.txt", "w") as f:
                        for comment_id in comments_replied_to:
                            f.write(comment_id + "\n")
                    print("---\n")
              
                else:
                    print ("Improperly formatted roll\n---\n")
                    comment.reply("Improperly formatted Roll. Please format comment as follows: \n \n 1d100 \n \n Roll \n \n tag ModBotShit")
                    with open("comments_replied_to.txt", "w") as f:
                        for comment_id in comments_replied_to:
                            f.write(comment_id + "\n")
                time.sleep(60) #We sleep for 3 minutes after each battle so we don't get screwed by rate limits. Delete this when karma is high enough.
                
                
            elif(re.search("Naval Battle",comment.body,re.IGNORECASE)):
                Globals.battleType = "Naval"
                battleInfo = re.match("(.*) ([\-]?\d*)\n+(.*) (\d+) ([\+\-]?\d*)\n+(.*) ([\+\-]?\d*)\n+(.*) (\d+) ([\+\-]?\d*)",comment.body)
                if(battleInfo):
                    print ("Running Naval battle\n")
                    battle = Battle.Battle()
                    if(re.search("Dramatic Mode",comment.body,re.IGNORECASE)):
                        print ("Dramatic Mode\n")
                        lastcomment = comment
                        comments_replied_to.append(lastcomment.id)
                        for roundCount in battle.run(battleInfo).split("---"):
                            try:
                                lastcomment = lastcomment.reply(roundCount)
                                comments_replied_to.append(lastcomment.id)
                                with open("comments_replied_to.txt", "w") as f:
                                    for comment_id in comments_replied_to:
                                        f.write(comment_id + "\n")
                            except: #Shouldn't happen too much, but in case we get rate limited.
                                print("Rate limited. Sleeping for 6 minutes.")
                                time.sleep(360)
                                lastcomment = lastcomment.reply(roundCount)
                                comments_replied_to.append(lastcomment.id)
                                with open("comments_replied_to.txt", "w") as f:
                                    for comment_id in comments_replied_to:
                                        f.write(comment_id + "\n")
                            time.sleep(60)
                    else:
                        print ("Quick Mode\n")
                        comment.reply(battle.run(battleInfo))#Post all at once
                        with open("comments_replied_to.txt", "w") as f:
                            for comment_id in comments_replied_to:
                                f.write(comment_id + "\n")

                    print("---\n")
                else:
                    print ("Improperly formatted battle\n---\n")
                    comment.reply("Improperly formatted battle info. Please format comment as follows: \n \nCommanderName + CommanderBonus\n \nAttackerName AttackerStrength +AttackerBonus \n \nCommanderName + CommanderBonus\n \nDefenderName DefenderStrength +DefenderBonus\n \nDramatic Mode (optional) \n \ntag ManyFacedBot")
                    with open("comments_replied_to.txt", "w") as f:
                        for comment_id in comments_replied_to:
                            f.write(comment_id + "\n")
                time.sleep(60) #We sleep for 3 minutes after each battle so we don't get screwed by rate limits. Delete this when karma is high enough.



                        
            elif(re.search("Land Battle",comment.body,re.IGNORECASE)):
                Globals.battleType = "Land"
                battleInfo = re.match("(.*) ([\-]?\d*)\n+(.*) (\d+) ([\+\-]?\d*)\n+(.*) ([\+\-]?\d*)\n+(.*) (\d+) ([\+\-]?\d*)",comment.body)
                if(battleInfo):
                    print ("Running Land battle\n")
                    battle = Battle.Battle()
                    if(re.search("Dramatic Mode",comment.body,re.IGNORECASE)):
                        print ("Dramatic Mode\n")
                        lastcomment = comment
                        comments_replied_to.append(lastcomment.id)
                        for roundCount in battle.run(battleInfo).split("---"):
                            try:
                                lastcomment = lastcomment.reply(roundCount)
                                comments_replied_to.append(lastcomment.id)
                                with open("comments_replied_to.txt", "w") as f:
                                    for comment_id in comments_replied_to:
                                        f.write(comment_id + "\n")
                            except: #Shouldn't happen too much, but in case we get rate limited.
                                print("Rate limited. Sleeping for 6 minutes.")
                                time.sleep(360)
                                lastcomment = lastcomment.reply(roundCount)
                                comments_replied_to.append(lastcomment.id)
                                with open("comments_replied_to.txt", "w") as f:
                                    for comment_id in comments_replied_to:
                                        f.write(comment_id + "\n")
                            time.sleep(60)
                    else:
                        print ("Quick Mode\n")
                        comment.reply(battle.run(battleInfo))#Post all at once
                        with open("comments_replied_to.txt", "w") as f:
                            for comment_id in comments_replied_to:
                                f.write(comment_id + "\n")
                    print("---\n")
                else:
                    print ("Improperly formatted battle\n---\n")
                    comment.reply("Improperly formatted battle info. Please format comment as follows: \n \nCommanderName + CommanderBonus\n \nAttackerName AttackerStrength +AttackerBonus \n \nCommanderName + CommanderBonus\n \nDefenderName DefenderStrength +DefenderBonus\n \nDramatic Mode (optional) \n \ntag ManyFacedBot")
                    with open("comments_replied_to.txt", "w") as f:
                        for comment_id in comments_replied_to:
                            f.write(comment_id + "\n")
                time.sleep(60) #We sleep for 3 minutes after each battle so we don't get screwed by rate limits. Delete this when karma is high enough.
                

            elif(re.search("Duel",comment.body,re.IGNORECASE)):
                duelInfo = re.match("(.*) ([\+\-]?\d+)(.*)\n+(.*) ([\+\-]?\d+)(.*)",comment.body)
                if(duelInfo):
                    print ("Running Live Duel\n")
                    duel = Duel.Duel()
                    if(re.search("Dramatic Mode",comment.body,re.IGNORECASE)):
                        print ("Dramatic Mode\n")
                        Globals.resultsMode = False
                        lastcomment = comment
                        comments_replied_to.append(lastcomment.id)
                        for roundCount in duel.run(duelInfo).split("---"):
                            try:
                                lastcomment = lastcomment.reply(roundCount)
                                comments_replied_to.append(lastcomment.id)
                                with open("comments_replied_to.txt", "w") as f:
                                    for comment_id in comments_replied_to:
                                        f.write(comment_id + "\n")
                            except: #Shouldn't happen too much, but in case we get rate limited.
                                print("Rate limited. Sleeping for 6 minutes.")
                                time.sleep(360)
                                lastcomment = lastcomment.reply(roundCount)
                                comments_replied_to.append(lastcomment.id)
                                with open("comments_replied_to.txt", "w") as f:
                                    for comment_id in comments_replied_to:
                                        f.write(comment_id + "\n")
                            time.sleep(30)
                        
                    elif(re.search("Results Mode",comment.body,re.IGNORECASE)):
                        Globals.resultsMode = True
                        print ("Results Mode\n")
                        comment.reply(duel.run(duelInfo))#Post all at once
                        with open("comments_replied_to.txt", "w") as f:
                            for comment_id in comments_replied_to:
                                f.write(comment_id + "\n")
                    else:
                        Globals.resultsMode = False
                        print ("Quick Mode\n")
                        comment.reply(duel.run(duelInfo))#Post all at once
                        with open("comments_replied_to.txt", "w") as f:
                            for comment_id in comments_replied_to:
                                f.write(comment_id + "\n")

                    print("--- \n")
                else:
                    print ("\nImproperly formatted duel\n--- \n")
                    comment.reply("Improperly formatted duel info. Please format comment as follows: \n \nName of PC 1 +X \n \nName of PC 2 +X \n \nDramatic Mode (optional) \n \n Live Duel or Blunted Duel \n\ntag ManyFacedBot")
                    with open("comments_replied_to.txt", "w") as f:
                        for comment_id in comments_replied_to:
                            f.write(comment_id + "\n")
                time.sleep(60) #We sleep for 3 minutes after each duel so we don't get screwed by rate limits. Delete this when karma is high enough
                
            else:
                comment.reply("Improperly formatted info. Please state which function you wish to use; Roll, Land Battle, Naval Battle, Ambush, Assault, Boxing, Live Duel, or Blunted Duel")
                print("Improperly formatted info\n---\n")

    except praw.exceptions.ClientException:  # fix for deleted comments
        print('SKIPPING due to ClientException')
        continue

    
