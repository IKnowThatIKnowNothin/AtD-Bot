# Implemented by /u/Crazymajor, based on the the original Land Movement Calculator 

from . import dijkstra_methods as dm
from datetime import datetime, timedelta
import re
import os
from .utils import normalize_location


NODENAME_FILE = os.path.join(os.path.dirname(__file__), 'land_nodemap.txt')

# ================== Core Movement Functions ==================

def movement(speed, start, end, sdatetime="now", avoid_list=None):
    if avoid_list is None:
        avoid_list = []

    nodemap = NODENAME_FILE

    if sdatetime == "now":
        sdatetime = datetime.now()
    elif not isinstance(sdatetime, datetime):
        sdatetime = datetime.strptime(sdatetime, '%d/%m/%y %H:%M:%S')

    graph = dm.Graph(nodemap, avoid_list=avoid_list)
    path, distance = graph.shortest_path(start, end)
    
    delta = 48 * distance / speed
    end_time = sdatetime + timedelta(hours=delta)

    return path, end_time, delta


def clean_movement(speed, start, end, sdatetime="now", avoid_list=None):
    if avoid_list is None:
        avoid_list = []

    nodemap = NODENAME_FILE

    if sdatetime == "now":
        sdatetime = datetime.now()
    elif not isinstance(sdatetime, datetime):
        sdatetime = datetime.strptime(sdatetime, '%d/%m/%y %H:%M:%S')

    graph = dm.Graph(nodemap, avoid_list=avoid_list)
    path, distance = graph.shortest_path(start, end)
    
    delta = 48 * distance / speed
    end_time = sdatetime + timedelta(hours=delta)

    return path, end_time, delta

# ================== Batch Movement for Multiple Destinations ==================

def land_movement_bot(speed, start, end_list, opt_route=True, avoid_list=None, start_time="now"):
    """
    Calculates path(s) for multi-leg land movement, blocks paths through avoided nodes.
    """
    if avoid_list is None:
        avoid_list = []

    total_time = 0
    all_paths = []

    # Normalize avoid list
    avoid_set = set(a.lower() for a in avoid_list if a)

    if start.lower() == 'lannisport':
        start = 'casterlyrock'

    for i, end in enumerate(end_list):
        if end.lower() == 'lannisport':
            end = 'casterlyrock'
        
        current_start = start if i == 0 else end_list[i - 1]
        
        # Use avoid list only if optimal route is disabled
        path, end_time, delta = clean_movement(speed, current_start, end, start_time, avoid_list if not opt_route else [])
        
        # Check if any avoided nodes are in the resulting path (besides start/end)
        blocked_nodes = avoid_set.intersection(set(path) - {current_start.lower(), end.lower()})
        if blocked_nodes:
            raise ValueError(f"Cannot complete route without passing through avoided provinces: {', '.join(blocked_nodes)}")

        all_paths.append((path, delta, end_time))
        total_time += delta
        start_time = end_time  # Chain the end time for next leg

    if not end_list:
        raise ValueError("Destination list is empty. At least one destination required.")

    return all_paths, total_time, end_time


# ================== Reddit Bot Comment Parser ==================

def parse_land_movement_comment(comment):
    """
    Parses Reddit comment and returns formatted land movement reply text.
    Raises ValueError for missing fields or invalid inputs.
    """
    lines = [line.strip() for line in comment.body.splitlines() if line.strip()]
    speed, start, start_time = None, None, "now"
    end = []
    opt_route = True
    avoid = []

    for line in lines:
        if re.match(r"Speed\s*:\s*(.*)", line, re.IGNORECASE):
            try:
                speed = float(re.findall(r"Speed\s*:\s*(.*)", line, re.IGNORECASE)[0].strip())
            except ValueError:
                raise ValueError("Invalid speed value. Please provide a numeric speed.")
        elif re.match(r"Start\s*:\s*(.*)", line, re.IGNORECASE):
            start = normalize_location(re.findall(r"Start\s*:\s*(.*)", line, re.IGNORECASE)[0].strip())
        elif re.match(r"End\s*:\s*(.*)", line, re.IGNORECASE):
            end = [normalize_location(e.strip()) for e in re.findall(r"End\s*:\s*(.*)", line, re.IGNORECASE)[0].split(",")]
        elif re.match(r"Optimal Route\s*:\s*(.*)", line, re.IGNORECASE):
            opt_route = re.findall(r"Optimal Route\s*:\s*(.*)", line, re.IGNORECASE)[0].strip().lower() == "y"
        elif re.match(r"Avoid\s*:\s*(.*)", line, re.IGNORECASE):
            avoid = [normalize_location(a.strip()) for a in re.findall(r"Avoid\s*:\s*(.*)", line, re.IGNORECASE)[0].split(",")]
        elif re.match(r"Time\s*:\s*(.*)", line, re.IGNORECASE):
            start_time = re.findall(r"Time\s*:\s*(.*)", line, re.IGNORECASE)[0].strip()

    # Validate required fields
    if speed is None:
        raise ValueError("Missing movement speed. Please include a 'Speed: [value]' line.")
    if not start:
        raise ValueError("Missing starting location. Please include a 'Start: [location]' line.")
    if not end:
        raise ValueError("Missing destination(s). Please include an 'End: [destination]' line with at least one destination.")

    # Validate known provinces
    nodemap = NODENAME_FILE
    graph = dm.Graph(nodemap, avoid_list=avoid if not opt_route else [])
    known_nodes = graph.nodes

    if start not in known_nodes:
        raise ValueError(f"Unknown starting province '{start}'. Please check spelling and capitalization.")
    for destination in end:
        if destination not in known_nodes:
            raise ValueError(f"Unknown destination province '{destination}'. Please check spelling and capitalization.")
    for a in avoid:
        if a and a not in known_nodes:
            raise ValueError(f"Unknown avoid province '{a}'. Please check spelling and capitalization.")

    # Validate time format
    if start_time.lower() != "now":
        try:
            datetime.strptime(start_time, '%d/%m/%y %H:%M:%S')
        except ValueError:
            raise ValueError("Invalid time format. Please use 'DD/MM/YY HH:MM:SS' or 'now'.")

    # Run movement calculation
    paths, total_hours, arrival_time = land_movement_bot(speed, start, end, opt_route, avoid, start_time)

    # Build reply
    response = "**Land Movement Order Processed**\n\n"

    for idx, (path, delta, leg_arrival) in enumerate(paths):
        response += f"* *Move {idx + 1}*: {' → '.join(path)}\n"
        response += f"  - Travel Time: **{delta:.2f} hours**\n"
        response += f"  - Arrival at Destination: **{leg_arrival.strftime('%d/%m/%Y %H:%M:%S')}**\n\n"


    # Only show final arrival if more than one move exists
    if len(paths) > 1:
        response += f"---\n\n"
        response += f"**Total Travel Time:** {total_hours:.2f} hours\n\n"
        response += f"**Final Arrival:** {arrival_time.strftime('%d/%m/%Y %H:%M:%S')}"

    return response
