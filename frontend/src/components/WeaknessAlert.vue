<template>
  <div class="weakness-alert">
    <div class="alert-section glass-card">
      <h4>⚠️ Alertas de Debilidad</h4>
      <div v-if="weaknesses && weaknesses.length > 0" class="badges-wrap">
        <p>El equipo es débil a:</p>
        <div class="badges">
          <TypeBadge v-for="w in weaknesses" :key="w" :type-name="w" />
        </div>
      </div>
      <div v-else class="success-msg">
        ¡No hay debilidades compartidas graves!
      </div>
    </div>
    
    <div class="alert-section glass-card">
      <h4>⚔️ Cobertura Ofensiva</h4>
      <div v-if="uncoveredTypes && uncoveredTypes.length > 0" class="badges-wrap">
        <p>No tienes daño súper efectivo contra:</p>
        <div class="badges">
          <TypeBadge v-for="t in uncoveredTypes" :key="t" :type-name="t" />
        </div>
      </div>
      <div v-else class="success-msg">
        ¡Cobertura ofensiva perfecta!
      </div>
    </div>
  </div>
</template>

<script setup>
import TypeBadge from './TypeBadge.vue';

defineProps({
  weaknesses: {
    type: Array,
    default: () => []
  },
  uncoveredTypes: {
    type: Array,
    default: () => []
  }
});
</script>

<style scoped>
.weakness-alert {
  display: flex;
  gap: 16px;
  margin: 20px 0;
}
@media (max-width: 768px) {
  .weakness-alert {
    flex-direction: column;
  }
}
.alert-section {
  flex: 1;
  padding: 16px;
  border-radius: 12px;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
}
h4 {
  margin: 0 0 12px 0;
  color: white;
}
p {
  margin: 0 0 8px 0;
  font-size: 0.9rem;
  color: #ccc;
}
.badges {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}
.success-msg {
  color: #4ade80;
  font-weight: bold;
}
</style>
