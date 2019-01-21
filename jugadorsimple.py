# coding: utf-8
from soccersimulator import Strategy, SoccerAction, Vector2D, SoccerTeam, Simulation, show_simu

class EstrategiaSimple(Strategy):
	def __init__(self):
		Strategy.__init__(self, "Random")

	def compute_strategy(self, state, id_team, id_player):
		# id_team is 1 or 2
		# id_player starts at 0
		posJug = state.player_state(id_team,id_player).position
		posBal = state.ball.position
		if (posJug.distance(posBal) > 1.65:
			return SoccerAction(posBal-posJug, posBal-posJug)
		else:
			return SoccerAction(Vector2D(1.,0.), Vector2D(1.,0.))

# Create teams
team1 = SoccerTeam(name="Real Madrid")
team2 = SoccerTeam(name="Barcelona")

# Add players
team1.add("Jugador Simple", EstrategiaSimple())  # Random strategy
team2.add("Jugador Estatico", Strategy())   # Static strategy

# Create a match
simu = Simulation(team1, team2)

# Simulate and display the match
show_simu(simu)
