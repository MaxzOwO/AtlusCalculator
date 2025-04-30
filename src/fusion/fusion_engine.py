import json
import os
import math
from pathlib import Path
from typing import Dict


def load_demon_data(game: str = "p5r") -> Dict[str, dict]:
    """
    Load demon data for a specific game.

    Loads demon data from a JSON file located in `src/data/{game}/demon-data.json`.
    If DLC data is available in `dlc-data.json`, it will also be loaded and merged.

    Args:
        game (str): The game identifier (e.g., "p5r" for Persona 5 Royal). Defaults to "p5r".

    Returns:
        Dict[str, dict]: A dictionary mapping demon names to their data.
    """
    base = Path("src") / "data" / game

    demons_path = base / "demon-data.json"
    with demons_path.open(encoding="utf-8") as f:
        demons = json.load(f)
    
    # read DLC data if avaliable
    dlc_path = base / "dlc-data.json"
    if dlc_path.exists():
        with dlc_path.open(encoding="utf-8") as f:
            dlc = json.load(f)
        demons.update(dlc)
    return demons


def load_fusion_chart_data(game="p5r"):
    """
    Load fusion chart data for a specific game.

    Loads the fusion chart which defines the race-to-race fusion rules.

    Args:
        game (str): The game identifier. Defaults to "p5r".

    Returns:
        dict: A dictionary representing the fusion chart data.
    """
    path = os.path.join("src", "data", game, "fusion-chart.json")
    with open(path, "r", encoding="utf-8") as file:
        fusion_chart_data = json.load(file)
    return fusion_chart_data


def list_demons_by_race(demons):
    """
    Organize demons by their race.

    Args:
        demons (dict): Dictionary of demon data.

    Returns:
        dict: A dictionary mapping race names to sorted lists of demon names, ordered by level.
    """
    by_race = {}
    
    for name, info in demons.items():
        race = info['race']
        by_race.setdefault(race, []).append(name)
        
    # sorts the demons based on their respective level
    for race, names in by_race.items():
        names.sort(key=lambda x: demons[x]['lvl'])
        
    return by_race



def calculate_fusion(demon1_name: str, demon2_name: str, demons: Dict[str, dict], fusion_chart: Dict, demons_by_race: Dict[str, dict]) -> str: 
    """
    Calculate the result of fusing two demons.

    Args:
        demon1_name (str): The name of the first demon.
        demon2_name (str): The name of the second demon.
        demons (Dict[str, dict]): Dictionary of demon data.
        fusion_chart (Dict): Fusion chart containing fusion rules by race.
        demons_by_race (Dict[str, list]): Dictionary of demons grouped by race.

    Returns:
        str: The name of the resulting demon, or an error message if fusion is invalid.
    """
    if demon1_name not in demons or demon2_name not in demons:
        return "ERR - Invalid demon names"
    if demon1_name == demon2_name:
        return "ERR - Cannot fuse the same demon"
    
    result_demon = None
    
    demon1_info = demons[demon1_name]
    demon2_info = demons[demon2_name]
    
    # get demon1 and demon2 info and level
    demon1_race, demon1_lvl = demon1_info.get('race'), demon1_info.get('lvl')
    demon2_race, demon2_lvl = demon2_info.get('race'), demon2_info.get('lvl')
    
    # get the index of each demons
    demon1_index = fusion_chart['races'].index(demon1_race)
    demon2_index = fusion_chart['races'].index(demon2_race)
    
    # same race fusion
    if demon1_index == demon2_index:
        result_demon = fusion_same_race(demon1_name, demon2_name, demon1_lvl, demon2_lvl, demon1_race, demons, demons_by_race)
    # different race fusion
    else:
        result_demon = fusion_diff_race(demon1_name, demon2_name,demon1_index, demon2_index, demon1_lvl, demon2_lvl, fusion_chart, demons, demons_by_race)
    
    return result_demon


def fusion_same_race(demon1_name: str,demon2_name: str,demon1_lvl: int,demon2_lvl: int,race: str,demons: Dict[str, dict],demons_by_race: Dict[str, dict]) -> str:
    """
    Handle the fusion of two demons from the same race.

    The function calculates the target level using the formula:
        ceil((level1 + level2 + 1) / 2)
    Then it searches for the highest-level demon in the same race that is below or equal to
    the target level, excluding the two input demons.

    Args:
        demon1_name (str): Name of the first demon.
        demon2_name (str): Name of the second demon.
        demon1_lvl (int): Level of the first demon.
        demon2_lvl (int): Level of the second demon.
        race (str): The race shared by both demons.
        demons (Dict[str, dict]): Dictionary containing all demon data.
        demons_by_race (Dict[str, dict]): Dictionary mapping races to lists of demon names.

    Returns:
        str: Name of the resulting fused demon, or None if no valid fusion result exists.
    """
    target_lvl = math.ceil((demon1_lvl + demon2_lvl + 1) / 2)
    print(f"Target level: {target_lvl}")
    possible_demons = demons_by_race.get(race, [])
    result_demon = None
    
    for demon in reversed(possible_demons):
        if demon == demon1_name or demon == demon2_name:
            continue
        cur_level = demons[demon]['lvl']
        
        if cur_level <= target_lvl:
            result_demon = demon
            break
    return result_demon


def fusion_diff_race(demon1_name: str,demon2_name: str,demon1_index: int,demon2_index: int,demon1_lvl: int,demon2_lvl: int,fusion_chart: Dict,demons: Dict[str, dict],demons_by_race: Dict[str, dict]) -> str:
    """
    Handle the fusion of two demons from different races.

    Determines the resulting race using the fusion chart, computes the average level,
    and selects the first demon from the resulting race whose level is >= average level + 1.
    If no such demon is found, returns the highest-level demon in that race.

    Args:
        demon1_name (str): Name of the first demon.
        demon2_name (str): Name of the second demon.
        demon1_index (int): Index of the first demon's race in the fusion chart.
        demon2_index (int): Index of the second demon's race in the fusion chart.
        demon1_lvl (int): Level of the first demon.
        demon2_lvl (int): Level of the second demon.
        fusion_chart (Dict): Fusion chart containing race combination rules.
        demons (Dict[str, dict]): Dictionary containing all demon data.
        demons_by_race (Dict[str, dict]): Dictionary mapping race names to lists of demon names.

    Returns:
        str: Name of the resulting demon, or None if fusion is invalid or no valid result found.
    """
    row_index = max(demon1_index, demon2_index)
    col_index = min(demon1_index, demon2_index)
    
    try:
        result_demon_race = fusion_chart['table'][row_index][col_index]
    except IndexError:
        print("ERR - Invalid fusion chart index [{larger_index}][{smaller_index}] for fusion chart table.")
        return None
    
    if result_demon_race == "-":
        print(f"Error: '-' found off-diagonal in fusion chart at [{row_index}][{col_index}].")
        return None 
    
    
    # calculate the result demon level
    avg_level = math.floor(((demon1_lvl + demon2_lvl) / 2) + 1)
    
    possible_demons = demons_by_race.get(result_demon_race)
    
    
    result_demon_name = None
    found_demon = False
    
    for possible_demon in possible_demons:
        cur_level = demons[possible_demon]['lvl']
        if cur_level >= avg_level:
            if possible_demon != demon1_name and possible_demon != demon2_name:
                result_demon_name = possible_demon
                found_demon = True
                break
    if not found_demon:
        highest_demon_name = possible_demons[-1]
        if highest_demon_name != demon1_name and highest_demon_name != demon2_name:
                result_demon_name = highest_demon_name
    return result_demon_name

