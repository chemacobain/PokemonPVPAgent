import requests
import math
import re

# Cache for gamemaster to avoid re-fetching
_gamemaster_cache = None

def get_gamemaster():
    global _gamemaster_cache
    if not _gamemaster_cache:
        try:
            res = requests.get("https://raw.githubusercontent.com/pvpoke/pvpoke/master/src/data/gamemaster/pokemon.json")
            if res.status_code == 200:
                _gamemaster_cache = res.json()
        except Exception as e:
            print("Error fetching gamemaster:", e)
            return []
    return _gamemaster_cache

def normalize_name(display_name):
    name = display_name.lower().replace("'", "").replace(".", "")
    is_shadow = False
    is_mega = False
    mega_suffix = ""

    if name.startswith("shadow "):
        is_shadow = True
        name = name.replace("shadow ", "")

    if name.startswith("mega "):
        is_mega = True
        name = name.replace("mega ", "")
        if " x" in name:
            mega_suffix = "_mega_x"
            name = name.replace(" x", "")
        elif " y" in name:
            mega_suffix = "_mega_y"
            name = name.replace(" y", "")
        else:
            mega_suffix = "_mega"

    prefixes = {"alolan": "alolan", "galarian": "galarian", "hisuian": "hisuian", "paldean": "paldean"}
    form = ""
    for pref in prefixes:
        if name.startswith(pref + " "):
            form = "_" + prefixes[pref]
            name = name.replace(pref + " ", "")
            break

    match = re.search(r'\((.*?)\)', name)
    if match:
        form_in_parens = match.group(1).replace(" ", "_")
        name = re.sub(r'\s*\(.*?\)', '', name)
        form = "_" + form_in_parens

    name = name.strip().replace(" ", "_")
    species_id = name + form + mega_suffix
    if is_shadow:
        species_id += "_shadow"

    return species_id

def calc_hundo_cp(base_atk, base_def, base_hp, cpm=0.84029999):
    atk = base_atk + 15
    def_ = base_def + 15
    hp = base_hp + 15
    cp = math.floor((atk * math.sqrt(def_) * math.sqrt(hp) * (cpm ** 2)) / 10.0)
    return max(10, cp)

def get_available_pokemon(league, ranked_pokemon):
    gamemaster = get_gamemaster()
    gm_map = {p.get("speciesId"): p for p in (gamemaster or [])}
    ranked_map = {p.get("speciesId"): p for p in ranked_pokemon}

    # Fetch Raids
    raids_data = []
    try:
        res = requests.get("https://raw.githubusercontent.com/bigfoott/ScrapedDuck/data/raids.json", timeout=10)
        if res.status_code == 200:
            raids_data = res.json()
    except Exception as e:
        print("Error fetching raids:", e)

    # Fetch Events for spawns
    events_data = []
    try:
        res = requests.get("https://raw.githubusercontent.com/bigfoott/ScrapedDuck/data/events.json", timeout=10)
        if res.status_code == 200:
            events_data = res.json()
    except Exception as e:
        print("Error fetching events:", e)

    processed_raids = []
    processed_spawns = []

    # Process Raids
    for r in raids_data:
        d_name = r.get("name", "")
        s_id = normalize_name(d_name)
        gm_entry = gm_map.get(s_id) or gm_map.get(s_id.replace("_normal", ""))
        
        # Fallback if mega not ranked, find base species rating
        ranked_entry = ranked_map.get(s_id)
        if not ranked_entry and "mega" in s_id:
            base_id = s_id.split("_mega")[0]
            ranked_entry = ranked_map.get(base_id)

        cp_50 = 0
        if gm_entry and "baseStats" in gm_entry:
            stats = gm_entry["baseStats"]
            cp_50 = calc_hundo_cp(stats.get("atk", 0), stats.get("def", 0), stats.get("hp", 0))

        pvp_rating = ranked_entry.get("rating", 0) if ranked_entry else 0
        
        processed_raids.append({
            "name": d_name,
            "speciesId": s_id,
            "tier": r.get("tier", "Raid"),
            "types": [t.get("name", "none").lower() for t in r.get("types", [])],
            "image": r.get("image", ""),
            "canBeShiny": r.get("canBeShiny", False),
            "cp_raid_normal": r.get("combatPower", {}).get("normal", {}),
            "cp_raid_boosted": r.get("combatPower", {}).get("boosted", {}),
            "cp_hundo_50": cp_50,
            "pvp_rating": pvp_rating,
            "best_moves": ranked_entry.get("recommended_moves", []) if ranked_entry else [],
            "move_types": ranked_entry.get("move_types", []) if ranked_entry else []
        })

    # Process Spawns from events
    for e in events_data:
        extra = e.get("extraData")
        if not extra: continue
        
        # E.g. Spotlight Hour
        if "spotlight" in extra:
            s_name = extra["spotlight"].get("name", "")
            if s_name:
                s_id = normalize_name(s_name)
                gm_entry = gm_map.get(s_id)
                ranked_entry = ranked_map.get(s_id)
                
                cp_50 = 0
                if gm_entry and "baseStats" in gm_entry:
                    stats = gm_entry["baseStats"]
                    cp_50 = calc_hundo_cp(stats.get("atk", 0), stats.get("def", 0), stats.get("hp", 0))

                processed_spawns.append({
                    "name": s_name,
                    "speciesId": s_id,
                    "source": "Spotlight Hour",
                    "event_name": e.get("heading", ""),
                    "types": gm_entry.get("types", []) if gm_entry else [],
                    "image": e.get("image", ""),
                    "canBeShiny": extra["spotlight"].get("canBeShiny", False),
                    "cp_hundo_50": cp_50,
                    "pvp_rating": ranked_entry.get("rating", 0) if ranked_entry else 0,
                    "best_moves": ranked_entry.get("recommended_moves", []) if ranked_entry else [],
                    "move_types": ranked_entry.get("move_types", []) if ranked_entry else []
                })
        
        # E.g. Community Day
        if "communityday" in extra:
            s_name = extra["communityday"].get("name", "")
            if s_name:
                s_id = normalize_name(s_name)
                gm_entry = gm_map.get(s_id)
                ranked_entry = ranked_map.get(s_id)
                
                cp_50 = 0
                if gm_entry and "baseStats" in gm_entry:
                    stats = gm_entry["baseStats"]
                    cp_50 = calc_hundo_cp(stats.get("atk", 0), stats.get("def", 0), stats.get("hp", 0))

                processed_spawns.append({
                    "name": s_name,
                    "speciesId": s_id,
                    "source": "Community Day",
                    "event_name": e.get("heading", ""),
                    "types": gm_entry.get("types", []) if gm_entry else [],
                    "image": e.get("image", ""),
                    "canBeShiny": True,
                    "cp_hundo_50": cp_50,
                    "pvp_rating": ranked_entry.get("rating", 0) if ranked_entry else 0,
                    "best_moves": ranked_entry.get("recommended_moves", []) if ranked_entry else [],
                    "move_types": ranked_entry.get("move_types", []) if ranked_entry else []
                })
    
    # Sort by pvp_rating
    processed_raids.sort(key=lambda x: x["pvp_rating"], reverse=True)
    processed_spawns.sort(key=lambda x: x["pvp_rating"], reverse=True)

    return {
        "raids": processed_raids,
        "wild_spawns": processed_spawns
    }
