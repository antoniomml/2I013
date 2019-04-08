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
    def __init__(self,accion):
        Strategy.__init__(self, "Simple")
        self.accion = accion

    def compute_strategy(self, state, id_team, id_player):
        s = SuperState(state,id_team,id_player)
        if self.accion == "right":
            punto = Vector2D(s.joueurPos.x+1,s.joueurPos.y)
        elif self.accion == "left":
            punto = Vector2D(s.joueurPos.x-1,s.joueurPos.y)
        elif self.accion == "up":
            punto = Vector2D(s.joueurPos.x,s.joueurPos.y+1)
        elif self.accion == "down":
            punto = Vector2D(s.joueurPos.x,s.joueurPos.y-1)
        return SoccerAction(punto-s.joueurPos,punto-s.joueurPos)

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
        pos = s.posFonceur
        if not s.peutToucher:
            if s.estProcheCoequipier:
                if s.meDemarque:
                    return seDemarquer(s)
            return allerA(pos,s)
        else:
            if s.jeDoisTirer:
                return tirer(4,s) #Chuta con fuerza 4 por optimizacion
            elif s.autrePeutTirer:
                return tirer(maxPlayerShoot,s)
            elif s.jeDoisPasserAMoi:
                return passerAToi(s)
            elif jeDoisPasser(pos,s):
                return passer(s)
            elif s.autreEstDevant:
                return avancer(s)
            else:
                return avancerVersBut(s)

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
            if s.jeDoisSortir:
                return allerA(s.ballonApprox,s)
            return allerA(s.posGardien,s)

#Estrategia de Defensa
class Defenseur(Strategy):
    def __init__(self):
        Strategy.__init__(self,"Defenseur")

    def compute_strategy(self,state,id_team,id_player):
        s = SuperState(state,id_team,id_player)
        pos = s.posDefenseur
        if not s.peutToucher:
            if s.jeDoisSortir:
                return allerA(s.ballonApprox,s)
            elif s.estProcheCoequipier:
                if s.meDemarque:
                    return seDemarquer(s)
            return allerA(pos,s)
        else:
            if not jeSuisEnPos(pos,s) and s.autreEstDevant:
                return passer(s)
            if s.jeDoisTirer:
                return tirer(4,s) #Chuta con fuerza 4 por optimizacion
            elif s.autrePeutTirer:
                return tirer(maxPlayerShoot,s)
            elif s.jeDoisPasserAMoi:
                return passerAToi(s)
            elif jeDoisPasser(pos,s):
                return passer(s)
            elif s.autreEstDevant:
                return avancer(s)
            else:
                return avancerVersBut(s)

#Estrategia de Delantero Solitario
class Attaquant(Strategy):
    def __init__(self):
        Strategy.__init__(self,"Attaquant")

    def compute_strategy(self,state,id_team,id_player):
        s = SuperState(state,id_team,id_player)
        pos = s.posAttaquant
        if not s.peutToucher:
            if s.estProcheCoequipier:
                if s.meDemarque:
                    return seDemarquer(s)
            return allerA(pos,s)
        else:
            if s.jeDoisTirer:
                return tirer(4,s) #Chuta con fuerza 4 por optimizacion
            elif s.autrePeutTirer:
                return tirer(maxPlayerShoot,s)
            elif s.jeDoisPasserAMoi:
                return passerAToi(s)
            elif jeDoisPasser(pos,s):
                return passer(s)
            elif s.autreEstDevant:
                return avancer(s)
            else:
                return avancerVersBut(s)

#Estrategia de Delantero Derecho
class AttaquantDroit(Strategy):
    def __init__(self):
        Strategy.__init__(self,"AttaquantDroit")

    def compute_strategy(self,state,id_team,id_player):
        s = SuperState(state,id_team,id_player)
        pos = s.posAttaquantDroit
        if not s.peutToucher:
            if s.estProcheCoequipier:
                if s.meDemarque:
                    return seDemarquer(s)
            return allerA(pos,s)
        else:
            if s.jeDoisTirer:
                return tirer(4,s) #Chuta con fuerza 4 por optimizacion
            elif s.autrePeutTirer:
                return tirer(maxPlayerShoot,s)
            elif s.jeDoisPasserAMoi:
                return passerAToi(s)
            elif jeDoisPasser(pos,s):
                return passer(s)
            elif s.autreEstDevant:
                return avancer(s)
            else:
                return avancerVersBut(s)

