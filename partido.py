#! /usr/bin/python3

from soccersimulator import SoccerTeam, Simulation, show_simu
from MillaModule.Estrategias import *

# Creacion de equipos
team1 = SoccerTeam(name="Real Madrid")
team2 = SoccerTeam(name="Barcelona")

# Creacion de jugadores
team1.add("Sergio Ramos", DefenseurStatique())
team1.add("Courtois", Gardien())
team1.add("Bale", AttaquantStatique())
team1.add("Benzema", MilieuStatique())

team2.add("Pique", Defenseur())
team2.add("Ter Stegen", Gardien())
team2.add("Suarez", AttaquantGauche())
team2.add("Messi", AttaquantDroit())

# Creacion del partido
simu = Simulation(team1, team2)

# Empezar simulacion
show_simu(simu)
