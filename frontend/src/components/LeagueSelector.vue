<template>
  <div class="league-selector">
    <button 
      class="league-btn" 
      :class="{ active: teamStore.league === '1500' }"
      @click="teamStore.setLeague('1500')"
    >
      ⭐ Liga Super
    </button>
    <button 
      class="league-btn" 
      :class="{ active: teamStore.league === '2500' }"
      @click="teamStore.setLeague('2500')"
    >
      💎 Liga Ultra
    </button>
    <button 
      class="league-btn" 
      :class="{ active: teamStore.league === '10000' }"
      @click="teamStore.setLeague('10000')"
    >
      👑 Liga Master
    </button>
  </div>
</template>

<script setup>
import { useTeamStore } from '@/stores/teamStore';

const teamStore = useTeamStore();
</script>

<style scoped>
.league-selector {
  display: flex;
  justify-content: center;
  gap: 12px;
  margin: 20px 0;
}
.league-btn {
  background: rgba(255, 255, 255, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.2);
  color: white;
  padding: 8px 16px;
  border-radius: 9999px;
  cursor: pointer;
  font-weight: 600;
  transition: all 0.2s;
  backdrop-filter: blur(5px);
}
.league-btn:hover {
  background: rgba(255, 255, 255, 0.2);
}
.league-btn.active {
  background: var(--accent, #6366f1);
  border-color: var(--accent, #6366f1);
}
</style>
