from module.Estrategias import *
from soccersimulator import SoccerTeam

def get_team ( nb_players ):
	team = SoccerTeam(name = "Antonio Milla's Team")
	if nb_players == 1:
		team.add("Attaquant",Attaquant())
	if nb_players == 2:
		team.add("Attaquant",Attaquant())
		team.add("Gardien",Gardien())
	if nb_players == 3:
		team.add("Attaquant",Attaquant())
		team.add("Gardien",Gardien())
		team.add("Defenseur",Defenseur())

	return team

if __name__ == "__main__":
	from soccersimulator import Simulation, show_simu

	# Check teams with 1 player and 2 players
	team1 = get_team(2)
	team2 = get_team(2)

	# Create a match
	simu = Simulation(team1, team2)

	# Simulate and display the match
	show_simu(simu)