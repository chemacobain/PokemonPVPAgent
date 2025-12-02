import streamlit as st
import data_loader
from data_loader import TYPE_ICONS
from team_logic import TeamAnalyzer
from ai_config import SYSTEM_PROMPT
import base64

# Helper to load SVG as base64
def get_svg_base64(file_path):
    try:
        with open(file_path, "r") as f:
            svg_data = f.read()
        b64_data = base64.b64encode(svg_data.encode("utf-8")).decode("utf-8")
        return f"data:image/svg+xml;base64,{b64_data}"
    except Exception:
        return ""

def render_type_with_icon(type_name):
    """Renders a type name with its icon inline."""
    icon_path = TYPE_ICONS.get(type_name.lower())
    if icon_path:
        icon_b64 = get_svg_base64(icon_path)
        if icon_b64:
            return f'<img src="{icon_b64}" width="20" style="vertical-align:middle; margin-right:5px;">{type_name.title()}'
    return type_name.title()

# Set page config
st.set_page_config(
    page_title="Agente PvP Pokémon GO",
    page_icon="🎮",
    layout="wide"
)

# Load data
@st.cache_data
def get_data(league_code):
    return data_loader.load_data(league_code)

# Title and Intro
st.title("🏆 Agente PvP: Constructor de Equipos")
st.markdown("""
**Bienvenido, Entrenador.**
Esta herramienta te ayudará a construir un equipo competitivo.
Selecciona tu liga, elige 1 o 2 Pokémon iniciales y deja que el agente sugiera el resto.
""")

# Sidebar for System Prompt (Brain) - HIDDEN
# with st.sidebar:
#     st.header("🧠 Cerebro del Agente")
#     st.info("Este es el System Prompt que guía la lógica del agente:")
#     st.code(SYSTEM_PROMPT, language="text")

# League Selector
league_map = {
    "Liga Super (CP 1500)": "1500",
    "Liga Ultra (CP 2500)": "2500",
    "Liga Master (Sin Límite)": "10000"
}
selected_league_name = st.selectbox("Selecciona la Liga:", list(league_map.keys()))
league_code = league_map[selected_league_name]

all_pokemon = get_data(league_code)
analyzer = TeamAnalyzer()

# Main Interface
# Layout: Vertical for better mobile responsiveness
st.subheader("1. Selecciona tus Pokémon")
pokemon_names = [p["name"] for p in all_pokemon]
selected_names = st.multiselect(
    "Elige 1 o 2 Pokémon:",
    options=pokemon_names,
    max_selections=2,
    help="Empieza con tu favorito o el núcleo de tu equipo."
)

selected_pokemon = [p for p in all_pokemon if p["name"] in selected_names]

generate_btn = st.button("Generar Equipo Completo", type="primary", disabled=len(selected_pokemon) == 0)

if generate_btn and selected_pokemon:
    st.divider()
    st.subheader("2. Análisis y Sugerencia")
    
    with st.spinner("Analizando el meta y buscando sinergias..."):
        # Suggest teammates
        current_team = selected_pokemon.copy()
        suggestions = []
        
        while len(current_team) < 3:
            # Find best teammate
            candidates = analyzer.suggest_teammate(current_team, all_pokemon, top_n=1)
            if candidates:
                best_pick = candidates[0]
                current_team.append(best_pick)
                suggestions.append(best_pick)
            else:
                st.warning("No se encontraron candidatos adecuados para completar el equipo.")
                break
        
        # Display the suggested team
        st.success("¡Equipo Generado!")
        
        def get_image_url(species_id):
            # Remove _shadow suffix
            if species_id.endswith("_shadow"):
                species_id = species_id[:-7]
            
            # Replace underscores with hyphens
            species_id = species_id.replace("_", "-")
            
            return f"https://img.pokemondb.net/sprites/home/normal/{species_id}.png"

        # Show the team cards
        cols = st.columns(3)
        for i, p in enumerate(current_team):
            role = "Lead" if i == 0 else ("Switch" if i == 1 else "Closer")
            with cols[i]:
                with st.container(border=True):
                    st.markdown(f"### {role}")
                    st.image(get_image_url(p['speciesId']), use_container_width=True)
                    

