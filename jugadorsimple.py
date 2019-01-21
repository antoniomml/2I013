# coding: utf-8
from soccersimulator import Strategy, SoccerAction, Vector2D, SoccerTeam, Simulation, show_simu
from soccersimulator.settings import GAME_WIDTH, GAME_HEIGHT, PLAYER_RADIUS, BALL_RADIUS

class EstrategiaSimple(Strategy):
	def __init__(self):
		Strategy.__init__(self, "Simple")

	def compute_strategy(self, state, id_team, id_player):
		# id_team is 1 or 2
		# id_player starts at 0
		posJug = state.player_state(id_team,id_player).position
		posBal = state.ball.position

		But1 = Vector2D(0,GAME_HEIGHT/2.)
		But2 = Vector2D(GAME_WIDTH,GAME_HEIGHT/2.)
		DistanceBal = PLAYER_RADIUS+BALL_RADIUS

		if posJug.distance(posBal) > DistanceBal:
			return SoccerAction(posBal-posJug, 0.)
		else:
			if id_team == 1:
				return SoccerAction(But2-posJug,But2-posJug)
			else:
				return SoccerAction(But1-posJug, But1-posJug)

# Create teams
team1 = SoccerTeam(name="Real Madrid")
team2 = SoccerTeam(name="Barcelona")

# Add players
team1.add("Jugador Simple", EstrategiaSimple())  # Simple strategy
#team2.add("Jugador Estatico", Strategy())   # Static strategy
team2.add("Jugador Simple", EstrategiaSimple())

# Create a match
simu = Simulation(team1, team2)

# Simulate and display the match
show_simu(simu)
