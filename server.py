import os
from flask import Flask, jsonify, request, send_from_directory, abort
from flask_cors import CORS
from data_loader import load_data, TYPE_ICONS
from team_logic import TeamAnalyzer
from ai_config import SYSTEM_PROMPT
from current_pokemon import get_available_pokemon

app = Flask(__name__, static_folder='frontend/dist', static_url_path='')
# CORS is mainly for local Vite development. In production, they share origin.
CORS(app)

# In-memory cache
pokemon_cache = {}
top_teams_cache = {}
available_cache = {}
analyzer = TeamAnalyzer()

VALID_LEAGUES = ['1500', '2500', '10000']

@app.route('/api/pokemon/<league>', methods=['GET'])
def get_pokemon(league):
    if league not in VALID_LEAGUES:
        abort(400, description="Invalid league")
        
    if league not in pokemon_cache:
        data = load_data(league)
        pokemon_cache[league] = data
    return jsonify(pokemon_cache[league])

@app.route('/api/available/<league>', methods=['GET'])
def get_available(league):
    if league not in VALID_LEAGUES:
        abort(400, description="Invalid league")
        
    if league not in pokemon_cache:
        pokemon_cache[league] = load_data(league)
        
    if league not in available_cache:
        data = get_available_pokemon(league, pokemon_cache[league])
        if len(data.get('raids', [])) > 0 or len(data.get('wild_spawns', [])) > 0:
            available_cache[league] = data
        else:
            return jsonify(data) # return empty but don't cache
        
    return jsonify(available_cache[league])

@app.route('/api/teams/top/<league>', methods=['GET'])
def get_top_teams(league):
    if league not in VALID_LEAGUES:
        abort(400, description="Invalid league")
        
    if league not in top_teams_cache:
        if league not in pokemon_cache:
            pokemon_cache[league] = load_data(league)
        
        all_pokemon = pokemon_cache[league]
        top_teams = analyzer.suggest_top_teams(all_pokemon, 5)
        
        formatted_teams = []
        for team_info in top_teams:
            if isinstance(team_info, tuple) and len(team_info) == 3:
                team, score, analysis = team_info
                formatted_teams.append({
                    "pokemon": team,
                    "analysis": analysis,
                    "score": score
                })
            elif isinstance(team_info, dict):
                formatted_teams.append(team_info)
                
        top_teams_cache[league] = formatted_teams
        
    return jsonify(top_teams_cache[league])

@app.route('/api/teams/generate', methods=['POST'])
def generate_team():
    data = request.json or {}
    league = str(data.get('league', '1500'))
    selected_ids = data.get('selected_ids', [])
    
    if league not in VALID_LEAGUES:
        return jsonify({'error': 'Liga inválida'}), 400
        
    if not isinstance(selected_ids, list) or len(selected_ids) > 3:
        return jsonify({'error': 'IDs de selección inválidos'}), 400

    if league not in pokemon_cache:
        pokemon_cache[league] = load_data(league)

    all_pokemon = pokemon_cache[league]

    # Filter selected pokemon by speciesId
    selected_pokemon = [p for p in all_pokemon if p.get('speciesId') in selected_ids]

    if not selected_pokemon:
        return jsonify({'error': 'No se encontraron Pokémon válidos'}), 400

    current_team = list(selected_pokemon)
    suggestions = []

    while len(current_team) < 3:
        candidates = analyzer.suggest_teammate(current_team, all_pokemon, top_n=1)
        if candidates:
            best_pick = candidates[0]
            current_team.append(best_pick)
            suggestions.append(best_pick)
        else:
            break

    analysis = analyzer.evaluate_coverage(current_team)

    # Assign roles
    roles = ['Lead', 'Switch', 'Closer']
    team_with_roles = []
    for i, p in enumerate(current_team):
        p_copy = dict(p)
        p_copy['role'] = roles[i] if i < len(roles) else 'Flex'
        team_with_roles.append(p_copy)

    # Generate commentary in Spanish
    selected_names = [p['name'] for p in selected_pokemon]
    suggestion_names = [s['name'] for s in suggestions]

    commentary = f"¡Excelente elección de base con {', '.join(selected_names)}! "
    if suggestion_names:
        commentary += f"He añadido a {', '.join(suggestion_names)} para completar el trío. "
    if suggestions:
        commentary += f"{suggestions[0]['name']} aporta una cobertura clave y ayuda a mitigar las debilidades del equipo. "
    commentary += f"Con un puntaje de seguridad de {analysis['safety_score']}, este equipo tiene un buen equilibrio. "
    commentary += f"Usa a {current_team[0]['name']} como Lead para presionar escudos temprano. "
    if len(current_team) > 1:
        commentary += f"Si te encuentras en un mal matchup, {current_team[1]['name']} es tu cambio seguro. "
    if len(current_team) > 2:
        commentary += f"Guarda a {current_team[2]['name']} para cerrar la partida cuando los escudos estén bajos."

    return jsonify({
        "team": team_with_roles,
        "analysis": analysis,
        "suggestions": suggestions,
        "commentary": commentary
    })

@app.route('/api/icons/<type_name>', methods=['GET'])
def get_icon(type_name):
    import re
    # Sanitize type_name (only allow alphanumeric chars)
    sanitized_type = re.sub(r'[^a-zA-Z0-9]', '', type_name)
    return send_from_directory('assets/icons', f"{sanitized_type}.svg")

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    if path != "" and os.path.exists(app.static_folder + '/' + path):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, 'index.html')

if __name__ == '__main__':
    # Use environment port for deployment, default to 8080 locally
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port, debug=False)
