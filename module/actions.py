from soccersimulator import Vector2D, SoccerAction
from module.tools import *

def ir_a(punto,s): #Ir a un punto determinado
    v = punto-s.player
    vnorm = v.normalize()*maxPlayerAcceleration
    return SoccerAction(vnorm,0.)

def chutar(fuerza,s): #Chutar a porteria (si fuerza = 0 -> fuerza = maxPlayerShoot)
    c = s.goal-s.player
    if fuerza == 0:
        cnorm = c.normalize()*maxPlayerShoot
        return SoccerAction(0.,cnorm)
    else:
        cnorm = c.normalize()*fuerza #POR LAS PRUEBAS A 35M MEJOR TIRAR CON 4 DE FUERZA
        return SoccerAction(0.,cnorm)

def distancia_a(idteam,idplayer,s): #Da la distancia hasta un jugador
    return s.player.distance(s.state.player_state(idteam,idplayer).position)

def distanciaPlayer(player1,s): #Da la distancia hasta un jugador
    return s.player.distance(player1.position)

def distanciaPorteria(s): #Da la distancia hasta la porteria
    return s.player.distance(s.goal)

def distanciaBalon(player,s): #Da la distancia hasta el balon
    return player.position.distance(s.ball)

def distanceadvproche(idplayer,s): #Da la distancia del jugador mas cercano a uno deseado
    adv = adversaireplusproche(idplayer,s)
    return s.state.player_state(s.id_team,idplayer).position.distance(adv.position)

def adversaireplusproche(idplayer,s): #Dice cual es el adversario mas cercano a un jugador
    advcercano = s.state.player_state(s.enemy_team,0)
    for i in range(1,len(s.liste_enemy)):
        if s.state.players[i][0] != s.id_team:
            if s.state.player_state(s.id_team,idplayer).position.distance(s.state.player_state(s.enemy_team,i).position) < s.state.player_state(s.id_team,idplayer).position.distance(advcercano.position):
                advcercano = s.state.player_state(s.enemy_team,i)
    return advcercano

def teammatealone(s): #Dice cual es el compañero de equipo que está mas alejado de los adversarios
    if s.nbteammates == 1:
        return s.state.player_state(s.id_team,s.id_player)
    idsolo = 0
    for i in range(1,len(s.liste_mates)):
        if distanceadvproche(i,s) > distanceadvproche(idsolo,s): #?
            idsolo = i
    return s.state.player_state(s.id_team,idsolo)

def teammatecercano(s): #Dice cual es el compañero de equipo mas cercano
    if s.nbteammates == 1:
        return s.state.player_state(s.id_team,s.id_player)
    if s.id_player == 0:
        idcerca = 1
    else:
        idcerca = 0
    for i in range(1,len(s.liste_mates)):
        if distancia_a(s.id_team,i,s) < distancia_a(s.id_team,idcerca,s):
            if i != s.id_player:
                idcerca = i
    return s.state.player_state(s.id_team,idcerca)

def pasar(s): #Da un pase al jugador mas solo
    mate = teammatealone(s)
    d = distanciaPlayer(mate,s)
    p = mate.position-s.player
    if d >= 60.:
        pnorm = p.normalize()*maxPlayerShoot
        return SoccerAction(0.,pnorm)
    if d >= 50. and d < 60:
        pnorm = p.normalize()*5.
        return SoccerAction(0.,pnorm)
    if d >= 40. and d < 50:
        pnorm = p.normalize()*4.
        return SoccerAction(0.,pnorm)
    if d >= 30. and d < 40:
        pnorm = p.normalize()*4.
        return SoccerAction(0.,pnorm)
    if d < 30:
        pnorm = p.normalize()*3.
        return SoccerAction(0.,pnorm)
    

def desmarcarse(s): #Se desmarca de su posicion actual
    if s.player.y >= 50:
        d = Vector2D(s.player.x,s.player.y-10.)-s.player
        dnorm = d.normalize()*maxPlayerAcceleration
        return SoccerAction(dnorm,0.)
    if s.player.y <= 40:
        d = Vector2D(s.player.x,s.player.y+10.)-s.player
        dnorm = d.normalize()*maxPlayerAcceleration
        return SoccerAction(dnorm,0.)
    if s.player.y < 50 and s.player.y > 40:
        if s.id_team == 1:
            d = Vector2D(s.player.x-10.,s.player.y)-s.player
            dnorm = d.normalize()*maxPlayerAcceleration
            return SoccerAction(dnorm,0.)
        if s.id_team == 2:
            d = Vector2D(s.player.x+10.,s.player.y)-s.player
            dnorm = d.normalize()*maxPlayerAcceleration
            return SoccerAction(dnorm,0.)

def avanzar(s): #Avanza dando pequenos toques al balon
    v = s.goal-s.player
    vnorm = v.normalize()*2.5
    return SoccerAction(vnorm,vnorm/2)

def despejar(s): #Despeja el balon hacia un jugador o hacia la porteria con fuerza
    punto = teammatealone(s).position
    if s.goal.distance(punto) < s.goal.distance(s.player):
        v = punto-s.player
        vnorm = v.normalize()*maxPlayerShoot
        return SoccerAction(0.,vnorm)
    else:
        v = s.goal-s.player
        vnorm = v.normalize()*maxPlayerShoot
        return SoccerAction(0.,vnorm)