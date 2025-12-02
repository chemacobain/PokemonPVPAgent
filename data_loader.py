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

# Type Icons Mapping
# Using local SVG icons in assets/icons/
TYPE_ICONS = {
    "normal": "assets/icons/normal.svg",
    "fire": "assets/icons/fire.svg",
    "water": "assets/icons/water.svg",
    "grass": "assets/icons/grass.svg",
    "electric": "assets/icons/electric.svg",
    "ice": "assets/icons/ice.svg",
    "fighting": "assets/icons/fighting.svg",
    "poison": "assets/icons/poison.svg",
    "ground": "assets/icons/ground.svg",
    "flying": "assets/icons/flying.svg",
    "psychic": "assets/icons/psychic.svg",
    "bug": "assets/icons/bug.svg",
    "rock": "assets/icons/rock.svg",
    "ghost": "assets/icons/ghost.svg",
    "dragon": "assets/icons/dragon.svg",
    "dark": "assets/icons/dark.svg",
    "steel": "assets/icons/steel.svg",
    "fairy": "assets/icons/fairy.svg",
    "none": ""
}

# English to Spanish Move Translations (Partial list - expanded as needed)
MOVES_ES = {
    "TACKLE": "Placaje",
    "VINE_WHIP": "Látigo Cepa",
    "POWER_WHIP": "Latigazo",
    "SEED_BOMB": "Bomba Germen",
    "SLUDGE_BOMB": "Bomba Lodo",
    "AIR_SLASH": "Tajo Aéreo",
    "DRAGON_CLAW": "Garra Dragón",
    "SHADOW_CLAW": "Garra Umbría",
    "VOLT_SWITCH": "Voltiocambio",
    "ROCK_SLIDE": "Avalancha",
    "EARTHQUAKE": "Terremoto",
    "HYDRO_CANNON": "Hidrocañón",
    "FRENZY_PLANT": "Planta Feroz",
    "BLAST_BURN": "Anillo Ígneo",
    "COUNTER": "Contraataque",
    "MUD_SHOT": "Disparo Lodo",
    "BUBBLE": "Burbuja",
    "ICE_BEAM": "Rayo Hielo",
    "PLAY_ROUGH": "Carantoña",
    "FOUL_PLAY": "Juego Sucio",
    "THUNDER_SHOCK": "Impactrueno",
    "DISCHARGE": "Chispazo",
    "SKY_ATTACK": "Ataque Aéreo",
    "BRAVE_BIRD": "Pájaro Osado",
    "HURRICANE": "Vendaval",
    "WEATHER_BALL_ICE": "Meteorobola (Hielo)",
    "WEATHER_BALL_FIRE": "Meteorobola (Fuego)",
    "WEATHER_BALL_WATER": "Meteorobola (Agua)",
    "WEATHER_BALL_ROCK": "Meteorobola (Roca)",
    "WEATHER_BALL_NORMAL": "Meteorobola (Normal)",
    "BODY_SLAM": "Golpe Cuerpo",
    "NIGHT_SLASH": "Tajo Umbrío",
    "SCALD": "Escaldar",
    "SURF": "Surf",
    "DRILL_RUN": "Taladradora",
    "STONE_EDGE": "Roca Afilada",
    "FLAMETHROWER": "Lanzallamas",
    "MOONBLAST": "Fuerza Lunar",
    "PSYCHIC": "Psíquico",
    "FUTURE_SIGHT": "Premonición",
    "SHADOW_BALL": "Bola Sombra",
    "DARK_PULSE": "Pulso Umbrío",
    "DRAGON_BREATH": "Dragoaliento",
    "OUTRAGE": "Enfado",
    "CLOSE_COMBAT": "A Bocajarro",
    "SUPER_POWER": "Fuerza Bruta",
    "DYNAMIC_PUNCH": "Puño Dinámico",
    "FOCUS_BLAST": "Onda Certera",
    "SOLAR_BEAM": "Rayo Solar",
    "LEAF_BLADE": "Hoja Aguda",
    "X_SCISSOR": "Tijera X",
    "BUG_BUZZ": "Zumbido",
    "MEGAHORN": "Megacuerno",
    "POISON_JAB": "Puya Nociva",
    "ACID_SPRAY": "Bomba Ácida",
    "SLUDGE_WAVE": "Onda Tóxica",
    "EARTH_POWER": "Tierra Viva",
    "SAND_TOMB": "Bucle Arena",
    "ICY_WIND": "Viento Hielo",
    "AVALANCHE": "Alud",
    "ICICLE_SPEAR": "Carámbano",
    "ZAP_CANNON": "Electrocañón",
    "WILD_CHARGE": "Voltio Cruel",
    "THUNDERBOLT": "Rayo",
    "CHARM": "Encanto",
    "DAZZLING_GLEAM": "Brillo Mágico",
    "DISARMING_VOICE": "Voz Cautivadora",
    "LOCK_ON": "Fijar Blanco",
    "TRI_ATTACK": "Triataque",
    "PAYBACK": "Vendetta",
    "CRUNCH": "Triturar",
    "SNARL": "Alarido",
    "LICK": "Lengüetazo",
    "HEX": "Infortunio",
    "ASTONISH": "Impresionar",
    "CONFUSION": "Confusión",
    "PSYCHO_CUT": "Psicocorte",
    "ZEN_HEADBUTT": "Cabezazo Zen",
    "SMACK_DOWN": "Antiaéreo",
    "ROCK_THROW": "Lanzarrocas",
    "WING_ATTACK": "Ataque Ala",
    "STEEL_WING": "Ala de Acero",
    "METAL_CLAW": "Garra Metal",
    "BULLET_PUNCH": "Puño Bala",
    "FLASH_CANNON": "Foco Resplandor",
    "METEOR_MASH": "Puño Meteoro",
    "IRON_HEAD": "Cabeza de Hierro",
    "DRAGON_TAIL": "Cola Dragón",
    "INCINERATE": "Calcinación",
    "FIRE_SPIN": "Giro Fuego",
    "EMBER": "Ascuas",
    "WATER_GUN": "Pistola Agua",
    "WATERFALL": "Cascada",
    "RAZOR_LEAF": "Hoja Afilada",
    "BULLET_SEED": "Semilladora",
    "POISON_STING": "Picotazo Veneno",
    "MUD_SLAP": "Bofetón Lodo",
    "POWDER_SNOW": "Nieve Polvo",
    "ICE_SHARD": "Canto Helado",
    "FROST_BREATH": "Vaho Gélido",
    "THUNDER_FANG": "Colmillo Rayo",
    "ICE_FANG": "Colmillo Hielo",
    "FIRE_FANG": "Colmillo Ígneo",
    "SHADOW_SNEAK": "Sombra Vil",
    "OMINOUS_WIND": "Viento Aciago",
    "ANCIENT_POWER": "Poder Pasado",
    "AERIAL_ACE": "Golpe Aéreo",
    "DRILL_PECK": "Pico Taladro",
    "FLY": "Vuelo",
    "ICY_WIND": "Viento Hielo",
    "POLTERGEIST": "Poltergeist",
    "HIGH_HORSEPOWER": "Fuerza Equina",
    "TRAILBLAZE": "Abrecaminos",
    "BRUTAL_SWING": "Giro Vil",
    "LIQUIDATION": "Hidroariete",
    "LEAFAGE": "Follaje",
    "FAIRY_WIND": "Viento Feérico",
    "DOUBLE_KICK": "Doble Patada",
    "ROLLOUT": "Desenrollar",
    "SACRED_SWORD": "Espada Santa",
    "FUSION_FLARE": "Llama Fusión",
    "FUSION_BOLT": "Rayo Fusión",
    "SPACIAL_REND": "Corte Vacío",
    "ROAR_OF_TIME": "Distorsión",
    "MAGMA_STORM": "Lluvia Ígnea",
    "SANDSEAR_STORM": "Simún de Arena",
    "WILDBOLT_STORM": "Electrofurian",
    "BLEAKWIND_STORM": "Gélido Despertar",
    "SPRINGTIDE_STORM": "Ciclón Primavera",
    "NATURES_MADNESS": "Furia Natural",
    "DARK_VOID": "Brecha Negra",
    "SWIFT": "Rapidez",
    "HYPER_BEAM": "Hiperrayo",
    "RETURN": "Retribución",
    "FRUSTRATION": "Frustración"
}

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

