<template>
  <div class="home-view">
    <section class="hero">
      <h1>🏆 Agente PvP: Constructor de Equipos</h1>
      <p>Construye el equipo perfecto de Pokémon GO PvP con inteligencia artificial</p>
    </section>

    <LeagueSelector />
    
    <AvailablePokemonSection />

    <TopTeamsSection />
    
    <hr class="divider" />
    
    <section class="team-builder">
      <h2>1. Selecciona tus Pokémon</h2>
      <PokemonSearch />
      
      <div class="action-row">
        <button 
          class="btn-primary" 
          :disabled="!teamStore.canGenerate || teamStore.loading.generating"
          @click="teamStore.generateTeam()"
        >
          {{ teamStore.loading.generating ? 'Generando...' : 'Generar Equipo Completo' }}
        </button>
      </div>
    </section>

    <section v-if="teamStore.generatedResult" class="result-section">
      <h2>2. Análisis y Sugerencia</h2>
      <div class="success-message">¡Equipo Generado!</div>
      
      <div class="generated-team">
        <PokemonCard 
          v-for="p in teamStore.generatedResult.team" 
          :key="p.speciesId" 
          :pokemon="p" 
          :role="p.role" 
        />
      </div>
      
      <SynergyMetrics :analysis="teamStore.generatedResult.analysis" />
      
      <WeaknessAlert 
        :weaknesses="teamStore.generatedResult.analysis.shared_weaknesses" 
        :uncovered-types="teamStore.generatedResult.analysis.uncovered_types" 
      />
      
      <AICommentary :commentary="teamStore.generatedResult.commentary" />
    </section>
  </div>
</template>

<script setup>
import { onMounted } from 'vue';
import { useTeamStore } from '@/stores/teamStore';
import LeagueSelector from '@/components/LeagueSelector.vue';
import AvailablePokemonSection from '@/components/AvailablePokemonSection.vue';
import TopTeamsSection from '@/components/TopTeamsSection.vue';
import PokemonSearch from '@/components/PokemonSearch.vue';
import PokemonCard from '@/components/PokemonCard.vue';
import SynergyMetrics from '@/components/SynergyMetrics.vue';
import WeaknessAlert from '@/components/WeaknessAlert.vue';
import AICommentary from '@/components/AICommentary.vue';

const teamStore = useTeamStore();

onMounted(() => {
  if (!teamStore.allPokemon || teamStore.allPokemon.length === 0) {
    teamStore.setLeague('1500');
  }
});
</script>

<style scoped>
.home-view {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
  color: white;
}
.hero {
  text-align: center;
  margin-bottom: 40px;
}
.hero h1 {
  font-size: 2.5rem;
  margin-bottom: 10px;
  background: linear-gradient(to right, #6366f1, #a855f7);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}
.hero p {
  font-size: 1.1rem;
  color: #ccc;
}
.divider {
  border: 0;
  height: 1px;
  background: rgba(255, 255, 255, 0.1);
  margin: 40px 0;
}
.team-builder h2, .result-section h2 {
  text-align: center;
  margin-bottom: 24px;
}
.action-row {
  display: flex;
  justify-content: center;
  margin-top: 24px;
}
.btn-primary {
  background: var(--accent, #6366f1);
  color: white;
  border: none;
  padding: 12px 24px;
  border-radius: 8px;
  font-size: 1.1rem;
  font-weight: bold;
  cursor: pointer;
  transition: opacity 0.2s;
}
.btn-primary:hover:not(:disabled) {
  opacity: 0.9;
}
.btn-primary:disabled {
  background: #4b5563;
  cursor: not-allowed;
  opacity: 0.7;
}
.result-section {
  margin-top: 40px;
}
.success-message {
  text-align: center;
  color: #4ade80;
  font-weight: bold;
  font-size: 1.2rem;
  margin-bottom: 24px;
}
.generated-team {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 24px;
  margin-bottom: 32px;
}
@media (max-width: 768px) {
  .generated-team {
    grid-template-columns: 1fr;
  }
}
</style>
