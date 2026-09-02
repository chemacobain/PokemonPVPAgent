<template>
  <div class="synergy-metrics">
    <div class="metric-card glass-card">
      <div class="icon-wrap">🛡️</div>
      <div class="metric-info">
        <span class="label">Puntaje de Seguridad</span>
        <span class="value" :style="{ color: safetyColor }">{{ analysis.safety_score }}</span>
      </div>
    </div>
    
    <div class="metric-card glass-card">
      <div class="icon-wrap">⚠️</div>
      <div class="metric-info">
        <span class="label">Debilidades Compartidas</span>
        <span class="value" :style="{ color: weaknessesColor }">{{ analysis.shared_weaknesses?.length || 0 }}</span>
      </div>
    </div>
    
    <div class="metric-card glass-card">
      <div class="icon-wrap">🎯</div>
      <div class="metric-info">
        <span class="label">Tipos sin Cobertura</span>
        <span class="value" :style="{ color: coverageColor }">{{ analysis.uncovered_types?.length || 0 }}</span>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue';

const props = defineProps({
  analysis: {
    type: Object,
    required: true
  }
});

const safetyColor = computed(() => {
  const score = props.analysis.safety_score || 0;
  if (score > 80) return '#4ade80';
  if (score > 60) return '#facc15';
  return '#f87171';
});

const weaknessesColor = computed(() => {
  const count = props.analysis.shared_weaknesses?.length || 0;
  return count > 0 ? '#f87171' : '#4ade80';
});

const coverageColor = computed(() => {
  const count = props.analysis.uncovered_types?.length || 0;
  return count > 0 ? '#f87171' : '#4ade80';
});
</script>

<style scoped>
.synergy-metrics {
  display: flex;
  gap: 16px;
  justify-content: space-between;
  margin: 20px 0;
}
@media (max-width: 768px) {
  .synergy-metrics {
    flex-direction: column;
  }
}
.metric-card {
  flex: 1;
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 16px;
  border-radius: 12px;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
}
.icon-wrap {
  font-size: 2rem;
}
.metric-info {
  display: flex;
  flex-direction: column;
}
.label {
  font-size: 0.85rem;
  color: #ccc;
}
.value {
  font-size: 1.5rem;
  font-weight: bold;
}
</style>
