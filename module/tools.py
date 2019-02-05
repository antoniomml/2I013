from soccersimulator import Vector2D, SoccerAction
from soccersimulator.settings import GAME_WIDTH, GAME_HEIGHT, PLAYER_RADIUS, BALL_RADIUS, maxPlayerAcceleration, maxPlayerShoot

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
    
    @property #Posicion donde debe estar el portero
    def posPortero(self):
        if self.id_team == 1:
            if self.ball.y > 60.:
                return Vector2D(5.,60.)
            if self.ball.y < 30.:
                return Vector2D(5.,30.)
            return Vector2D(10.,self.ball.y)
        if self.id_team == 2:
            if self.ball.y > 60.:
                return Vector2D(GAME_WIDTH-5.,60.)
            if self.ball.y < 30.:
                return Vector2D(GAME_WIDTH-5.,30.)
            return Vector2D(GAME_WIDTH-10.,self.ball.y)
    
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