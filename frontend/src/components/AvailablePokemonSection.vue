<template>
  <section class="available-section glass-card">
    <div class="section-header">
      <h2>🎯 Pokémon Disponibles Esta Semana</h2>
      <div class="tabs">
        <button 
          :class="['tab-btn', { active: activeTab === 'raids' }]"
          @click="activeTab = 'raids'"
        >
          ⚔️ Raids
        </button>
        <button 
          :class="['tab-btn', { active: activeTab === 'wild' }]"
          @click="activeTab = 'wild'"
        >
          🌿 Salvajes/Eventos
        </button>
      </div>
    </div>

    <div v-if="teamStore.loading.available" class="loading-state">
      <div class="spinner"></div>
      <p>Buscando Pokémon disponibles...</p>
    </div>
    
    <div v-else class="tab-content">
      <!-- Raids Tab -->
      <div v-if="activeTab === 'raids'" class="pokemon-list">
        <div v-if="teamStore.availablePokemon.raids.length === 0" class="empty-state">
          No hay información de raids disponible en este momento.
        </div>
        <div 
          v-for="p in teamStore.availablePokemon.raids" 
          :key="p.speciesId" 
          class="avail-card"
          :class="{ 'meta-card': p.pvp_rating >= 85 }"
        >
          <div class="card-left">
            <img :src="p.image || getImageUrl(p.speciesId)" :alt="p.name" class="pkm-image" @error="handleImageError" />
            <div class="shiny-badge" v-if="p.canBeShiny">✨</div>
          </div>
          <div class="card-content">
            <div class="card-header">
              <h3 class="pkm-name">{{ p.name }}</h3>
              <span class="source-badge">{{ p.tier }}</span>
              <span v-if="p.pvp_rating >= 85" class="meta-badge">Meta 🔥</span>
            </div>
            
            <div class="types-row">
              <TypeBadge v-for="t in p.types" :key="t" :type="t" />
            </div>

            <div class="stats-grid">
              <div class="stat-col">
                <span class="stat-label">Rating PvP ({{ teamStore.leagueName }})</span>
                <div class="rating-bar-container">
                  <div 
                    class="rating-bar" 
                    :style="{ 
                      width: `${p.pvp_rating || 0}%`, 
                      backgroundColor: getRatingColor(p.pvp_rating) 
                    }"
                  ></div>
                </div>
                <span class="stat-value">{{ p.pvp_rating ? p.pvp_rating.toFixed(1) : 'N/A' }}</span>
              </div>
              
              <div class="stat-col cp-info">
                <div class="cp-row" v-if="p.cp_raid_normal?.min">
                  <span class="cp-label">CP Raid:</span>
                  <span class="cp-val">{{ p.cp_raid_normal.min }} - {{ p.cp_raid_normal.max }}</span>
                </div>
                <div class="cp-row" v-if="p.cp_raid_boosted?.min">
                  <span class="cp-label">Raid Boosted:</span>
                  <span class="cp-val">{{ p.cp_raid_boosted.min }} - {{ p.cp_raid_boosted.max }}</span>
                </div>
                <div class="cp-row hundo">
                  <span class="cp-label">💯 Hundo Lvl 50:</span>
                  <span class="cp-val">{{ p.cp_hundo_50 }}</span>
                </div>
              </div>
            </div>

            <div class="moves-section" v-if="p.best_moves && p.best_moves.length > 0">
              <span class="moves-label">Mejores Ataques:</span>
              <div class="moves-list">
                <span class="move-pill fast-move">
                  <img :src="getIconUrl(p.move_types[0])" class="move-icon" alt="" />
                  {{ p.best_moves[0] }}
                </span>
                <span class="move-pill charged-move" v-for="(move, i) in p.best_moves.slice(1)" :key="move">
                  <img :src="getIconUrl(p.move_types[i+1])" class="move-icon" alt="" />
                  {{ move }}
                </span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Wild / Events Tab -->
      <div v-if="activeTab === 'wild'" class="pokemon-list">
        <div v-if="teamStore.availablePokemon.wild_spawns.length === 0" class="empty-state">
          No hay eventos con spawns destacados activos.
        </div>
        <div 
          v-for="p in teamStore.availablePokemon.wild_spawns" 
          :key="p.speciesId" 
          class="avail-card"
          :class="{ 'meta-card': p.pvp_rating >= 85 }"
        >
          <div class="card-left">
            <img :src="p.image || getImageUrl(p.speciesId)" :alt="p.name" class="pkm-image" @error="handleImageError" />
            <div class="shiny-badge" v-if="p.canBeShiny">✨</div>
          </div>
          <div class="card-content">
            <div class="card-header">
              <h3 class="pkm-name">{{ p.name }}</h3>
              <span class="source-badge event-badge">{{ p.source }}: {{ p.event_name }}</span>
              <span v-if="p.pvp_rating >= 85" class="meta-badge">Meta 🔥</span>
            </div>
            
            <div class="types-row">
              <TypeBadge v-for="t in p.types" :key="t" :type="t" />
            </div>

            <div class="stats-grid">
              <div class="stat-col">
                <span class="stat-label">Rating PvP ({{ teamStore.leagueName }})</span>
                <div class="rating-bar-container">
                  <div 
                    class="rating-bar" 
                    :style="{ 
                      width: `${p.pvp_rating || 0}%`, 
                      backgroundColor: getRatingColor(p.pvp_rating) 
                    }"
                  ></div>
                </div>
                <span class="stat-value">{{ p.pvp_rating ? p.pvp_rating.toFixed(1) : 'N/A' }}</span>
              </div>
              
              <div class="stat-col cp-info">
                <div class="cp-row hundo">
                  <span class="cp-label">💯 Hundo Lvl 50:</span>
                  <span class="cp-val">{{ p.cp_hundo_50 }}</span>
                </div>
              </div>
            </div>

            <div class="moves-section" v-if="p.best_moves && p.best_moves.length > 0">
              <span class="moves-label">Mejores Ataques:</span>
              <div class="moves-list">
                <span class="move-pill fast-move">
                  <img :src="getIconUrl(p.move_types[0])" class="move-icon" alt="" />
                  {{ p.best_moves[0] }}
                </span>
                <span class="move-pill charged-move" v-for="(move, i) in p.best_moves.slice(1)" :key="move">
                  <img :src="getIconUrl(p.move_types[i+1])" class="move-icon" alt="" />
                  {{ move }}
                </span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
