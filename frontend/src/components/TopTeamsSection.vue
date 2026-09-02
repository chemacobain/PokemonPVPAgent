<template>
  <div class="top-teams-section">
    <h3>Top 5 equipos para esta liga</h3>
    <p class="subtitle">Equipos distintos construidos con el meta actual de PvPoke y sinergia de tipos.</p>
    
    <div v-if="teamStore.loading.topTeams" class="loading">
      Cargando top equipos...
    </div>
    
    <div v-else class="teams-list">
      <div 
        v-for="(teamItem, index) in teamStore.topTeams.slice(0,5)" 
        :key="index" 
        class="team-card glass-card"
        :class="{ expanded: expandedIndex === index }"
      >
        <div class="team-header" @click="toggleExpand(index)">
          <div class="header-info">
            <strong>Equipo {{ index + 1 }}</strong> · 
            {{ teamItem.pokemon.map(p => p.name).join(' · ') }} · 
            <span class="score">{{ teamItem.analysis?.safety_score || 0 }}/100</span>
          </div>
          <div class="expand-icon">{{ expandedIndex === index ? '▲' : '▼' }}</div>
        </div>
        
        <div v-if="expandedIndex === index" class="team-body">
          <div class="pokemon-row">
            <PokemonCard 
              v-for="(p, pIdx) in teamItem.pokemon" 
              :key="p.speciesId" 
              :pokemon="p" 
              :role="['Lead', 'Switch', 'Closer'][pIdx]" 
              compact 
            />
          </div>
          <SynergyMetrics v-if="teamItem.analysis" :analysis="teamItem.analysis" />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useTeamStore } from '@/stores/teamStore';
import PokemonCard from './PokemonCard.vue';
import SynergyMetrics from './SynergyMetrics.vue';

const teamStore = useTeamStore();
const expandedIndex = ref(0);

const toggleExpand = (index) => {
  expandedIndex.value = expandedIndex.value === index ? -1 : index;
};
</script>

<style scoped>
.top-teams-section {
  margin: 40px 0;
}
h3 {
  color: white;
  text-align: center;
  margin-bottom: 8px;
}
.subtitle {
  text-align: center;
  color: #ccc;
  margin-bottom: 20px;
}
.loading {
  text-align: center;
  color: #9ca3af;
  padding: 20px;
}
.teams-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}
.team-card {
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 12px;
  overflow: hidden;
  backdrop-filter: blur(10px);
}
.team-header {
  padding: 16px;
  cursor: pointer;
  display: flex;
  justify-content: space-between;
  align-items: center;
  color: white;
  transition: background 0.2s;
}
.team-header:hover {
  background: rgba(255, 255, 255, 0.1);
}
.score {
  color: #4ade80;
  font-weight: bold;
}
.team-body {
  padding: 16px;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
}
.pokemon-row {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 16px;
  margin-bottom: 20px;
}
@media (max-width: 768px) {
  .pokemon-row {
    grid-template-columns: 1fr;
  }
}
</style>
