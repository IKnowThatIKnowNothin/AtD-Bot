import re
import Duel
import Globals

def run_case(body):
    is_blunted = bool(re.search("Blunted Duel", body, re.IGNORECASE))
    duelInfo = re.match(
        r"(.*) ([\-]?\d+) ([\+\-]?\d*) ([\+\-]?\d*) ([\+\-]?\d*)(?: (\d+))?\n+"
        r"(.*) ([\-]?\d+) ([\+\-]?\d*) ([\+\-]?\d*) ([\+\-]?\d*)(?: (\d+))?",
        body
    )

    if not duelInfo:
        print("FAILED TO PARSE\n", body)
        return

    d = Duel.Duel()
    d.LIVE_STEEL = not is_blunted
    Globals.resultsMode = False
    print("MODE:", "BLUNTED" if is_blunted else "LIVE")
    print(d.run(duelInfo)) # print first chunk so terminal isn’t flooded
    print("\n" + "="*80 + "\n")

LIVE = """Renly Rowan -48 +5 +18 +0 5
Caradoc Peake -46 +2 +16 +5 5

Duel
"""

BLUNTED = """Renly Rowan -48 +5 +18 +0 5
Caradoc Peake -46 +2 +16 +5 5

Blunted Duel
"""
run_case(BLUNTED)