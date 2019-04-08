#! /usr/bin/python3

from soccersimulator import Strategy, SoccerAction, Vector2D, SoccerTeam
from soccersimulator import VolleySimulation, volley_show_simu
from MillaModule.tools import *
from MillaModule.actions import *

class Echauffement(Strategy):
    def __init__(self):
        Strategy.__init__(self, "Echauffement")

    def compute_strategy(self, state, id_team, id_player):
    	s = SuperState(state,id_team,id_player)
    	if not s.peutToucher:
    		return allerA(s.ballonApprox,s)
    	return passerAuContraire(s)

# Create teams
team1 = SoccerTeam(name="Team 1")
team2 = SoccerTeam(name="Team 2")

# Add players
team1.add("Player 1", Echauffement())  # Echauffement strategy
team2.add("Player 2", Echauffement())   # Echauffement strategy

# Create a match
simu = VolleySimulation(team1, team2)

# Simulate and display the match
volley_show_simu(simu)