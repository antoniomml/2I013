from soccersimulator import Vector2D, SoccerAction
from module.tools import *

def allerA(punto,s): #Ir a un punto determinado
    v = punto-s.joueur
    vnorm = v.normalize()*maxPlayerAcceleration
    return SoccerAction(vnorm,0.)

def tirer(fuerza,s): #Chutar a porteria (si fuerza = 0 -> fuerza = maxPlayerShoot)
    c = s.but-s.joueur
    if fuerza == 0:
        cnorm = c.normalize()*maxPlayerShoot
        return SoccerAction(0.,cnorm)
    else:
        cnorm = c.normalize()*fuerza #POR LAS PRUEBAS A 35M MEJOR TIRAR CON 4 DE FUERZA
        return SoccerAction(0.,cnorm)

def distanceIdJoueur(idteam,idplayer,s): #Da la distancia hasta un jugador
    return s.joueur.distance(s.state.player_state(idteam,idplayer).position)

def distanceJoueur(player1,s): #Da la distancia hasta un jugador
    return s.joueur.distance(player1.position)

def distanceBut(s): #Da la distancia hasta la porteria
    return s.joueur.distance(s.but)

def distanceBallon(player,s): #Da la distancia hasta el balon
    return player.position.distance(s.ballon)

def distanceAdvProche(idplayer,s): #Da la distancia del jugador mas cercano a uno deseado
    adv = adversairePlusProche(idplayer,s)
    return s.state.player_state(s.id_team,idplayer).position.distance(adv.position)

def adversairePlusProche(idplayer,s): #Dice cual es el adversario mas cercano a un jugador
    advcercano = s.state.player_state(s.equipeEnnemi,0)
    ppos = s.state.player_state(s.id_team,idplayer).position
    for i in range(1,len(s.listeEnnemi)):
        if s.state.players[i][0] != s.id_team:
            if ppos.distance(s.state.player_state(s.equipeEnnemi,i).position) < ppos.distance(advcercano.position):
                advcercano = s.state.player_state(s.equipeEnnemi,i)
    return advcercano

def coequipierSeul(s): #Dice cual es el compañero de equipo que está mas alejado de los adversarios
    if s.nbTeammates == 1:
        return s.state.player_state(s.id_team,s.id_player)
    idsolo = 0
    for i in range(1,len(s.listeEquipe)):
        if distanceAdvProche(i,s) > distanceAdvProche(idsolo,s): #?
            idsolo = i
    return s.state.player_state(s.id_team,idsolo)

def coequipierProche(s): #Dice cual es el compañero de equipo mas cercano
    if s.nbTeammates == 1:
        return s.state.player_state(s.id_team,s.id_player)
    if s.id_player == 0:
        idcerca = 1
    else:
        idcerca = 0
    for i in range(1,len(s.listeEquipe)):
        if distanceIdJoueur(s.id_team,i,s) < distanceIdJoueur(s.id_team,idcerca,s):
            if i != s.id_player:
                idcerca = i
    return s.state.player_state(s.id_team,idcerca)

#def lancerA(s):


def passer(s): #Da un pase al jugador mas solo
    mate = coequipierSeul(s)
    d = distanceJoueur(mate,s)
    p = mate.position-s.joueur
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
    

def seDemarquer(s): #Se desmarca de su posicion actual
    if s.joueur.y >= 50:
        d = Vector2D(s.joueur.x,s.joueur.y-10.)-s.joueur
        dnorm = d.normalize()*maxPlayerAcceleration
        return SoccerAction(dnorm,0.)
    if s.joueur.y <= 40:
        d = Vector2D(s.joueur.x,s.joueur.y+10.)-s.joueur
        dnorm = d.normalize()*maxPlayerAcceleration
        return SoccerAction(dnorm,0.)
    if s.joueur.y < 50 and s.joueur.y > 40:
        if s.id_team == 1:
            d = Vector2D(s.joueur.x-10.,s.joueur.y)-s.joueur
            dnorm = d.normalize()*maxPlayerAcceleration
            return SoccerAction(dnorm,0.)
        if s.id_team == 2:
            d = Vector2D(s.joueur.x+10.,s.joueur.y)-s.joueur
            dnorm = d.normalize()*maxPlayerAcceleration
            return SoccerAction(dnorm,0.)

def avancer(s): #Avanza dando pequenos toques al balon
    v = s.but-s.joueur
    vnorm = v.normalize()*2.5
    return SoccerAction(vnorm,vnorm/2)

def degager(s): #Despeja el balon hacia un jugador o hacia la porteria con fuerza
    punto = coequipierSeul(s).position
    if s.but.distance(punto) < s.but.distance(s.joueur):
        v = punto-s.joueur
        vnorm = v.normalize()*maxPlayerShoot
        return SoccerAction(0.,vnorm)
    else:
        v = s.but-s.joueur
        vnorm = v.normalize()*maxPlayerShoot
        return SoccerAction(0.,vnorm)