from soccersimulator import Strategy, SoccerAction, Vector2D
from module.tools import *
from module.actions import *

#Estrategia de movimiento aleatorio
class EstrategiaAleatoria(Strategy):
    def __init__(self):
        Strategy.__init__(self, "Aleatoria")

    def compute_strategy(self, state, id_team, id_player):
        # id_team is 1 or 2
        # id_player starts at 0
        return SoccerAction(Vector2D.create_random(),
                            Vector2D.create_random())

#Estrategia Simple (para prueba de acciones)
class EstrategiaSimple(Strategy):
    def __init__(self):
        Strategy.__init__(self, "Simple")

    def compute_strategy(self, state, id_team, id_player):
        s = SuperState(state,id_team,id_player)
        return allerA(Vector2D(15.,17.),s)

#Estrategia de buscar el balon y tirar
class EstrategiaTirador(Strategy):
    def __init__(self):
        Strategy.__init__(self, "Tirador")

    def compute_strategy(self, state, id_team, id_player):
        s = SuperState(state,id_team,id_player)
        if s.peutToucher:
            return tirer(0,s)
        else:
            return allerA(s.ballon,s)

#Estrategia de Portero
class Portero(Strategy):
    def __init__(self):
        Strategy.__init__(self,"Portero")
    
    def compute_strategy(self,state,id_team,id_player):
        s = SuperState(state,id_team,id_player)
        if s.peutToucher:
            if s.deboDespejar:
                return degager(s)
            else:
                return passer(s)
        else:
            return allerA(s.posGardien,s)

#Estrategia de Defensa
class Defensa(Strategy):
    def __init__(self):
        Strategy.__init__(self,"Defensa")

    def compute_strategy(self,state,id_team,id_player):
        s = SuperState(state,id_team,id_player)
        if s.peutToucher:
            if s.deboPasar:
                return passer(s)
            else:
                return avancer(s)
        else:
            if s.estProcheCoequipier:
                if s.meDesmarco:
                    return seDemarquer(s)
                else:
                    return allerA(s.posDefenseur,s)
            return allerA(s.posDefenseur,s)

#Estrategia de Delantero
class Delantero(Strategy):
    def __init__(self):
        Strategy.__init__(self,"Delantero")

    def compute_strategy(self,state,id_team,id_player):
        s = SuperState(state,id_team,id_player)
        if s.peutToucher:
            if s.deboChutar:
                return tirer(4,s) #Chuta con fuerza 4 por optimizacion
            else:
                if s.deboPasar:
                    return passer(s)
                else:
                    return avancer(s)
        else:
            if s.estProcheCoequipier:
                if s.meDesmarco:
                    return seDemarquer(s)
                else:
                    return allerA(s.posAttaquant,s)
            return allerA(s.posAttaquant,s)