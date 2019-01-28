from soccersimulator import Vector2D, SoccerAction
from soccersimulator.settings import GAME_WIDTH, GAME_HEIGHT, PLAYER_RADIUS, BALL_RADIUS

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

def ir_a(punto,superestado):
    return SoccerAction(punto-superestado.player,0.)

def chutar(superestado):
    return SoccerAction(0.,superestado.goal-superestado.player)