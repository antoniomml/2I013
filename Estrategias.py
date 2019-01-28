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
		if can_shoot(s):
			return chutar(s)
		else:
			return ir_a(s.ball,s)

#Estrategia Simple (para prueba de acciones)
class EstrategiaSimple(Strategy):
    def __init__(self):
        Strategy.__init__(self, "Simple")

    def compute_strategy(self, state, id_team, id_player):
        s = SuperState(state,id_team,id_player)
        return ir_a(Vector2D(15.,17.),s)

#Estrategia de Portero
class Portero(Strategy):
    def __init__(self):
        Strategy.__init__(self,"Portero")
    
    def compute_strategy(self,state,id_team,id_player):
        s = SuperState(state,id_team,id_player)
        if can_shoot(s):
            return chutar(s)
        else:
            return ir_a(s.posPortero,s)
