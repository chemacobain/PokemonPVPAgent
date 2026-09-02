<template>
  <div class="app-wrapper">
    <header class="navbar">
      <div class="container navbar-content">
        <div class="logo">
          🏆 Agente PvP
        </div>
        <div class="league-info">
          <!-- League selection or info -->
        </div>
      </div>
    </header>
    <main class="main-content">
      <router-view />
    </main>
    <footer class="footer">
      <div class="container">
        <p>&copy; 2026 Agente PvP Pokémon GO. Todos los derechos reservados.</p>
      </div>
    </footer>
  </div>
</template>

<style scoped>
.app-wrapper {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
  background-color: #0f0f1a;
}

.navbar {
  position: sticky;
  top: 0;
  background-color: #1a1a2e;
  z-index: 100;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
}

.navbar-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  height: 60px;
}

.logo {
  font-family: 'Poppins', sans-serif;
  font-size: 1.5rem;
  font-weight: 700;
  background: linear-gradient(90deg, var(--accent, #e94560), var(--accent-hover, #ff6b81));
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.main-content {
  flex: 1;
  padding: 2rem 0;
}

.footer {
  background-color: var(--bg-secondary, #1a1a2e);
  padding: 1.5rem 0;
  text-align: center;
  border-top: 1px solid var(--border, #2a2a4a);
  color: var(--text-secondary, #a0a0b0);
}
</style>
