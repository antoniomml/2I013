# coding: utf-8
from soccersimulator import Strategy, SoccerAction, Vector2D, SoccerTeam, Simulation, show_simu
from tools import *
from Estrategias import *

# Creacion de equipos
team1 = SoccerTeam(name="Real Madrid")
team2 = SoccerTeam(name="Barcelona")

# Creacion de jugadores
team1.add("Jugador 1", EstrategiaTirador())
team2.add("Jugador 2", EstrategiaTirador())

# Creacion del partido
simu = Simulation(team1, team2)

# Empezar simulacion
show_simu(simu)