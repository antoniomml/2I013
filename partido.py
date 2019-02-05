from soccersimulator import SoccerTeam, Simulation, show_simu
from module.Estrategias import *

# Creacion de equipos
team1 = SoccerTeam(name="Real Madrid")
team2 = SoccerTeam(name="Barcelona")

# Creacion de jugadores
team1.add("Delantero 1", EstrategiaTirador())
team1.add("Quieto 1", Strategy())
team1.add("Portero 1", Portero())

team2.add("Delantero 2", EstrategiaTirador())
team2.add("Quieto 2", Strategy())
team2.add("Portero 2", Portero())

# Creacion del partido
simu = Simulation(team1, team2)

# Empezar simulacion
show_simu(simu)