from soccersimulator import Vector2D, SoccerAction
from MillaModule.tools import *
from soccersimulator.settings import GAME_WIDTH, GAME_HEIGHT, PLAYER_RADIUS, BALL_RADIUS, maxPlayerAcceleration, maxPlayerShoot

from random import randint

def allerA(punto,s): #Ir a un punto determinado
    v = punto-s.joueurPos
    d = punto.distance(s.joueurPos)
    if d < 0.5:
        return SoccerAction(0,0)
    else:
        vnorm = v.normalize()*maxPlayerAcceleration
        return SoccerAction(vnorm,0.)

def tirer(fuerza,s): #Chutar a porteria (fuerzamax = maxPlayerShoot = 6)
    c = s.but-s.joueurPos
    if fuerza > maxPlayerShoot:
        cnorm = c.normalize()*maxPlayerShoot
        return SoccerAction(0.,cnorm)
    else:
        cnorm = c.normalize()*fuerza #POR LAS PRUEBAS A 35M MEJOR TIRAR CON 4 DE FUERZA
        return SoccerAction(0.,cnorm)

def distanceIdJoueur(idteam,idplayer,s): #Da la distancia hasta un jugador
    return s.joueurPos.distance(s.state.player_state(idteam,idplayer).position)

def distanceJoueur(player1,s): #Da la distancia hasta un jugador
    return s.joueurPos.distance(player1.position)

def distanceBut(s): #Da la distancia hasta la porteria
    return s.joueurPos.distance(s.but)

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

def adversairesProches(distance,s): #Devuelve una lista con los adversarios cercanos a una distancia
    lista = []
    for i in s.listeEnnemi:
            adv = s.state.player_state(s.equipeEnnemi,i)
            if distanceIdJoueur(s.equipeEnnemi,i,s) < distance:
                lista.append(adv)
    return lista

def coequipierSeul(s): #Dice cual es el compañero de equipo que está mas alejado de los adversarios
    if s.nbCoequipiers == 1:
        return s.state.player_state(s.id_team,s.id_player)
    idsolo = 0
    for i in s.listeEquipe:
        if distanceAdvProche(i,s) > distanceAdvProche(idsolo,s):
            if i != s.id_player:
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

def ennemiesAuMilieu(player,s): #Devuelve si hay enemigos entre dos jugadores
    d = distanceJoueur(player,s)
    advProches = adversairesProches(d,s)
    for i in advProches:
        posAdv = i.position
        if posAdv.distance(player.position) < distanceJoueur(player,s):
            return True
    return False

def forceTir(distance,s): #Da la fuerza (valor por el que multiplicar el vector) del tiro
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
    if distance > s.minDistanceBallon and distance < 5:
        return 0.1
    if distance <= s.minDistanceBallon:
        return 0

def forcePasse(distance,s): #Da la fuerza (valor por el que multiplicar el vector) del pase
    if distance >= 40.:
        return maxPlayerShoot
    if distance >= 30. and distance < 40:
        return 4
    if distance >= 20. and distance < 30:
        return 3.5
    if distance >= 5. and distance < 20:
        return 3
    if distance < 5:
        return 2.5

def lancerA(punto,force,s): #Lanza el balon a un punto en concreto
    v = punto-s.joueurPos
    distance = punto.distance(s.joueurPos)
    if force == 0:
        vnorm = v.normalize()*forceTir(distance,s)
    else:
        vnorm = v.normalize()*maxPlayerShoot
    return SoccerAction(0.,vnorm)

def peutToucher(idteam,idplayer,s): #Devuelve si puede tocar el balon
    if s.state.player_state(idteam,idplayer).position.distance(s.ballon) > s.minDistanceBallon:
        return False
    else:
        return True

def jeSuisEnPos(posicion,s): #Devuelve si estoy en posicion
    if s.joueurPos.x >= posicion.x - 2 and s.joueurPos.x <= posicion.x + 2:
        return True
    else:
        return False

