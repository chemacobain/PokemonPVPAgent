import requests
import pandas as pd

# Type effectiveness chart (Attacker -> Defender multipliers)
# 2.0: Super Effective, 0.5: Not Very Effective, 0.390625: Immune (approx 0.39)
# We only care about weaknesses (multiplier > 1.0)
TYPE_CHART = {
    "normal": {"rock": 0.5, "ghost": 0.39, "steel": 0.5},
    "fire": {"fire": 0.5, "water": 0.5, "grass": 2.0, "ice": 2.0, "bug": 2.0, "rock": 0.5, "dragon": 0.5, "steel": 2.0},
    "water": {"fire": 2.0, "water": 0.5, "grass": 0.5, "ground": 2.0, "rock": 2.0, "dragon": 0.5},
    "grass": {"fire": 0.5, "water": 2.0, "grass": 0.5, "poison": 0.5, "ground": 2.0, "flying": 0.5, "bug": 0.5, "rock": 2.0, "dragon": 0.5, "steel": 0.5},
    "electric": {"water": 2.0, "grass": 0.5, "electric": 0.5, "ground": 0.39, "flying": 2.0, "dragon": 0.5},
    "ice": {"fire": 0.5, "water": 0.5, "grass": 2.0, "ice": 0.5, "ground": 2.0, "flying": 2.0, "dragon": 2.0, "steel": 0.5},
    "fighting": {"normal": 2.0, "ice": 2.0, "poison": 0.5, "flying": 0.5, "psychic": 0.5, "bug": 0.5, "rock": 2.0, "ghost": 0.0, "dark": 2.0, "steel": 2.0, "fairy": 0.5},
    "poison": {"grass": 2.0, "poison": 0.5, "ground": 0.5, "rock": 0.5, "ghost": 0.5, "steel": 0.0, "fairy": 2.0},
    "ground": {"fire": 2.0, "grass": 0.5, "electric": 2.0, "poison": 2.0, "flying": 0.0, "bug": 0.5, "rock": 2.0, "steel": 2.0},
    "flying": {"grass": 2.0, "electric": 0.5, "fighting": 2.0, "bug": 2.0, "rock": 0.5, "steel": 0.5},
    "psychic": {"fighting": 2.0, "poison": 2.0, "psychic": 0.5, "dark": 0.0, "steel": 0.5},
    "bug": {"fire": 0.5, "grass": 2.0, "fighting": 0.5, "poison": 0.5, "flying": 0.5, "psychic": 2.0, "ghost": 0.5, "dark": 2.0, "steel": 0.5, "fairy": 0.5},
    "rock": {"fire": 2.0, "ice": 2.0, "fighting": 0.5, "ground": 0.5, "flying": 2.0, "bug": 2.0, "steel": 0.5},
    "ghost": {"normal": 0.0, "psychic": 2.0, "ghost": 2.0, "dark": 0.5},
    "dragon": {"dragon": 2.0, "steel": 0.5, "fairy": 0.0},
    "dark": {"fighting": 0.5, "psychic": 2.0, "ghost": 2.0, "dark": 0.5, "fairy": 0.5},
    "steel": {"fire": 0.5, "water": 0.5, "electric": 0.5, "ice": 2.0, "rock": 2.0, "steel": 0.5, "fairy": 2.0},
    "fairy": {"fire": 0.5, "fighting": 2.0, "poison": 0.5, "dragon": 2.0, "dark": 2.0, "steel": 0.5}
}

ALL_TYPES = list(TYPE_CHART.keys())

def get_weaknesses(defender_types):
    """
    Calculate weaknesses for a given list of defender types.
    Returns a list of types that are super effective against the defender.
    """
    weaknesses = []
    
    for attacker_type in ALL_TYPES:
        multiplier = 1.0
        for defender_type in defender_types:
            defender_type = defender_type.lower()
            # Default to 1.0 if not in chart (neutral)
            if attacker_type in TYPE_CHART:
                effect = TYPE_CHART[attacker_type].get(defender_type, 1.0)
                multiplier *= effect
        
        if multiplier > 1.0:
            weaknesses.append(attacker_type)
            
    return weaknesses

def load_data():
    """
    Fetches ranking and gamemaster data, merges them, and returns a list of Pokemon dictionaries.
    """
    print("Fetching rankings data...")
    rankings_url = "https://raw.githubusercontent.com/pvpoke/pvpoke/master/src/data/rankings/all/overall/rankings-1500.json"
    try:
        rankings_response = requests.get(rankings_url)
        rankings_response.raise_for_status()
        rankings_data = rankings_response.json()
    except Exception as e:
        print(f"Error fetching rankings: {e}")
        return []

    print("Fetching gamemaster data (for types)...")
    gamemaster_url = "https://raw.githubusercontent.com/pvpoke/pvpoke/master/src/data/gamemaster/pokemon.json"
    try:
        gamemaster_response = requests.get(gamemaster_url)
        gamemaster_response.raise_for_status()
        gamemaster_data = gamemaster_response.json()
    except Exception as e:
        print(f"Error fetching gamemaster: {e}")
        return []

    print("Fetching moves data...")
    moves_url = "https://raw.githubusercontent.com/pvpoke/pvpoke/master/src/data/gamemaster/moves.json"
    try:
        moves_response = requests.get(moves_url)
        moves_response.raise_for_status()
        moves_data = moves_response.json()
    except Exception as e:
        print(f"Error fetching moves: {e}")
        return []

    # Create a map of speciesId -> types
    species_types_map = {}
    for pokemon in gamemaster_data:
        species_id = pokemon.get("speciesId")
        types = pokemon.get("types", [])
        if species_id:
            species_types_map[species_id] = types

    # Create a map of moveId -> type
    moves_map = {}
    for move in moves_data:
        move_id = move.get("moveId")
        move_type = move.get("type")
        if move_id and move_type:
            moves_map[move_id] = move_type

    processed_data = []

    for entry in rankings_data:
        species_id = entry.get("speciesId")
        species_name = entry.get("speciesName")
        score = entry.get("score")
        moveset = entry.get("moveset", [])
        
        # Get types from gamemaster map
        types = species_types_map.get(species_id, [])
        
        # Get move types
        move_types = []
        for move in moveset:
            m_type = moves_map.get(move)
            if m_type:
                move_types.append(m_type)
        
        # Calculate weaknesses
        weaknesses = get_weaknesses(types)

        pokemon_obj = {
            "name": species_name,
            "types": types,
            "recommended_moves": moveset,
            "move_types": move_types,
            "weaknesses": weaknesses,
            "rating": score,
            "speciesId": species_id # Keeping ID for reference
        }
        
        processed_data.append(pokemon_obj)

    print(f"Successfully processed {len(processed_data)} Pokemon.")
    return processed_data

if __name__ == "__main__":
    data = load_data()
    if data:
        print("Example entry:")
        print(data[0])
