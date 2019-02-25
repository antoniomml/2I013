from soccersimulator import Vector2D, SoccerAction
from soccersimulator.settings import GAME_WIDTH, GAME_HEIGHT, PLAYER_RADIUS, BALL_RADIUS, maxPlayerAcceleration, maxPlayerShoot
from MillaModule.actions import *

class SuperState(object):
    def __init__(self,state,id_team,id_player):
        self.state = state
        self.id_team = id_team
        self.id_player = id_player
        self.joueur = state.player_state(id_team,id_player)
    
    @property #Posicion de la pelota
    def ballon(self):
        return self.state.ball.position

    @property #Posicion del jugador que ejecuta la estrategia
    def joueurPos(self):
        return self.state.player_state(self.id_team,self.id_player).position

    @property #Posicion de la porteria contraria
    def but(self):
        if self.id_team == 1:
            return Vector2D(GAME_WIDTH,GAME_HEIGHT/2.)
        if self.id_team == 2:
            return Vector2D(0,GAME_HEIGHT/2.)

    @property #Distancia desde la que se puede tocar el balon
    def minDistanceBallon(self):
        return PLAYER_RADIUS+BALL_RADIUS

    @property #Devuelve si puede tocar el balon
    def peutToucher(self):
        if self.joueurPos.distance(self.ballon) > self.minDistanceBallon:
            return False
        else:
            return True
    
    @property #Id del equipo enemigo
    def equipeEnnemi(self):
        if self.id_team == 1:
            return 2
        if self.id_team == 2:
            return 1
    
    @property #Lista de los id del equipo enemigo
    def listeEnnemi(self):
        liste = []
        for idteam, idplayer in self.state.players:
            if idteam == self.equipeEnnemi:
                liste.append(idplayer)
        return liste

    @property #Lista de los id del equipo actual
    def listeEquipe(self):
        liste = []
        for idteam, idplayer in self.state.players:
            if idteam == self.id_team:
                liste.append(idplayer)
        return liste

    @property #Posicion donde estará la pelota segun su velocidad
    def ballonApprox(self):
        return self.ballon + 5 * self.state.ball.vitesse

    @property
    def posFonceur(self):
        if self.nbCoequipiers == 1:
            return self.ballonApprox
        if self.id_team == 1:
            if self.ballon.x < 40:
                return Vector2D(40.,self.ballonApprox.y)
            else:
                return self.ballonApprox
        if self.id_team == 2:
            if self.ballon.x > GAME_WIDTH-40.:
                return Vector2D(GAME_WIDTH-40.,self.ballonApprox.y)
            else:
                return self.ballonApprox

    @property #Posicion donde debe estar el portero
    def posGardien(self):
        if self.id_team == 1:
            if self.ballon.y > 60.:
                if self.ballon.x < 5.:
                    return Vector2D(self.ballonApprox.x,60.)
                return Vector2D(5.,60.)
            if self.ballon.y < 30.:
                if self.ballon.x < 5.:
                    return Vector2D(self.ballonApprox.x,30.)
                return Vector2D(5.,30.)
            if self.ballon.x < 10.:
                return self.ballonApprox
            return Vector2D(10.,self.ballonApprox.y)
        if self.id_team == 2:
            if self.ballon.y > 60.:
                if self.ballon.x > GAME_WIDTH-5.:
                    return Vector2D(self.ballonApprox.x,60.)
                return Vector2D(GAME_WIDTH-5.,60.)
            if self.ballon.y < 30.:
                if self.ballon.x > GAME_WIDTH-5.:
                    return Vector2D(self.ballonApprox.x,30.)
                return Vector2D(GAME_WIDTH-5.,30.)
            if self.ballon.x > GAME_WIDTH-10.:
                return self.ballonApprox
            return Vector2D(GAME_WIDTH-10.,self.ballonApprox.y)

    @property #Posicion donde debe estar el defensa
    def posDefenseur(self):
        if self.id_team == 1:
            if self.ballon.x > 70:
                return Vector2D(70.,self.ballonApprox.y)
            return self.ballonApprox
        if self.id_team == 2:
            if self.ballon.x < 80.:
                return Vector2D(80.,self.ballonApprox.y)
            return self.ballonApprox
    
    @property #Posicion donde debe estar el delantero
    def posAttaquant(self):
        if self.nbCoequipiers == 1:
            return self.ballonApprox
        if self.id_team == 1:
            if self.ballon.x < 45.:
                return Vector2D(45.,self.ballonApprox.y)
            return self.ballonApprox
        if self.id_team == 2:
            if self.ballon.x > 105.:
                return Vector2D(105.,self.ballonApprox.y)
            return self.ballonApprox

    @property #Devuelve si hay un compañero muy cerca
    def estProcheCoequipier(self):
        d = coequipierProche(self).position.distance(self.joueurPos)
        if d <= 5.:
            return True
        if d > 5.:
            return False
    
    @property #Devuelves si se debe de desmarcar
    def meDemarque(self):
        player = self.state.player_state(self.id_team,self.id_player)
        if distanceBallon(coequipierProche(self),self) < distanceBallon(player,self):
            return True
        else:
            return False

    @property #Devuelve si debe chutar a porteria
    def jeDoisTirer(self):
        if distanceBut(self) < 35. and self.ballon.y > 30. and self.ballon.y < 60.:
            return True
        else:
            return False

    @property #Devuelve si debe pasar el balon
    def jeDoisPasser(self):
        if distanceAdvProche(self.id_player,self) < 2. and self.nbCoequipiers > 1:
            return True
        else:
            return False

    @property #Devuelve si debe despejar el balon
    def jeDoisDegager(self):
        if distanceJoueur(coequipierProche(self),self) > distanceAdvProche(self.id_player,self):
            return True
        else:
            return False
    
    @property
    def jeDoisSortir(self):
        d = distanceBallon(self.joueur,self)
        if distanceAdvProche(self.id_player,self) > d*2:
            if distanceBallon(coequipierProche(self),self) > d:
                if distanceBallon(self.joueur,self) < 10.:
                    return True
        return False
    
    @property #Devuelve el numero de jugadores de su equipo
    def nbCoequipiers(self):
        return len(self.listeEquipe)

    @property #Devuelve si alguien mas puede tocar el balon
    def autrePeutTirer(self):
        liste = []
        for idteam, idplayer in self.state.players:
            if idteam == self.equipeEnnemi:
                if peutToucher(idteam,idplayer,self):
                    liste.append(idplayer)
        if len(liste) > 0:
            return True
        else:
            return False
    
    @property #Devuelve el muro mas proximo (0-Arriba 1-Abajo 2-Izquierda 3-Derecha)
    def murProche(self):
        dArriba = self.joueurPos.distance(Vector2D(self.joueurPos.x,GAME_HEIGHT))
        dAbajo = self.joueurPos.distance(Vector2D(self.joueurPos.x,0))
        dIzq = self.joueurPos.distance(Vector2D(0,self.joueurPos.y))
        dDer = self.joueurPos.distance(Vector2D(GAME_WIDTH,self.joueurPos.y))
        lista = [dArriba,dAbajo,dIzq,dDer]
        minimo = min(lista)
        return lista.index(minimo)