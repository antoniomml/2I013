from soccersimulator import Vector2D, SoccerAction
from MillaModule.tools import *

def allerA(punto,s): #Ir a un punto determinado
    v = punto-s.joueur
    d = punto.distance(s.joueur)
    if d < 2:
        return SoccerAction(0,0)
    else:
        vnorm = v.normalize()*maxPlayerAcceleration
        return SoccerAction(vnorm,0.)

def tirer(fuerza,s): #Chutar a porteria (fuerzamax = maxPlayerShoot = 6)
    c = s.but-s.joueur
    if fuerza > maxPlayerShoot:
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
    if s.nbCoequipiers == 1:
        return s.state.player_state(s.id_team,s.id_player)
    idsolo = 0
    for i in range(1,len(s.listeEquipe)):
        if distanceAdvProche(i,s) > distanceAdvProche(idsolo,s): #?
            idsolo = i
    return s.state.player_state(s.id_team,idsolo)

def coequipierProche(s): #Dice cual es el compañero de equipo mas cercano
    if s.nbCoequipiers == 1:
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

def forceTir(distance,s):
    if distance >= 60.:
        return maxPlayerShoot
    if distance >= 50. and distance < 60:
        return 5
    if distance >= 30. and distance < 50:
        return 4
    if distance >= 20. and distance < 30:
        return 3
    if distance >= 5. and distance < 20:
        return 1
    if distance >= 2. and distance < 5:
        return 0.1
    if distance < 2.:
        return 0

def lancerA(punto,s): #Lanza el balon a un punto en concreto
    v = punto-s.joueur
    distance = punto.distance(s.joueur)
    vnorm = v.normalize()*forceTir(distance,s)
    return SoccerAction(0.,vnorm)

def peutToucher(idteam,idplayer,s): #Devuelve si puede tocar el balon
    if s.state.player_state(idteam,idplayer).position.distance(s.ballon) > s.minDistanceBallon:
        return False
    else:
        return True

def passer(s): #Da un pase al jugador mas solo
    mate = coequipierSeul(s)
    d = distanceJoueur(mate,s)
    p = mate.position-s.joueur
    pnorm = p.normalize()*forceTir(d,s)
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