import { ref } from 'vue'
import { useTeamStore } from '@/stores/teamStore'
import { getImageUrl, getIconUrl } from '@/api/pokemon'
import TypeBadge from '@/components/TypeBadge.vue'

const teamStore = useTeamStore()
const activeTab = ref('raids')

const getRatingColor = (rating) => {
  if (!rating) return '#666';
  if (rating >= 90) return '#4ade80';
  if (rating >= 80) return '#facc15';
  return '#f87171';
}

const handleImageError = (e) => {
  // If LeekDuck image fails, fallback to our generated URL or a placeholder
  if (!e.target.src.includes('img.pokemondb.net')) {
    e.target.src = '/assets/placeholder.png'; // Make sure you have one, or just hide it
  }
}
</script>

<style scoped>
.available-section {
  margin-bottom: 2rem;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 1rem;
  margin-bottom: 1.5rem;
  padding-bottom: 1rem;
  border-bottom: 1px solid var(--border);
}

.section-header h2 {
  margin: 0;
  font-size: 1.3rem;
  color: var(--text-primary);
}

.tabs {
  display: flex;
  gap: 0.5rem;
  background: rgba(0, 0, 0, 0.2);
  padding: 0.3rem;
  border-radius: 20px;
}

.tab-btn {
  background: transparent;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 16px;
  color: var(--text-secondary);
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
}

.tab-btn:hover {
  color: var(--text-primary);
}

.tab-btn.active {
  background: var(--surface);
  color: var(--accent);
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
}

.pokemon-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.avail-card {
  display: flex;
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid var(--border);
  border-radius: 12px;
  overflow: hidden;
  transition: transform 0.2s, border-color 0.2s;
}

