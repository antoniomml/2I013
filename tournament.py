from module.Estrategias import *
from soccersimulator import SoccerTeam

def get_team ( nb_players ):
	team = SoccerTeam(name = "Antonio Milla's Team")
	if nb_players == 1:
		team.add("Striker",EstrategiaTirador())
	if nb_players == 2:
		team.add("Striker",EstrategiaTirador())
		team.add("Random",EstrategiaAleatoria())
	return team

if __name__ == "__main__":
	from soccersimulator import Simulation, show_simu

	# Check teams with 1 player and 2 players
	team1 = get_team(1)
	team2 = get_team(2)

	# Create a match
	simu = Simulation(team1, team2)

	# Simulate and display the match
	show_simu(simu)