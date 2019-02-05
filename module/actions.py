from soccersimulator import Vector2D, SoccerAction
from module.tools import *

def ir_a(punto,s): #Ir a un punto determinado
    v = punto-s.player
    vnorm = v.normalize()*maxPlayerAcceleration
    return SoccerAction(vnorm,0.)

def chutar(s): #Chutar a porteria
    c = s.goal-s.player
    cnorm = c.normalize()*maxPlayerShoot
    return SoccerAction(0.,cnorm)

def adversaireplusproche(idplayer,s): #Dice cual es el adversario mas cercano a un jugador
    advcercano = s.state.player_state(s.enemy_team,0)
    for i in range(1,len(s.liste_enemy)):
        if s.state.players[i][0] != s.id_team:
            if s.state.player_state(s.id_team,idplayer).position.distance(s.state.player_state(s.enemy_team,i).position) < s.state.player_state(s.id_team,idplayer).position.distance(advcercano.position):
                advcercano = s.state.player_state(s.enemy_team,i)
    return advcercano

def distanceadvproche(idplayer,s): #Da la distancia del jugador mas cercano a uno deseado
    adv = adversaireplusproche(idplayer,s)
    return s.state.player_state(s.id_team,idplayer).position.distance(adv.position)

def teammatealone(s): #Dice cual es el compañero de equipo que está mas alejado de los adversarios
    idsolo = 0
    for i in range(1,len(s.liste_mates)):
        if distanceadvproche(i,s) > distanceadvproche(idsolo,s): #?
            idsolo = i
    return s.state.player_state(s.id_team,idsolo)

def distancia_a(idteam,idplayer,s): #Da la distancia hasta un jugador
    return s.player.distance(s.state.player_state(idteam,idplayer).position)

def teammatecercano(s): #Dice cual es el compañero de equipo mas cercano
    idcerca = 0
    for i in range(1,len(s.liste_mates)):
        if distancia_a(s.id_team,i,s) < distancia_a(s.id_team,idcerca,s): #?
            idcerca = i
    return s.state.player_state(s.id_team,idcerca)

def pasar(s): #Da un pase al jugador mas solo
    p = teammatealone(s).position-s.player
    pnorm = p.normalize()*maxPlayerShoot
    return SoccerAction(0.,pnorm)

def desmarcarse(s): #Se desmarca de su posicion actual
    if s.player.y >= 45:
        d = Vector2D(s.player.x,s.player.y-5.)-s.player
        dnorm = d.normalize()*maxPlayerAcceleration
        return SoccerAction(dnorm,0.)
    if s.player.y < 45:
        d = Vector2D(s.player.x,s.player.y+5.)-s.player
        dnorm = d.normalize()*maxPlayerAcceleration
        return SoccerAction(dnorm,0.)
