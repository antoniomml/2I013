from soccersimulator import Strategy, SoccerAction, Vector2D
from tools import *

#Estrategia de movimiento aleatorio
class EstrategiaAleatoria(Strategy):
    def __init__(self):
        Strategy.__init__(self, "Aleatoria")

    def compute_strategy(self, state, id_team, id_player):
        # id_team is 1 or 2
        # id_player starts at 0
        return SoccerAction(Vector2D.create_random(),
                            Vector2D.create_random())

#Estrategia de buscar el balon y tirar
class EstrategiaTirador(Strategy):
	def __init__(self):
		Strategy.__init__(self, "Tirador")

	def compute_strategy(self, state, id_team, id_player):
		s = SuperState(state,id_team,id_player)

		if s.player.distance(s.ball) > s.ballDistance:
			return ir_a(s.ball,s)
		else:
			return chutar(s)