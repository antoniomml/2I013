from .tools import *
from .Estrategias import *
from soccersimulator import SoccerTeam

__version__ = '0.3'
__project__ = 'projetfoot'

def get_team ( nb_players ):
	team = SoccerTeam(name = "Antonio Milla's Team")
	if nb_players == 1:
		team.add("Fonceur",FonceurAmeliore())
	if nb_players == 2:
		team.add("Fonceur",FonceurAmeliore())
		team.add("Gardien",Gardien())
	if nb_players == 3:
		team.add("Attaquant",Attaquant())
		team.add("Gardien",Gardien())
		team.add("Defenseur",Defenseur())

	return team