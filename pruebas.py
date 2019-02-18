from Simulation import *
from soccersimulator import SoccerTeam, Simulation, show_simu
from soccersimulator.settings import GAME_WIDTH, GAME_HEIGHT, PLAYER_RADIUS, BALL_RADIUS, maxPlayerAcceleration, maxPlayerShoot
from MillaModule.Estrategias import *

class Tirador(Strategy):
    def __init__(self,strength=None):
        Strategy.__init__(self,"Go-getter")
        self.strength = strength

    def compute_strategy(self,state,id_team,id_player):
        s = SuperState(state,id_team,id_player)
        if s.peutToucher:
            return tirer(self.strength,s)
        else:
            return allerA(s.ballon,s)

class Pasador(Strategy):
    def __init__(self,strength=None):
        Strategy.__init__(self,"Go-getter")
        self.strength = strength

    def compute_strategy(self,state,id_team,id_player):
        s = SuperState(state,id_team,id_player)
        if s.peutToucher:
            return passer(self.strength,s)
        else:
            return allerA(s.ballon,s)

expe = GoalSearch(Tirador(),params={'strength':[3,4,5,0]}) #max=6
expe.start() #expe.start(False) no muestra el partido
print(expe.get_res())
print(expe.get_best())

#expe = BuscaPase(Pasador(),params={'strength':[0.1,0.5,0.75,1,2,3,4,5,0]}) #max=6
#expe.start() #expe.start(False) no muestra el partido
#print(expe.get_res())
#print(expe.get_best())