def passerAToi(s): #Pasa a si mismo el balon utilizando los muros
    mur = s.murProche
    angle = 10
    if s.id_team == 2:
        angle = -angle
    if s.joueurPos.y <= 45-2*abs(angle):
        angleY = abs(angle)
    if s.joueurPos.y >= 45-2*abs(angle):
        angleY = -abs(angle)

    if mur == 0: # El muro cercano es el de arriba
        murPos = Vector2D(s.joueurPos.x+angle,GAME_HEIGHT)
        cPos = Vector2D(s.joueurPos.x + 2*angle, s.joueurPos.y)
    if mur == 1: # El muro cercano es el de abajo
        murPos = Vector2D(s.joueurPos.x+angle,0)
        cPos = Vector2D(s.joueurPos.x + 2*angle, s.joueurPos.y)
    if mur == 2: # El muro cercano es el de izquierda
        murPos = Vector2D(0,s.joueurPos.y+angleY)
        cPos = Vector2D(s.joueurPos.x, s.joueurPos.y + 2*angleY)
    if mur == 3: # El muro cercano es el de derecha
        murPos = Vector2D(GAME_WIDTH,s.joueurPos.y+angleY)
        cPos = Vector2D(s.joueurPos.x, s.joueurPos.y + 2*angleY)

    d = s.joueurPos.distance(murPos)
    p = murPos - s.joueurPos
    pnorm = p.normalize()*forcePasse(d,s)
    c = cPos - s.joueurPos
    cnorm = c.normalize()*maxPlayerAcceleration
    return SoccerAction(cnorm,pnorm)

def jeDoisPasser(pos,s): #Devuelve si debe pasar el balon
    mate = s.coequipierPlusAvance
    if distanceAdvProche(s.id_player,s)<10 and s.nbCoequipiers>1 and not ennemiesAuMilieu(mate,s):
        return True
    elif s.joueurPos.distance(pos) > 40:
        return True
    else:
        return False

def passer(s): #Da un pase al jugador mas avanzado
    mate = s.coequipierPlusAvance
    d = distanceJoueur(mate,s)
    p = mate.position-s.joueurPos
    pnorm = p.normalize()*forceTir(d,s)
    return SoccerAction(0.,pnorm)

def seDemarquer(s): #Se desmarca de su posicion actual
    if s.joueurPos.y >= 50:
        d = Vector2D(s.joueurPos.x,s.joueurPos.y-10.)-s.joueurPos
        dnorm = d.normalize()*maxPlayerAcceleration
        return SoccerAction(dnorm,0.)
    if s.joueurPos.y <= 40:
        d = Vector2D(s.joueurPos.x,s.joueurPos.y+10.)-s.joueurPos
        dnorm = d.normalize()*maxPlayerAcceleration
        return SoccerAction(dnorm,0.)
    if s.joueurPos.y < 50 and s.joueurPos.y > 40:
        if s.id_team == 1:
            d = Vector2D(s.joueurPos.x-10.,s.joueurPos.y)-s.joueurPos
            dnorm = d.normalize()*maxPlayerAcceleration
            return SoccerAction(dnorm,0.)
        if s.id_team == 2:
            d = Vector2D(s.joueurPos.x+10.,s.joueurPos.y)-s.joueurPos
            dnorm = d.normalize()*maxPlayerAcceleration
            return SoccerAction(dnorm,0.)

def avancerVersBut(s): #Avanza a la porteria dando pequenos toques al balon
    v = s.but-s.joueurPos
    vnorm = v.normalize()*2.5
    return SoccerAction(vnorm,vnorm/2)

def avancer(s): #Avanza por la banda hasta que se acerca
    pos = s.ballon
    if s.id_team == 1:
        if s.joueurPos.y <= 45 and s.joueurPos.y >= 30. and s.joueurPos.x < 100.:
            pos = Vector2D(s.joueurPos.x+1,s.joueurPos.y-1)
        if s.joueurPos.y > 45 and s.joueurPos.y <= GAME_HEIGHT-30. and s.joueurPos.x < 100.:
            pos = Vector2D(s.joueurPos.x+1,s.joueurPos.y+1)
    if s.id_team == 2:
        if s.joueurPos.y <= 45 and s.joueurPos.y >= 30. and s.joueurPos.x > 50.:
            pos = Vector2D(s.joueurPos.x-1,s.joueurPos.y-1)
        if s.joueurPos.y > 45 and s.joueurPos.y <= GAME_HEIGHT-30. and s.joueurPos.x > 50.:
            pos = Vector2D(s.joueurPos.x-1,s.joueurPos.y+1)
    v = pos-s.joueurPos
    vnorm = v.normalize()*2.5
    return SoccerAction(vnorm,vnorm/2)

def degager(s): #Despeja el balon hacia un jugador o hacia la porteria con fuerza
    punto = coequipierSeul(s).position
    if s.but.distance(punto) < s.but.distance(s.joueurPos):
        v = punto-s.joueurPos
        vnorm = v.normalize()*maxPlayerShoot
        return SoccerAction(0.,vnorm)
    else:
        v = s.but-s.joueurPos
        vnorm = v.normalize()*maxPlayerShoot
        return SoccerAction(0.,vnorm)

