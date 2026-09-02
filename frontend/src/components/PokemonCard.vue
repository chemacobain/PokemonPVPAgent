<template>
  <div class="pokemon-card glass-card" :class="{ compact }">
    <div v-if="role" class="role-label" :class="roleClass">
      {{ role }}
    </div>
    <div class="image-container">
      <img :src="getImageUrl(pokemon.speciesId)" :alt="pokemon.name" class="pokemon-image" />
    </div>
    <h3 class="pokemon-name">{{ pokemon.name }}</h3>
    <div class="types">
      <TypeBadge 
        v-for="type in filteredTypes" 
        :key="type" 
        :type-name="type" 
      />
    </div>
    
    <div class="rating-section">
      <div class="rating-bar-container">
        <div class="rating-bar" :style="{ width: pokemon.rating + '%', backgroundColor: ratingColor }"></div>
      </div>
      <span class="rating-value" :style="{ color: ratingColor }">{{ pokemon.rating }}</span>
    </div>

    <div v-if="!compact && pokemon.recommended_moves?.length" class="moves-section">
      <h4>Movimientos</h4>
      <ul class="moves-list">
        <li v-for="(move, i) in pokemon.recommended_moves" :key="i" class="move-item">
          <img :src="getIconUrl(pokemon.move_types[i])" class="move-icon" />
          <span>{{ move }}</span>
        </li>
      </ul>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue';
import TypeBadge from './TypeBadge.vue';
import { getImageUrl, getIconUrl } from '@/api/pokemon.js';

const props = defineProps({
  pokemon: {
    type: Object,
    required: true
  },
  role: {
    type: String,
    default: null
  },
  compact: {
    type: Boolean,
    default: false
  }
});

const filteredTypes = computed(() => (props.pokemon.types || []).filter(t => t.toLowerCase() !== 'none'));

const roleClass = computed(() => {
  if (!props.role) return '';
  const r = props.role.toLowerCase();
  if (r === 'lead') return 'role-lead';
  if (r === 'switch') return 'role-switch';
  if (r === 'closer') return 'role-closer';
  return '';
});

const ratingColor = computed(() => {
  const r = props.pokemon.rating;
  if (r > 90) return '#4ade80';
  if (r > 80) return '#facc15';
  return '#f87171';
});
</script>

<style scoped>
.glass-card {
  background: rgba(255, 255, 255, 0.05);
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 12px;
  padding: 16px;
  position: relative;
  transition: transform 0.2s, box-shadow 0.2s;
  display: flex;
  flex-direction: column;
  align-items: center;
  color: white;
}

.glass-card:hover {
  transform: translateY(-4px) scale(1.02);
  box-shadow: 0 10px 20px rgba(0, 0, 0, 0.2), 0 0 15px rgba(255, 255, 255, 0.1);
}

.role-label {
  position: absolute;
  top: 0;
  left: 50%;
  transform: translate(-50%, -50%);
  padding: 4px 12px;
  border-radius: 9999px;
  font-size: 0.75rem;
  font-weight: bold;
  text-transform: uppercase;
}
.role-lead { background: #4ade80; color: #064e3b; }
.role-switch { background: #60a5fa; color: #1e3a8a; }
.role-closer { background: #f87171; color: #7f1d1d; }

.image-container {
  margin-bottom: 8px;
}
.pokemon-image {
  height: 120px;
  object-fit: contain;
}
.compact .pokemon-image {
  height: 80px;
}

.pokemon-name {
  font-size: 1.1rem;
  font-weight: bold;
  margin: 0 0 8px 0;
  text-align: center;
}

.types {
  display: flex;
  gap: 8px;
  margin-bottom: 12px;
}

.rating-section {
  width: 100%;
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 12px;
}
.rating-bar-container {
  flex: 1;
  background: rgba(255,255,255,0.1);
  height: 6px;
  border-radius: 3px;
  overflow: hidden;
}
.rating-bar {
  height: 100%;
  border-radius: 3px;
}
.rating-value {
  font-size: 0.85rem;
  font-weight: bold;
}

.moves-section {
  width: 100%;
  text-align: left;
}
.moves-section h4 {
  margin: 0 0 8px 0;
  font-size: 0.9rem;
  color: #ccc;
}
.moves-list {
  list-style: none;
  padding: 0;
  margin: 0;
  display: flex;
  flex-direction: column;
  gap: 6px;
}
.move-item {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 0.85rem;
}
.move-icon {
  width: 16px;
  height: 16px;
}
</style>
