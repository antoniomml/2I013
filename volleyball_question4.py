#! /usr/bin/python3

from soccersimulator import Strategy, SoccerAction, Vector2D, SoccerTeam
from soccersimulator import VolleySimulation, volley_show_simu
from MillaModule.tools import *
from MillaModule.actions import *

class soloStrategy(Strategy):
    def __init__(self):
        Strategy.__init__(self, "soloStrategy")

    def compute_strategy(self, state, id_team, id_player):
        s = SuperState(state,id_team,id_player)
        pos = posCentral(s)
        if not s.peutToucher:
            if estDansMonTerrain(s):
                return allerA(s.ballonApprox,s)
            return allerA(pos,s)
        return lancerLoin(s)

# Create teams
team1 = SoccerTeam(name="Team 1")
team2 = SoccerTeam(name="Team 2")

# Add players
team1.add("Player 1", soloStrategy())  # Solo Strategy
team2.add("Player 2", soloStrategy())  # Solo Strategy


# Create a match
simu = VolleySimulation(team1, team2)

# Simulate and display the match
volley_show_simu(simu)