#####################################################################################
#
# TODO LO DE ABAJO ES PARA EL TME SOLO
#
#####################################################################################

def adversaireAleatoire(s):
    nb = randint(0,s.nbAdversaires-1)
    adversaires = s.listeEnnemi
    adv = s.state.player_state(s.equipeEnnemi, adversaires[nb])
    return adv

def passerAuContraire(s):
    adv = adversaireAleatoire(s)
    return lancerA(adv.position,0,s)

def lancerLoin(s):
    adv = adversaireAleatoire(s)
    if s.id_team == 1:
        if adv.position.x < GAME_WIDTH - GAME_WIDTH/4:
            if adv.position.y < GAME_HEIGHT - GAME_HEIGHT/2:
                return lancerA(Vector2D(GAME_WIDTH - GAME_WIDTH/8,GAME_HEIGHT - GAME_HEIGHT/4),0,s)
            return lancerA(Vector2D(GAME_WIDTH - GAME_WIDTH/8,GAME_HEIGHT - 3*(GAME_HEIGHT/4)),0,s)
        if adv.position.y < GAME_HEIGHT - GAME_HEIGHT/2:
            return lancerA(Vector2D(GAME_WIDTH - 3*(GAME_WIDTH/8),GAME_HEIGHT - GAME_HEIGHT/4),0,s)
        return lancerA(Vector2D(GAME_WIDTH - 3*(GAME_WIDTH/8),GAME_HEIGHT - 3*(GAME_HEIGHT/4)),0,s)
    if s.id_team == 2:
        if adv.position.x < GAME_WIDTH/4:
            if adv.position.y < GAME_HEIGHT - GAME_HEIGHT/2:
                return lancerA(Vector2D(GAME_WIDTH/2 - GAME_WIDTH/8,GAME_HEIGHT - GAME_HEIGHT/4),0,s)
            return lancerA(Vector2D(GAME_WIDTH/2 - GAME_WIDTH/8,GAME_HEIGHT - 3*(GAME_HEIGHT/4)),0,s)
        if adv.position.y < GAME_HEIGHT - GAME_HEIGHT/2:
            return lancerA(Vector2D(GAME_WIDTH/2 - 3*(GAME_WIDTH/8),GAME_HEIGHT - GAME_HEIGHT/4),0,s)
        return lancerA(Vector2D(GAME_WIDTH/2 - 3*(GAME_WIDTH/8),GAME_HEIGHT - 3*(GAME_HEIGHT/4)),0,s)

def posDefense(s):
    equipe = s.listeEquipe
    if s.id_player == 0:
        idmate = 1
    else:
        idmate = 0
    matePos = s.state.player_state(s.id_team,idmate).position

    if s.id_team == 1:
        if matePos.x < GAME_WIDTH/4:
            if matePos.y < GAME_HEIGHT - GAME_HEIGHT/2:
                return Vector2D(GAME_WIDTH/2 - GAME_WIDTH/8,GAME_HEIGHT - GAME_HEIGHT/4)
            return Vector2D(GAME_WIDTH/2 - GAME_WIDTH/8,GAME_HEIGHT - 3*(GAME_HEIGHT/4))
        if matePos.y < GAME_HEIGHT - GAME_HEIGHT/2:
            return Vector2D(GAME_WIDTH/2 - 3*(GAME_WIDTH/8),GAME_HEIGHT - GAME_HEIGHT/4)
        return Vector2D(GAME_WIDTH/2 - 3*(GAME_WIDTH/8),GAME_HEIGHT - 3*(GAME_HEIGHT/4))
    if s.id_team == 2:
        if matePos.x < GAME_WIDTH - GAME_WIDTH/4:
            if matePos.y < GAME_HEIGHT - GAME_HEIGHT/2:
                return Vector2D(GAME_WIDTH - GAME_WIDTH/8,GAME_HEIGHT - GAME_HEIGHT/4)
            return Vector2D(GAME_WIDTH - GAME_WIDTH/8,GAME_HEIGHT - 3*(GAME_HEIGHT/4))
        if matePos.y < GAME_HEIGHT - GAME_HEIGHT/2:
            return Vector2D(GAME_WIDTH - 3*(GAME_WIDTH/8),GAME_HEIGHT - GAME_HEIGHT/4)
        return Vector2D(GAME_WIDTH - 3*(GAME_WIDTH/8),GAME_HEIGHT - 3*(GAME_HEIGHT/4))