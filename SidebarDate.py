from datetime import datetime
from datetime import timedelta
from datetime import date
import re
import time
import math
import praw

###This is no longer in use but will be kept in the repository for archival purposes

def ic_date(date_ooc):
  #Converts IRL UTC time to in-game date system
  #First find difference from provided time from 00:00 UTC 02/01/23
  game_start = date(2024, 1, 2)
  difference = date_ooc - game_start
  #Convert difference to days
  days = difference.days
  ic_year = (days // 21) + 270
  newsday_count = (days + 1) // 7
  ic_month = (((days - newsday_count) / 2) % 9) + 1
  #print("IC Year: ", ic_year, "IC Month: ", ic_month)
  return ic_year, ic_month


def ooc_date(ic_year, ic_month):
  #Converts in-game date system to IRL UTC time
  game_start = date(2024, 1, 2)
  newsday_count = math.floor((ic_month - 1) / 3)
  delta_time = timedelta(days=((ic_year - 270) * 21) + ((ic_month - 1) * 2) +
                         newsday_count)
  return game_start + delta_time


def display_ic_date(ic_year, ic_month):
  full_month = math.floor(ic_month)
  half_month = "A"
  if full_month != ic_month:
    half_month = "B"
  months = ["1st", "2nd", "3rd", "4th", "5th", "6th", "7th", "8th", "9th"]
  return months[math.floor(ic_month) -
                1] + " Month " + half_month + ", " + str(ic_year) +"AC"

def current_ic_date():
    ic_year, ic_month = ic_date(datetime.date(datetime.utcnow()))
    return display_ic_date(ic_year, ic_month)

def update_ic_date(reddit):
    print("Update date")
    wiki_page = reddit.subreddit("NinePennyKings").wiki['config/sidebar']
    content = wiki_page.content_md
    match = re.search(r"##\[Date: (.*)\]", content)
    current_date = current_ic_date()
    if match:
        old_date = match.group(1)
        print(old_date)
        print(current_date)
        if old_date != current_date:
          content = re.sub(r"##\[Date:.*\]", "##[Date: " + current_date + "]", content)
          wiki_page.edit(content, "Updated sidebar date")
          print("Updated sidebar date")
          return 
        else:
            print("Failed to update sidebar date, no change")  
            return
    else:        
        print("Failed to update sidebar date, could not be found")
        return
      

