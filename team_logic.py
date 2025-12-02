from data_loader import TYPE_CHART, ALL_TYPES

class TeamAnalyzer:
    def __init__(self):
        pass

    def evaluate_coverage(self, team_list):
        """
        Evaluates a team of 3 Pokemon.
        
        Args:
            team_list (list): List of 3 Pokemon dictionaries (as returned by data_loader).
            
        Returns:
            dict: Analysis results including shared weaknesses, offensive coverage gaps, and safety score.
        """
        if not team_list:
            return {"error": "Team is empty"}
        
        # 1. Shared Weaknesses
        weakness_counts = {}
        for pokemon in team_list:
            for weakness in pokemon.get("weaknesses", []):
                weakness_counts[weakness] = weakness_counts.get(weakness, 0) + 1
        
        shared_weaknesses = [w for w, count in weakness_counts.items() if count >= 2]
        
        # 2. Offensive Coverage
        # Determine which types the team can hit for super effective damage
        covered_types = set()
        
        # Collect all move types available in the team
        team_move_types = set()
        for pokemon in team_list:
            for m_type in pokemon.get("move_types", []):
                team_move_types.add(m_type)
        
        # For each move type, find what it is super effective against
        for move_type in team_move_types:
            move_type = move_type.lower()
            if move_type in TYPE_CHART:
                # Check what this move type hits super effectively (> 1.0)
                # TYPE_CHART[attacker][defender]
                for defender_type, multiplier in TYPE_CHART[move_type].items():
                    if multiplier > 1.0:
                        covered_types.add(defender_type)
        
        # Identify types that are NOT covered (i.e., we don't have super effective moves against them)
        uncovered_types = [t for t in ALL_TYPES if t not in covered_types]
        
        # 3. Safety Rating
        total_rating = sum(p.get("rating", 0) for p in team_list)
        safety_score = total_rating / len(team_list) if team_list else 0
        
        return {
            "shared_weaknesses": shared_weaknesses,
            "uncovered_types": uncovered_types,
            "safety_score": round(safety_score, 1),
            "team_size": len(team_list)
        }

    def suggest_teammate(self, current_team, all_pokemon, top_n=5):
        """
        Suggests the best teammates for the current team.
        
        Args:
            current_team (list): List of currently selected Pokemon objects.
            all_pokemon (list): List of all available Pokemon objects.
            top_n (int): Number of suggestions to return.
            
        Returns:
            list: List of suggested Pokemon objects with a 'match_score'.
        """
        if not current_team:
            # If no team, just return top rated pokemon
            return sorted(all_pokemon, key=lambda x: x.get("rating", 0), reverse=True)[:top_n]

        # Analyze current team weaknesses and gaps
        current_analysis = self.evaluate_coverage(current_team)
        current_weaknesses = set(current_analysis["shared_weaknesses"])
        current_uncovered = set(current_analysis["uncovered_types"])
        
        suggestions = []
        
        for candidate in all_pokemon:
            # Skip if already in team
            if any(p["speciesId"] == candidate["speciesId"] for p in current_team):
                continue
                
            # Skip if rating is too low (e.g. below 80) to ensure quality
            if candidate.get("rating", 0) < 80:
                continue

            score = 0
            
            # Bonus for high rating (0-100 points)
            score += candidate.get("rating", 0)
            
            # Penalty for sharing weaknesses with the team
            # If candidate is weak to something the team is already weak to (shared weakness), big penalty
            candidate_weaknesses = set(candidate.get("weaknesses", []))
            
            # Check if adding this candidate CREATES a new shared weakness or exacerbates an existing one
            # We simulate the new team
            new_team = current_team + [candidate]
            new_analysis = self.evaluate_coverage(new_team)
            new_shared_weaknesses = set(new_analysis["shared_weaknesses"])
            
            # Penalty for each shared weakness in the new team
            score -= len(new_shared_weaknesses) * 50 
            
            # Bonus for covering offensive gaps
            # Check if candidate's moves hit types that were previously uncovered
            candidate_move_types = set(candidate.get("move_types", []))
            covered_by_candidate = set()
            for m_type in candidate_move_types:
                if m_type in TYPE_CHART:
                    for defender, mult in TYPE_CHART[m_type].items():
                        if mult > 1.0:
                            covered_by_candidate.add(defender)
            
            # Intersection of what candidate covers and what was uncovered
            useful_coverage = covered_by_candidate.intersection(current_uncovered)
            score += len(useful_coverage) * 10
            
            # Bonus for resisting current team's weaknesses
            # If the team has a shared weakness, and this candidate RESISTS it, that's good.
            # (Resistance logic: if type chart says attacker -> candidate is < 1.0)
            # We need to check resistance against 'current_weaknesses' (which are types)
            # But 'current_weaknesses' from evaluate_coverage are types that >1 member is weak to.
            # Let's look at individual weaknesses of team members too? 
            # For simplicity, let's just look at the 'shared_weaknesses' identified.
            
            for weak_type in current_weaknesses:
                # Check if candidate resists 'weak_type'
                # weak_type attacking candidate
                multiplier = 1.0
                for t in candidate.get("types", []):
                    if weak_type in TYPE_CHART:
                         multiplier *= TYPE_CHART[weak_type].get(t, 1.0)
                
                if multiplier < 1.0:
                    score += 30 # Good synergy!
            
            candidate["match_score"] = score
            suggestions.append(candidate)
            
        # Sort by score descending
        suggestions.sort(key=lambda x: x["match_score"], reverse=True)
        return suggestions[:top_n]

if __name__ == "__main__":
    # Test with dummy data
    dummy_team = [
        {
            "name": "Registeel",
            "weaknesses": ["fire", "fighting", "ground"],
            "move_types": ["steel", "fighting", "electric"], # Lock On (Normal), Focus Blast (Fighting), Zap Cannon (Electric) - simplified
            "rating": 90
        },
        {
            "name": "Altaria",
            "weaknesses": ["ice", "rock", "dragon", "fairy"],
            "move_types": ["dragon", "flying", "fairy"], # Dragon Breath, Sky Attack, Moonblast
            "rating": 88
        },
        {
            "name": "Swampert",
            "weaknesses": ["grass"],
            "move_types": ["ground", "water", "poison"], # Mud Shot, Hydro Cannon, Sludge Wave
            "rating": 92
        }
    ]
    
    analyzer = TeamAnalyzer()
    results = analyzer.evaluate_coverage(dummy_team)
    print("Analysis Results:", results)