def load_data(league="1500"):
    """
    Fetches ranking and gamemaster data, merges them, and returns a list of Pokemon dictionaries.
    
    Args:
        league (str): "1500" (Great), "2500" (Ultra), or "10000" (Master).
    """
    print(f"Fetching rankings data for league {league}...")
    
    # Validate league
    if league not in ["1500", "2500", "10000"]:
        league = "1500"
        
    rankings_url = f"https://raw.githubusercontent.com/pvpoke/pvpoke/master/src/data/rankings/all/overall/rankings-{league}.json"
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
        
        # Get move types and translated names
        move_types = []
        translated_moves = []
        move_type_icons = []
        
        for move in moveset:
            m_type = moves_map.get(move)
            if m_type:
                move_types.append(m_type)
                move_type_icons.append(TYPE_ICONS.get(m_type, ""))
            else:
                move_type_icons.append("")
            
            # Translate move name
            translated_name = MOVES_ES.get(move, move.replace("_", " ").title())
            translated_moves.append(translated_name)
        
        # Calculate weaknesses
        weaknesses = get_weaknesses(types)
        
        # Get type icons
        type_icons = [TYPE_ICONS.get(t, "") for t in types]

        pokemon_obj = {
            "name": species_name,
            "types": types,
            "type_icons": type_icons,
            "recommended_moves": translated_moves, # Use translated names for display
            "recommended_moves_raw": moveset, # Keep raw IDs if needed
            "move_types": move_types,
            "move_type_icons": move_type_icons,
            "weaknesses": weaknesses,
            "rating": score,
            "speciesId": species_id # Keeping ID for reference
        }
        
        processed_data.append(pokemon_obj)

    print(f"Successfully processed {len(processed_data)} Pokemon for league {league}.")
    return processed_data

if __name__ == "__main__":
    data = load_data()
    if data:
        print("Example entry:")
        print(data[0])
