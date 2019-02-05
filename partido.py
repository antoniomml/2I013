from soccersimulator import SoccerTeam, Simulation, show_simu
from module.Estrategias import *

# Creacion de equipos
team1 = SoccerTeam(name="Real Madrid")
team2 = SoccerTeam(name="Barcelona")

# Creacion de jugadores
team1.add("Gareth Bale", Delantero())
team1.add("Sergio Ramos", Defensa())
team1.add("Courtois", Portero())

team2.add("Lionel Messi", Delantero())
team2.add("Gerard Pique", Defensa())
team2.add("Ter Stegen", Portero())

# Creacion del partido
simu = Simulation(team1, team2)

# Empezar simulacion
show_simu(simu)