# Implemented by /u/Crazymajor, based on the the original Naval Movement Calculator 

import os
import re
from datetime import datetime, timedelta
from . import dijkstra_methods as dm
from .utils import normalize_location

# ========================= Configuration and Helpers =========================

# Path to naval node map file
NODENAME_FILE = os.path.join(os.path.dirname(__file__), 'naval_nodemap.txt')

# List of named ports used for automatic avoidance (except start/end)
KNOWN_PORTS = [
    "kingshouse", "deepdown", "driftwoodhall", "whiteharbor", "barrowton",
    "bearisland", "flintsfinger", "riverrun", "fairmarket", "lordharrowaystown",
    "maidenpool", "seagard", "briarwhite", "pebble", "thepaps", "gulltown",
    "witchisle", "oldanchor", "wickenden", "sisterton", "longsister",
    "littlesister", "pyke", "ironholt", "saltcliffe", "tentowers", "volmark",
    "hammerhorn", "sealskinpoint", "pebbleton", "lonelylight", "oldwyk",
    "orkmont", "blacktyde", "kingslanding", "dragonstone", "driftmark",
    "hightide", "sharppoint", "sweetportsound", "clawisle", "duskendale",
    "casterlyrock", "feastfires", "kayce", "crakehall", "faircastle",
    "riverspring", "highgarden", "oldtown", "vinetown", "ryamsport",
    "greenshield", "southshield", "grimston", "lordhewettstown", "bitterbridge",
    "stonehelm", "weepingtown", "evenfallhall", "s41", "greenstone",
    "sunspear", "plankytown", "yronwood", "godsgrace", "starfall", "saltshore"
]

# ========================= Movement Calculation =========================

def nclean_movement(speed, start, end, sdatetime="now", avoid_list=None):
    """
    Core pathfinding function. Returns path, arrival time, and duration for a single movement leg.
    """
    if avoid_list is None:
        avoid_list = []

    if sdatetime == "now":
        sdatetime = datetime.now()
    elif not isinstance(sdatetime, datetime):
        sdatetime = datetime.strptime(sdatetime, '%d/%m/%y %H:%M:%S')

    graph = dm.Graph(NODENAME_FILE, avoid_list=avoid_list)
    path, distance = graph.shortest_path(start, end)

    delta = 48 * distance / speed
    end_time = sdatetime + timedelta(hours=delta)

    return path, end_time, delta

# ========================= Multi-Leg Movement Engine =========================

def naval_movement_bot(speed, start, end_list, openwater="y", opt_route=True, avoid_list=None, start_time="now"):
    """
    Handles multi-leg naval movements with automatic port avoidance and optional open water restriction.
    Returns detailed path, cumulative time, and final arrival.
    """
    if avoid_list is None:
        avoid_list = []

    total_time = 0
    all_paths = []
    avoid_set = set(a.lower() for a in avoid_list if a)
    ow_avoid = [f"os{i}" for i in range(1, 60)] if openwater != "y" else []

    known_ports_set = set(KNOWN_PORTS)

    for i, end in enumerate(end_list):
        current_start = start if i == 0 else end_list[i - 1]

        full_avoid = []

        # Block open water nodes if requested
        if openwater != "y":
            full_avoid.extend(ow_avoid)

        # Auto-avoid known ports unless start/end
        for port in known_ports_set:
            if port != current_start and port != end:
                full_avoid.append(port)

        # Include user-defined avoid list if optimal route disabled
        if not opt_route:
            full_avoid.extend(avoid_list)

        # Calculate leg
        path, end_time, delta = nclean_movement(speed, current_start, end, start_time, full_avoid)

        # Check for forbidden nodes in path
        blocked_nodes = avoid_set.intersection(set(path) - {current_start, end})
        if blocked_nodes:
            raise ValueError(f"Cannot complete route without passing through avoided provinces: {', '.join(blocked_nodes)}")

        all_paths.append((path, delta, end_time))
        total_time += delta
        start_time = end_time
    
    if not end_list:
        raise ValueError("Destination list is empty. At least one destination required.")

    return all_paths, total_time, end_time

# ========================= Reddit Bot Comment Parser =========================