# ... (inside the loop)
                    # Name and Types with Icons
                    # Use HTML to display SVG icons inline
                    type_html = ""
                    for t, icon_path in zip(p['types'], p['type_icons']):
                        if icon_path:
                            icon_b64 = get_svg_base64(icon_path)
                            if icon_b64:
                                type_html += f'<img src="{icon_b64}" width="20" style="vertical-align:middle; margin-right:5px;">{t.title()} '
                            else:
                                type_html += f'{t.title()} '
                        else:
                            type_html += f'{t.title()} '
                            
                    st.markdown(f"**{p['name']}**")
                    st.markdown(type_html, unsafe_allow_html=True)
                    
                    st.caption(f"Rating: {p['rating']}")
                    
                    st.markdown("**Movimientos:**")
                    # Display moves with icons
                    for move_name, move_icon_path in zip(p['recommended_moves'], p['move_type_icons']):
                        if move_icon_path:
                            icon_b64 = get_svg_base64(move_icon_path)
                            if icon_b64:
                                st.markdown(f'<img src="{icon_b64}" width="15" style="vertical-align:middle; margin-right:5px;"> {move_name}', unsafe_allow_html=True)
                            else:
                                st.text(f"- {move_name}")
                        else:
                            st.text(f"- {move_name}")
        
        # Analyze the full team
        analysis = analyzer.evaluate_coverage(current_team)
        
        st.divider()
        
        # Display Analysis
        st.markdown("### 📊 Reporte de Sinergia")
        
        # Metrics
        m1, m2, m3 = st.columns(3)
        m1.metric("Puntaje de Seguridad", f"{analysis['safety_score']}/100")
        m2.metric("Debilidades Compartidas", len(analysis['shared_weaknesses']), delta_color="inverse")
        m3.metric("Tipos sin Cobertura", len(analysis['uncovered_types']), delta_color="inverse")
        
        # Detailed breakdown
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("#### ⚠️ Alertas de Debilidad")
            if analysis['shared_weaknesses']:
                for w in analysis['shared_weaknesses']:
                    st.markdown(f"El equipo es débil a: {render_type_with_icon(w)}", unsafe_allow_html=True)
            else:
                st.success("¡No hay debilidades compartidas graves!")
                
        with c2:
            st.markdown("#### ⚔️ Cobertura Ofensiva")
            if analysis['uncovered_types']:
                # st.warning(f"No tienes daño súper efectivo contra: {', '.join([t.upper() for t in analysis['uncovered_types']])}")
                st.markdown("No tienes daño súper efectivo contra:")
                cols = st.columns(3)
                for i, t in enumerate(analysis['uncovered_types']):
                    with cols[i % 3]:
                        st.markdown(render_type_with_icon(t), unsafe_allow_html=True)
            else:
                st.success("¡Cobertura ofensiva perfecta!")

        # AI Commentary (Simulated)
        st.divider()
        st.markdown("### 💬 Comentarios del Entrenador (IA)")
        
        commentary = f"""
        > "¡Excelente elección de base con **{', '.join(selected_names)}**!
        >
        > He añadido a **{', '.join([s['name'] for s in suggestions])}** para completar el trío.
        >
        > **¿Por qué?**
        > {suggestions[0]['name'] if suggestions else ''} aporta una cobertura clave y ayuda a mitigar las debilidades del equipo. 
        > Con un puntaje de seguridad de **{analysis['safety_score']}**, este equipo tiene un buen equilibrio para la Liga Super.
        >
        > **Estrategia:**
        > Usa a **{current_team[0]['name']}** como Lead para presionar escudos temprano. 
        > Si te encuentras en un mal matchup, **{current_team[1]['name']}** es tu cambio seguro.
        > Guarda a **{current_team[2]['name']}** para cerrar la partida cuando los escudos estén bajos."
        """
        st.info(commentary)

elif generate_btn and not selected_pokemon:
    st.error("Por favor selecciona al menos 1 Pokémon.")