#Estrategia de Delantero Izquierdo
class AttaquantGauche(Strategy):
    def __init__(self):
        Strategy.__init__(self,"AttaquantGauche")

    def compute_strategy(self,state,id_team,id_player):
        s = SuperState(state,id_team,id_player)
        pos = s.posAttaquantGauche
        if not s.peutToucher:
            if s.estProcheCoequipier:
                if s.meDemarque:
                    return seDemarquer(s)
            return allerA(pos,s)
        else:
            if s.jeDoisTirer:
                return tirer(4,s) #Chuta con fuerza 4 por optimizacion
            elif s.autrePeutTirer:
                return tirer(maxPlayerShoot,s)
            elif s.jeDoisPasserAMoi:
                return passerAToi(s)
            elif jeDoisPasser(pos,s):
                return passer(s)
            elif s.autreEstDevant:
                return avancer(s)
            else:
                return avancerVersBut(s)

class AttaquantStatique(Strategy):
    def __init__(self):
        Strategy.__init__(self,"AttaquantStatique")

    def compute_strategy(self,state,id_team,id_player):
        s = SuperState(state,id_team,id_player)
        pos = s.posAttaquantStatique
        if s.ballon == Vector2D(75,45):
            if not s.peutToucher:
                return allerA(s.ballonApprox,s)
            else:
                return tirer(maxPlayerShoot,s)
        if not s.peutToucher:
            if s.jeSuisProche:
                return allerA(s.ballonApprox,s)
            return allerA(pos,s)
        else:
            if s.jeDoisTirer:
                return tirer(4,s)
            elif s.autrePeutTirer:
                return tirer(maxPlayerShoot,s)
            elif jeDoisPasser(pos,s):
                return passer(s)
            elif s.jeDoisPasserAMoi:
                return passerAToi(s)
            elif s.autreEstDevant:
                return avancer(s)
            else:
                return avancerVersBut(s)

class MilieuStatique(Strategy):
    def __init__(self):
        Strategy.__init__(self,"MilieuStatique")

    def compute_strategy(self,state,id_team,id_player):
        s = SuperState(state,id_team,id_player)
        pos = s.posMilieuStatique
        if s.ballon == Vector2D(75,45):
            if not s.peutToucher:
                return allerA(s.ballonApprox,s)
            else:
                return tirer(maxPlayerShoot,s)
        if not s.peutToucher:
            if s.jeSuisProche:
                return allerA(s.ballonApprox,s)
            return allerA(pos,s)
        else:
            if s.jeDoisTirer:
                return tirer(4,s)
            elif s.autrePeutTirer:
                return tirer(maxPlayerShoot,s)
            elif jeDoisPasser(pos,s):
                return passer(s)
            elif s.jeDoisPasserAMoi:
                return passerAToi(s)
            elif s.autreEstDevant:
                return avancer(s)
            else:
                return avancerVersBut(s)

class DefenseurStatique(Strategy):
    def __init__(self):
        Strategy.__init__(self,"DefenseurStatique")

    def compute_strategy(self,state,id_team,id_player):
        s = SuperState(state,id_team,id_player)
        pos = s.posDefenseurStatique
        if not s.peutToucher:
            if s.jeSuisProche:
                return allerA(s.ballonApprox,s)
            return allerA(pos,s)
        else:
            if s.jeDoisTirer:
                return tirer(4,s)
            elif s.autrePeutTirer:
                return tirer(maxPlayerShoot,s)
            elif jeDoisPasser(pos,s):
                return passer(s)
            elif s.jeDoisPasserAMoi:
                return passerAToi(s)
            elif s.autreEstDevant:
                return avancer(s)
            else:
                return avancerVersBut(s)