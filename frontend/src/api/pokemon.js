export async function fetchPokemon(league) {
  const response = await fetch(`/api/pokemon/${league}`)
  if (!response.ok) throw new Error('Failed to fetch Pokemon')
  return response.json()
}

export async function fetchTopTeams(league) {
  const response = await fetch(`/api/teams/top/${league}`)
  if (!response.ok) throw new Error('Failed to fetch top teams')
  return response.json()
}

export async function fetchAvailable(league) {
  const response = await fetch(`/api/available/${league}`)
  if (!response.ok) throw new Error('Failed to fetch available Pokemon')
  return response.json()
}

export async function generateTeam(league, selectedIds) {
  const response = await fetch('/api/teams/generate', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ league, selected_ids: selectedIds })
  })
  if (!response.ok) throw new Error('Failed to generate team')
  return response.json()
}

export function getIconUrl(typeName) {
  return `/api/icons/${typeName}`
}

export function getImageUrl(speciesId) {
  const id = speciesId.replace(/_shadow$/, '').replace(/_/g, '-')
  return `https://img.pokemondb.net/sprites/home/normal/${id}.png`
}
