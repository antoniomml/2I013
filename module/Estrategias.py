from soccersimulator import Strategy, SoccerAction, Vector2D
from module.tools import *
from module.actions import *

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
        return allerA(Vector2D(15.,17.),s)

#Estrategia de buscar el balon y tirar
class StrategieFonceur(Strategy):
    def __init__(self):
        Strategy.__init__(self, "Tirador")

    def compute_strategy(self, state, id_team, id_player):
        s = SuperState(state,id_team,id_player)
        if s.peutToucher:
            return tirer(0,s)
        else:
            return allerA(s.ballon,s)

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