def parse_naval_movement_comment(comment):
    """
    Parses Reddit comment text and builds formatted naval movement summary.
    Includes detailed time breakdown for each leg.
    """
    lines = [line.strip() for line in comment.body.splitlines() if line.strip()]
    speed, start, start_time = None, None, "now"
    end, avoid, openwater, opt_route = [], [], "y", True

    for line in lines:
        if re.match(r"Speed\s*:\s*(.*)", line, re.IGNORECASE):
            try:
                speed_val = re.findall(r"Speed\s*:\s*(.*)", line, re.IGNORECASE)[0].strip()
                speed = float(speed_val) if speed_val.lower() != "lorecog" else 20
            except ValueError:
                raise ValueError("Invalid speed. Provide numeric speed or 'lorecog'.")
        elif re.match(r"Start\s*:\s*(.*)", line, re.IGNORECASE):
            start = normalize_location(re.findall(r"Start\s*:\s*(.*)", line, re.IGNORECASE)[0].strip())
        elif re.match(r"End\s*:\s*(.*)", line, re.IGNORECASE):
            end = [normalize_location(e.strip()) for e in re.findall(r"End\s*:\s*(.*)", line, re.IGNORECASE)[0].split(",")]
        elif re.match(r"Open Water\s*:\s*(.*)", line, re.IGNORECASE):
            openwater = re.findall(r"Open Water\s*:\s*(.*)", line, re.IGNORECASE)[0].strip().lower()
        elif re.match(r"Optimal Route\s*:\s*(.*)", line, re.IGNORECASE):
            opt_route = re.findall(r"Optimal Route\s*:\s*(.*)", line, re.IGNORECASE)[0].strip().lower() == "y"
        elif re.match(r"Avoid\s*:\s*(.*)", line, re.IGNORECASE):
            avoid = [normalize_location(a.strip()) for a in re.findall(r"Avoid\s*:\s*(.*)", line, re.IGNORECASE)[0].split(",")]
        elif re.match(r"Time\s*:\s*(.*)", line, re.IGNORECASE):
            start_time = re.findall(r"Time\s*:\s*(.*)", line, re.IGNORECASE)[0].strip()

    # Basic validation
    if speed is None:
        raise ValueError("Missing speed. Include 'Speed: [value]'.")
    if not start:
        raise ValueError("Missing starting province. Include 'Start: [province]'.")
    if not end:
        raise ValueError("Missing destination(s). Include 'End: [province list]'.")

    graph = dm.Graph(NODENAME_FILE)
    known_nodes = graph.nodes

    if start not in known_nodes:
        raise ValueError(f"Unknown starting province '{start}'. Check spelling.")
    for destination in end:
        if destination not in known_nodes:
            raise ValueError(f"Unknown destination '{destination}'. Check spelling.")
    for a in avoid:
        if a and a not in known_nodes:
            raise ValueError(f"Unknown avoid province '{a}'. Check spelling.")
    if start_time.lower() != "now":
        try:
            datetime.strptime(start_time, '%d/%m/%y %H:%M:%S')
        except ValueError:
            raise ValueError("Invalid time format. Use 'DD/MM/YY HH:MM:SS' or 'now'.")

    # Movement execution
    paths, total_hours, arrival_time = naval_movement_bot(
        speed, start, end, openwater, opt_route, avoid, start_time
    )

    # Build reply with leg-by-leg breakdown
    response = "**Naval Movement Order Processed**\n\n"

    for idx, (path, delta, leg_arrival) in enumerate(paths):
        response += f"* *Move {idx + 1}*: {' → '.join(path)}\n"
        response += f"  - Travel Time: **{delta:.2f} hours**\n"
        response += f"  - Arrival at Destination: **{leg_arrival.strftime('%d/%m/%Y %H:%M:%S')}**\n\n"

    # Only show final arrival summary if multiple moves
    if len(paths) > 1:
        response += f"---\n\n"
        response += f"**Total Travel Time:** {total_hours:.2f} hours\n\n"
        response += f"**Final Arrival:** {arrival_time.strftime('%d/%m/%Y %H:%M:%S')}"

    return response
