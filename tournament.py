
if __name__ == "__main__":
	from soccersimulator import Simulation, show_simu
	from MillaModule import *

	# Check teams with 1 player and 2 players
	team1 = get_team(1)
	team2 = get_team(1)

	# Create a match
	simu = Simulation(team1, team2)

	# Simulate and display the match
	show_simu(simu)