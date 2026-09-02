<template>
  <span class="type-badge" :style="{ backgroundColor: `var(--type-${typeName.toLowerCase()}, rgba(255, 255, 255, 0.25))` + '40', color: `var(--type-${typeName.toLowerCase()}, #fff)` }">
    <img :src="getIconUrl(typeName.toLowerCase())" :alt="typeName" class="type-icon" />
    <span class="type-name">{{ capitalizedName }}</span>
  </span>
</template>

<script setup>
import { computed } from 'vue';
import { getIconUrl } from '@/api/pokemon.js';

const props = defineProps({
  typeName: {
    type: String,
    required: true
  }
});

const capitalizedName = computed(() => {
  if (!props.typeName) return '';
  return props.typeName.charAt(0).toUpperCase() + props.typeName.slice(1).toLowerCase();
});
</script>

<style scoped>
.type-badge {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  padding: 4px 10px;
  border-radius: 9999px;
  font-size: 0.75rem;
  font-weight: 600;
  text-transform: capitalize;
  /* Basic fallback */
  background-color: rgba(255, 255, 255, 0.25);
  color: #fff;
}
.type-icon {
  width: 20px;
  height: 20px;
}
</style>
