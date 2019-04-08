#! /usr/bin/python3

from Simulation import *
from soccersimulator import Strategy, SoccerAction, Vector2D, SoccerTeam
from soccersimulator import VolleySimulation, volley_show_simu
from MillaModule.tools import *
from MillaModule.actions import *

class soloStrategy(Strategy):
    def __init__(self,force=None):
        Strategy.__init__(self, "soloStrategy")
        self.force = force

    def compute_strategy(self, state, id_team, id_player):
        s = SuperState(state,id_team,id_player)
        pos = posCentral(s)
        if not s.peutToucher:
            if estDansMonTerrain(s):
                return allerA(s.ballonApprox,s)
            return allerA(pos,s)
        else:
            if jeDoisLancer(s):
                return lancerLoin(s)
            return avancerVolleyParam(s,self.force)

expe = GoalSearch(soloStrategy(),params={'force':[3,4,5,0]}) #max=6
expe.start(False) #expe.start(False) no muestra el partido
print(expe.get_res())
print(expe.get_best())