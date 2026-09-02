<template>
  <div class="ai-commentary glass-card">
    <h4>💬 Comentarios del Entrenador (IA)</h4>
    <blockquote>
      {{ commentary }}
    </blockquote>
  </div>
</template>

<script setup>
defineProps({
  commentary: {
    type: String,
    required: true
  }
});
</script>

<style scoped>
.ai-commentary {
  padding: 20px;
  border-radius: 12px;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  margin: 20px 0;
}
h4 {
  margin: 0 0 12px 0;
  color: white;
}
blockquote {
  margin: 0;
  padding-left: 16px;
  border-left: 4px solid var(--accent, #6366f1);
  font-style: italic;
  font-size: 1.1rem;
  color: #e2e8f0;
  line-height: 1.5;
}
</style>
