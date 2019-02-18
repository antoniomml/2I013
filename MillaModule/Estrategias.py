from soccersimulator import Strategy, SoccerAction, Vector2D
from MillaModule.tools import *
from MillaModule.actions import *
from soccersimulator.settings import GAME_WIDTH, GAME_HEIGHT, PLAYER_RADIUS, BALL_RADIUS, maxPlayerAcceleration, maxPlayerShoot

#Estrategia de movimiento aleatorio
class StrategieAleatoire(Strategy):
    def __init__(self):
        Strategy.__init__(self, "Aleatoria")

    def compute_strategy(self, state, id_team, id_player):
        # id_team is 1 or 2
        # id_player starts at 0
        return SoccerAction(Vector2D.create_random(),
                            Vector2D.create_random())

#Estrategia Simple (para prueba de acciones)
class StrategieSimple(Strategy):
    def __init__(self):
        Strategy.__init__(self, "Simple")

    def compute_strategy(self, state, id_team, id_player):
        s = SuperState(state,id_team,id_player)
        punto = Vector2D(75.,50.)
        if s.peutToucher:
            return lancerA(punto,s)
        else:
            return allerA(s.ballonApprox,s)

#Estrategia de buscar el balon y tirar
class StrategieFonceur(Strategy):
    def __init__(self):
        Strategy.__init__(self, "Tirador")

    def compute_strategy(self, state, id_team, id_player):
        s = SuperState(state,id_team,id_player)
        if s.peutToucher:
            return tirer(maxPlayerShoot,s)
        else:
            return allerA(s.ballon,s)

#Estrategia de Tirador Mejorado
class FonceurAmeliore(Strategy):
    def __init__(self):
        Strategy.__init__(self,"Fonceur Ameliore")

    def compute_strategy(self,state,id_team,id_player):
        s = SuperState(state,id_team,id_player)
        if s.peutToucher:
            if s.jeDoisTirer:
                return tirer(4,s) #Chuta con fuerza 4 por optimizacion
            else:
                if s.autrePeutTirer:
                    return tirer(maxPlayerShoot,s)
                else:
                    return avancer(s)
        else:
            return allerA(s.posFonceur,s)

#Estrategia de Portero
class Gardien(Strategy):
    def __init__(self):
        Strategy.__init__(self,"Gardien")
    
    def compute_strategy(self,state,id_team,id_player):
        s = SuperState(state,id_team,id_player)
        if s.peutToucher:
            if s.jeDoisDegager:
                return degager(s)
            else:
                return passer(s)
        else:
            return allerA(s.posGardien,s)

#Estrategia de Defensa
class Defenseur(Strategy):
    def __init__(self):
        Strategy.__init__(self,"Defenseur")

    def compute_strategy(self,state,id_team,id_player):
        s = SuperState(state,id_team,id_player)
        if s.peutToucher:
            if s.autrePeutTirer:
                return tirer(maxPlayerShoot,s)
            if s.jeDoisPasser:
                return passer(s)
            else:
                return avancer(s)
        else:
            if s.estProcheCoequipier:
                if s.meDemarque:
                    return seDemarquer(s)
                else:
                    return allerA(s.posDefenseur,s)
            return allerA(s.posDefenseur,s)

#Estrategia de Delantero
class Attaquant(Strategy):
    def __init__(self):
        Strategy.__init__(self,"Attaquant")

    def compute_strategy(self,state,id_team,id_player):
        s = SuperState(state,id_team,id_player)
        if s.peutToucher:
            if s.jeDoisTirer:
                return tirer(4,s) #Chuta con fuerza 4 por optimizacion
            else:
                if s.autrePeutTirer:
                    return tirer(maxPlayerShoot,s)
                if s.jeDoisPasser:
                    return passer(s)
                else:
                    return avancer(s)
        else:
            if s.estProcheCoequipier:
                if s.meDemarque:
                    return seDemarquer(s)
                else:
                    return allerA(s.posAttaquant,s)
            return allerA(s.posAttaquant,s)