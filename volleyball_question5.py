#! /usr/bin/python3

from soccersimulator import Strategy, SoccerAction, Vector2D, SoccerTeam
from soccersimulator import VolleySimulation, volley_show_simu
from MillaModule.tools import *
from MillaModule.actions import *

class Attaque(Strategy):
    def __init__(self):
        Strategy.__init__(self, "Attaque")

    def compute_strategy(self, state, id_team, id_player):
        s = SuperState(state,id_team,id_player)
        pos = posAttaque(s)
        if not s.peutToucher:
            if s.jeSuisProche and estDansMonTerrain(s):
                return allerA(s.ballonApprox,s)
            return allerA(pos,s)
        else:
            if jeDoisLancer(s):
                return lancerLoin(s)
            return avancerVolley(s)

class Defense(Strategy):
    def __init__(self):
        Strategy.__init__(self, "Defense")

    def compute_strategy(self, state, id_team, id_player):
    	s = SuperState(state,id_team,id_player)
    	pos =  posDefense(s)
    	if not s.peutToucher:
    		if s.jeSuisProche:
    			return allerA(s.ballonApprox,s)
    		return allerA(pos,s)
    	return lancerLoin(s)

# Create teams
team1 = SoccerTeam(name="Team 1")
team2 = SoccerTeam(name="Team 2")

# Add players
team1.add("Attaquant", Attaque())  # Attaque strategy
team1.add("Defenseur", Defense())  # Defense strategy
team2.add("Attaquant", Attaque())  # Attaque strategy
team2.add("Defenseur", Defense())  # Defense strategy

# Create a match
simu = VolleySimulation(team1, team2)

# Simulate and display the match
volley_show_simu(simu)