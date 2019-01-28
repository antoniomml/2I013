from soccersimulator import Vector2D, SoccerAction
from soccersimulator.settings import GAME_WIDTH, GAME_HEIGHT, PLAYER_RADIUS, BALL_RADIUS, maxPlayerAcceleration, maxPlayerShoot

class SuperState(object):
    def __init__(self,state,id_team,id_player):
        self.state = state
        self.id_team = id_team
        self.id_player = id_player
    
    @property
    def ball(self):
        return self.state.ball.position

    @property
    def player(self):
        return self.state.player_state(self.id_team,self.id_player).position

    @property
    def goal(self):
        if self.id_team == 1:
            return Vector2D(GAME_WIDTH,GAME_HEIGHT/2.)
        if self.id_team == 2:
            return Vector2D(0,GAME_HEIGHT/2.)

    @property
    def ballDistance(self):
        return PLAYER_RADIUS+BALL_RADIUS
    
    @property
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
    
    @property
    def enemy_team(self):
        if self.id_team == 1:
            return 2
        if self.id_team == 2:
            return 1
    
    @property
    def liste_enemy(self):
        liste = []
        for idteam, idplayer in self.state.players:
            if idteam == self.enemy_team:
                liste.append(idplayer)
        return liste

def ir_a(punto,superestado):
    v = punto-superestado.player
    vnorm = v.normalize()*maxPlayerAcceleration
    return SoccerAction(vnorm,0.)

def chutar(superestado):
    c = superestado.goal-superestado.player
    cnorm = c.normalize()*maxPlayerShoot
    return SoccerAction(0.,cnorm)

def can_shoot(superestado):
    if superestado.player.distance(superestado.ball) > superestado.ballDistance:
        return False
    else:
        return True

def adversaireplusproche(idplayer,s):
    minimo = s.state.player_state(s.enemy_team,0)
    for i in range(1,len(s.liste_enemy)):
        if s.state.players[i][0] != s.id_team:
            if s.state.player_state(s.id_team,idplayer).position.distance(s.state.player_state(s.enemy_team,i).position) < s.state.player_state(s.id_team,idplayer).position.distance(minimo.position):
                minimo = s.state.player_state(s.enemy_team,i)
    return minimo

def teammatealone(s):
    massolo = adversaireplusproche(0,s)
    for i in range(1,len(s.liste_enemy)):
        if s.player.distance(adversaireplusproche(i,s).position) < s.player.distance(massolo.position):
            massolo = adversaireplusproche(i,s)
    return massolo

def pasar(superestado):
    p = teammatealone(superestado).position-superestado.player
    pnorm = p.normalize()*maxPlayerShoot
    return SoccerAction(0.,pnorm)