.avail-card:hover {
  transform: translateY(-2px);
  border-color: rgba(255, 255, 255, 0.2);
}

.meta-card {
  border-color: rgba(233, 69, 96, 0.3);
  background: linear-gradient(to right, rgba(233, 69, 96, 0.05), rgba(255, 255, 255, 0.02));
}

.card-left {
  position: relative;
  width: 100px;
  min-width: 100px;
  background: rgba(0, 0, 0, 0.2);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 0.5rem;
}

.pkm-image {
  width: 100%;
  height: auto;
  object-fit: contain;
  filter: drop-shadow(0 4px 6px rgba(0,0,0,0.4));
}

.shiny-badge {
  position: absolute;
  top: 5px;
  left: 5px;
  font-size: 1.2rem;
  filter: drop-shadow(0 0 2px rgba(255, 255, 255, 0.8));
}

.card-content {
  flex: 1;
  padding: 1rem;
  display: flex;
  flex-direction: column;
  gap: 0.8rem;
}

.card-header {
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  gap: 0.8rem;
}

.pkm-name {
  margin: 0;
  font-size: 1.2rem;
  font-weight: 600;
  color: var(--text-primary);
}

.source-badge {
  background: rgba(255, 255, 255, 0.1);
  padding: 0.2rem 0.6rem;
  border-radius: 12px;
  font-size: 0.75rem;
  font-weight: 600;
  color: var(--text-secondary);
}

.event-badge {
  background: rgba(74, 222, 128, 0.15);
  color: #4ade80;
}

.meta-badge {
  background: rgba(233, 69, 96, 0.2);
  color: var(--accent);
  padding: 0.2rem 0.6rem;
  border-radius: 12px;
  font-size: 0.75rem;
  font-weight: 700;
}

.types-row {
  display: flex;
  gap: 0.5rem;
}

.stats-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
  background: rgba(0, 0, 0, 0.15);
  padding: 0.8rem;
  border-radius: 8px;
}

.stat-col {
  display: flex;
  flex-direction: column;
  gap: 0.4rem;
}

.stat-label, .cp-label {
  font-size: 0.75rem;
  color: var(--text-secondary);
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.rating-bar-container {
  height: 6px;
  background-color: rgba(255, 255, 255, 0.1);
  border-radius: 3px;
  overflow: hidden;
}

.rating-bar {
  height: 100%;
  border-radius: 3px;
  transition: width 0.3s ease;
}

.stat-value {
  font-size: 0.9rem;
  font-weight: 600;
}

.cp-info {
  gap: 0.2rem;
}

.cp-row {
  display: flex;
  justify-content: space-between;
  font-size: 0.85rem;
}

.cp-val {
  font-family: monospace;
  font-weight: 600;
  color: var(--text-primary);
}

.cp-row.hundo .cp-val {
  color: #facc15;
}

.moves-section {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.moves-label {
  font-size: 0.8rem;
  color: var(--text-secondary);
}

.moves-list {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
}

.move-pill {
  display: flex;
  align-items: center;
  gap: 0.3rem;
  padding: 0.25rem 0.6rem;
  border-radius: 12px;
  font-size: 0.8rem;
  font-weight: 500;
  background: rgba(255, 255, 255, 0.05);
}

.fast-move {
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.charged-move {
  background: rgba(255, 255, 255, 0.1);
}

.move-icon {
  width: 14px;
  height: 14px;
}

.empty-state {
  text-align: center;
  padding: 2rem;
  color: var(--text-secondary);
  font-style: italic;
  background: rgba(0, 0, 0, 0.1);
  border-radius: 8px;
}

.loading-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 3rem;
  gap: 1rem;
  color: var(--text-secondary);
}

.spinner {
  width: 30px;
  height: 30px;
  border: 3px solid rgba(255, 255, 255, 0.1);
  border-top-color: var(--accent);
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

@media (max-width: 600px) {
  .avail-card {
    flex-direction: column;
  }
  .card-left {
    width: 100%;
    height: 120px;
  }
  .pkm-image {
    height: 100%;
    width: auto;
  }
  .stats-grid {
    grid-template-columns: 1fr;
  }
}
</style>
