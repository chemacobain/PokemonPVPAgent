<template>
  <div class="pokemon-search">
    <div class="selected-chips" v-if="selectedPokemon.length">
      <div v-for="p in selectedPokemon" :key="p.speciesId" class="chip">
        <img :src="getImageUrl(p.speciesId)" class="chip-img" />
        <span>{{ p.name }}</span>
        <button @click="toggleSelection(p.speciesId)" class="remove-btn">&times;</button>
      </div>
    </div>
    
    <div class="search-input-wrap">
      <input 
        type="text" 
        v-model="searchQuery" 
        placeholder="Buscar Pokémon..." 
        class="search-input"
        @focus="isFocused = true"
        @blur="handleBlur"
      />
    </div>

    <div v-if="isFocused && filteredResults.length" class="dropdown glass-card">
      <div 
        v-for="p in filteredResults" 
        :key="p.speciesId" 
        class="dropdown-item"
        @mousedown.prevent="toggleSelection(p.speciesId)"
      >
        <img :src="getImageUrl(p.speciesId)" class="item-img" />
        <div class="item-info">
          <span class="item-name">{{ p.name }}</span>
          <div class="item-types">
            <TypeBadge v-for="t in (p.types || []).filter(ty => ty.toLowerCase() !== 'none')" :key="t" :type-name="t" />
          </div>
        </div>
        <div class="item-rating">
          ⭐ {{ p.rating }}
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue';
import { useTeamStore } from '@/stores/teamStore';
import { getImageUrl } from '@/api/pokemon.js';
import TypeBadge from './TypeBadge.vue';

const teamStore = useTeamStore();
const searchQuery = ref('');
const isFocused = ref(false);

const selectedPokemon = computed(() => teamStore.selectedPokemon);

const filteredResults = computed(() => {
  let list = teamStore.allPokemon || [];
  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase();
    list = list.filter(p => p.name.toLowerCase().includes(query));
  } else {
    // Top rated if empty
    list = [...list].sort((a, b) => b.rating - a.rating);
  }
  return list.slice(0, 20);
});

const handleBlur = () => {
  setTimeout(() => {
    isFocused.value = false;
  }, 200);
};

const toggleSelection = (id) => {
  if (!teamStore.selectedPokemonIds.includes(id) && teamStore.selectedPokemonIds.length >= 2) {
    alert('Puedes seleccionar un máximo de 2 Pokémon.');
    return;
  }
  teamStore.togglePokemonSelection(id);
  searchQuery.value = '';
};
</script>

<style scoped>
.pokemon-search {
  position: relative;
  width: 100%;
  max-width: 500px;
  margin: 0 auto;
}
.selected-chips {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin-bottom: 12px;
}
.chip {
  display: flex;
  align-items: center;
  gap: 6px;
  background: rgba(255, 255, 255, 0.1);
  padding: 4px 12px 4px 4px;
  border-radius: 9999px;
  color: white;
  font-size: 0.9rem;
}
.chip-img {
  width: 24px;
  height: 24px;
  border-radius: 50%;
  background: rgba(0,0,0,0.2);
}
.remove-btn {
  background: transparent;
  border: none;
  color: #f87171;
  font-size: 1.2rem;
  cursor: pointer;
  line-height: 1;
}
.search-input {
  width: 100%;
  padding: 12px 16px;
  border-radius: 8px;
  border: 1px solid rgba(255, 255, 255, 0.2);
  background: rgba(255, 255, 255, 0.05);
  color: white;
  font-size: 1rem;
  outline: none;
}
.search-input:focus {
  border-color: var(--accent, #6366f1);
}
.dropdown {
  position: absolute;
  top: 100%;
  left: 0;
  right: 0;
  margin-top: 4px;
  max-height: 300px;
  overflow-y: auto;
  background: rgba(30, 30, 40, 0.95);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 8px;
  z-index: 10;
  backdrop-filter: blur(10px);
}
.dropdown-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 10px 16px;
  cursor: pointer;
  transition: background 0.2s;
}
.dropdown-item:hover {
  background: rgba(255, 255, 255, 0.1);
}
.item-img {
  width: 40px;
  height: 40px;
}
.item-info {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 4px;
}
.item-name {
  color: white;
  font-weight: bold;
}
.item-types {
  display: flex;
  gap: 4px;
  transform: scale(0.85);
  transform-origin: left center;
}
.item-rating {
  color: #facc15;
  font-weight: bold;
}
</style>
