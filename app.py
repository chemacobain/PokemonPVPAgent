import streamlit as st
import data_loader
from team_logic import TeamAnalyzer
from ai_config import SYSTEM_PROMPT

# Set page config
st.set_page_config(
    page_title="Agente PvP Pokémon GO",
    page_icon="🎮",
    layout="wide"
)

# Load data
@st.cache_data
def get_data():
    return data_loader.load_data()

all_pokemon = get_data()
analyzer = TeamAnalyzer()

# Title and Intro
st.title("🏆 Agente PvP: Constructor de Equipos (Liga Super)")
st.markdown("""
**Bienvenido, Entrenador.**
Esta herramienta te ayudará a construir un equipo competitivo para la Liga Super (CP 1500).
Selecciona 1 o 2 Pokémon iniciales y deja que el agente sugiera el resto basándose en la sinergia y el meta actual.
""")

# Sidebar for System Prompt (Brain) - HIDDEN
# with st.sidebar:
#     st.header("🧠 Cerebro del Agente")
#     st.info("Este es el System Prompt que guía la lógica del agente:")
#     st.code(SYSTEM_PROMPT, language="text")

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
                    st.markdown(f"**{p['name']}**")
                    st.caption(f"Tipos: {', '.join(p['types'])}")
                    st.caption(f"Rating: {p['rating']}")
                    st.markdown("**Movimientos:**")
                    for move in p['recommended_moves']:
                        st.text(f"- {move}")
        
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
                    st.error(f"El equipo es débil a: **{w.upper()}**")
            else:
                st.success("¡No hay debilidades compartidas graves!")
                
        with c2:
            st.markdown("#### ⚔️ Cobertura Ofensiva")
            if analysis['uncovered_types']:
                st.warning(f"No tienes daño súper efectivo contra: {', '.join([t.upper() for t in analysis['uncovered_types']])}")
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
