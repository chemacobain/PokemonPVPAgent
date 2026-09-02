import { defineStore } from 'pinia'
import { fetchPokemon, fetchTopTeams, generateTeam, fetchAvailable } from '../api/pokemon'

export const useTeamStore = defineStore('team', {
  state: () => ({
    league: '1500',
    allPokemon: [],
    topTeams: [],
    availablePokemon: { raids: [], wild_spawns: [] },
    selectedPokemonIds: [],
    generatedResult: null,
    loading: {
      pokemon: false,
      topTeams: false,
      available: false,
      generating: false
    },
    error: null
  }),
  getters: {
    selectedPokemon: (state) => {
      return state.allPokemon.filter(p => state.selectedPokemonIds.includes(p.id || p.speciesId))
    },
    canGenerate: (state) => state.selectedPokemonIds.length >= 1,
    leagueName: (state) => {
      const names = {
        '1500': 'Liga Super (CP 1500)',
        '2500': 'Liga Ultra (CP 2500)',
        '10000': 'Liga Master (Sin Límite)'
      }
      return names[state.league] || state.league
    }
  },
  actions: {
    async setLeague(league) {
      this.league = league
      this.clearSelection()
      await Promise.all([this.fetchPokemon(), this.fetchTopTeams(), this.fetchAvailable()])
    },
    async fetchPokemon() {
      this.loading.pokemon = true
      this.error = null
      try {
        this.allPokemon = await fetchPokemon(this.league)
      } catch (e) {
        this.error = e.message
      } finally {
        this.loading.pokemon = false
      }
    },
    async fetchTopTeams() {
      this.loading.topTeams = true
      this.error = null
      try {
        this.topTeams = await fetchTopTeams(this.league)
      } catch (e) {
        this.error = e.message
      } finally {
        this.loading.topTeams = false
      }
    },
    async fetchAvailable() {
      this.loading.available = true
      try {
        this.availablePokemon = await fetchAvailable(this.league)
      } catch (e) {
        console.error(e)
      } finally {
        this.loading.available = false
      }
    },
    togglePokemonSelection(speciesId) {
      const index = this.selectedPokemonIds.indexOf(speciesId)
      if (index > -1) {
        this.selectedPokemonIds.splice(index, 1)
      } else if (this.selectedPokemonIds.length < 2) {
        this.selectedPokemonIds.push(speciesId)
      }
      this.generatedResult = null
    },
    async generateTeam() {
      this.loading.generating = true
      this.error = null
      try {
        this.generatedResult = await generateTeam(this.league, this.selectedPokemonIds)
      } catch (e) {
        this.error = e.message
      } finally {
        this.loading.generating = false
      }
    },
    clearSelection() {
      this.selectedPokemonIds = []
      this.generatedResult = null
    }
  }
})
