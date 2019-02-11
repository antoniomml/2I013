from soccersimulator import Vector2D, SoccerAction
from soccersimulator.settings import GAME_WIDTH, GAME_HEIGHT, PLAYER_RADIUS, BALL_RADIUS, maxPlayerAcceleration, maxPlayerShoot
from module.actions import *

class SuperState(object):
    def __init__(self,state,id_team,id_player):
        self.state = state
        self.id_team = id_team
        self.id_player = id_player
    
    @property #Posicion de la pelota
    def ball(self):
        return self.state.ball.position

    @property #Posicion del jugador que ejecuta la estrategia
    def player(self):
        return self.state.player_state(self.id_team,self.id_player).position

    @property #Posicion de la porteria contraria
    def goal(self):
        if self.id_team == 1:
            return Vector2D(GAME_WIDTH,GAME_HEIGHT/2.)
        if self.id_team == 2:
            return Vector2D(0,GAME_HEIGHT/2.)

    @property #Distancia desde la que se puede tocar el balon
    def minBallDistance(self):
        return PLAYER_RADIUS+BALL_RADIUS

    @property #Devuelve si puede tocar el balon
    def can_touch(self):
        if self.player.distance(self.ball) > self.minBallDistance:
            return False
        else:
            return True
    
    @property #Id del equipo enemigo
    def enemy_team(self):
        if self.id_team == 1:
            return 2
        if self.id_team == 2:
            return 1
    
    @property #Lista de los id del equipo enemigo
    def liste_enemy(self):
        liste = []
        for idteam, idplayer in self.state.players:
            if idteam == self.enemy_team:
                liste.append(idplayer)
        return liste

    @property #Lista de los id del equipo actual
    def liste_mates(self):
        liste = []
        for idteam, idplayer in self.state.players:
            if idteam == self.id_team:
                liste.append(idplayer)
        return liste

    @property #Posicion donde estará la pelota segun su velocidad
    def ballaprox(self):
        return self.ball + 5 * self.state.ball.vitesse

    @property #Posicion donde debe estar el portero
    def posPortero(self):
        if self.id_team == 1:
            if self.ball.y > 60.:
                if self.ball.x < 5.:
                    return Vector2D(self.ballaprox.x,60.)
                return Vector2D(5.,60.)
            if self.ball.y < 30.:
                if self.ball.x < 5.:
                    return Vector2D(self.ballaprox.x,30.)
                return Vector2D(5.,30.)
            if self.ball.x < 10.:
                return self.ballaprox
            return Vector2D(10.,self.ballaprox.y)
        if self.id_team == 2:
            if self.ball.y > 60.:
                if self.ball.x > GAME_WIDTH-5.:
                    return Vector2D(self.ballaprox.x,60.)
                return Vector2D(GAME_WIDTH-5.,60.)
            if self.ball.y < 30.:
                if self.ball.x > GAME_WIDTH-5.:
                    return Vector2D(self.ballaprox.x,30.)
                return Vector2D(GAME_WIDTH-5.,30.)
            if self.ball.x > GAME_WIDTH-10.:
                return self.ballaprox
            return Vector2D(GAME_WIDTH-10.,self.ballaprox.y)

    @property #Posicion donde debe estar el defensa
    def posDefensa(self):
        if self.id_team == 1:
            if self.ball.x > 70:
                return Vector2D(70.,self.ballaprox.y)
            return self.ballaprox
        if self.id_team == 2:
            if self.ball.x < 80.:
                return Vector2D(80.,self.ballaprox.y)
            return self.ballaprox
    
    @property #Posicion donde debe estar el delantero
    def posDelantero(self):
        if len(self.liste_mates) == 1:
            return self.ballaprox
        if self.id_team == 1:
            if self.ball.x < 60.:
                return Vector2D(60.,self.ballaprox.y)
            return self.ballaprox
        if self.id_team == 2:
            if self.ball.x > 90.:
                return Vector2D(90.,self.ballaprox.y)
            return self.ballaprox

    @property #Devuelve si hay un compañero muy cerca
    def isNearMate(self):
        d = teammatecercano(self).position.distance(self.player)
        if d <= 5.:
            return True
        if d > 5.:
            return False
    
    @property
    def meDesmarco(self):
        if distanciaBalon(teammatecercano(self),self) < distanciaBalon(self.state.player_state(self.id_team,self.id_player),self):
            return True
        else:
            return False

    @property
    def deboChutar(self):
        if self.id_team == 1:
            if self.ball.x > 115. and self.ball.y > 30. and self.ball.y < 60.:
                return True
            else:
                return False
        if self.id_team == 2:
            if self.ball.x < 35.:
                return True
            else:
                return False

    @property
    def deboPasar(self):
        if distanceadvproche(self.id_player,self) < 2. and self.nbteammates > 1:
            return True
        else:
            return False
    
    @property
    def nbteammates(self):
        return len(self.liste_mates)
    