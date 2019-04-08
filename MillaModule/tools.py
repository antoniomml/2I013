from soccersimulator import Vector2D, SoccerAction
from soccersimulator.settings import GAME_WIDTH, GAME_HEIGHT, PLAYER_RADIUS, BALL_RADIUS, maxPlayerAcceleration, maxPlayerShoot
from MillaModule.actions import *

class SuperState(object):
    def __init__(self,state,id_team,id_player):
        self.state = state
        self.id_team = id_team
        self.id_player = id_player
    
    @property #Posicion de la pelota
    def ballon(self):
        return self.state.ball.position
    
    @property #Jugador que ejecuta la estrategia
    def joueur(self):
        return self.state.player_state(self.id_team,self.id_player)
    
    @property #Posicion del jugador que ejecuta la estrategia
    def joueurPos(self):
        return self.joueur.position

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
        pos = self.ballon + 5 * self.state.ball.vitesse
        if pos.x > 0 and pos.x < GAME_WIDTH and pos.y > 0 and pos.y < GAME_HEIGHT:
            return pos
        if pos.y < 0:
            return Vector2D(pos.x,-pos.y)
        if pos.y > GAME_HEIGHT:
            dif = pos.y - GAME_HEIGHT
            return Vector2D(pos.x,GAME_HEIGHT-dif)
        if pos.x < 0:
            return Vector2D(-pos.x,pos.y)
        if pos.x > GAME_WIDTH:
            dif = pos.x - GAME_WIDTH
            return Vector2D(GAME_WIDTH-dif,pos.y)

    @property #Posicion donde debe estar el tirador
    def posFonceur(self):
        if self.nbCoequipiers == 1:
            return self.ballonApprox
        if self.id_team == 1:
            if self.ballonApprox.x < 40:
                return Vector2D(40.,self.ballonApprox.y)
            else:
                return self.ballonApprox
        if self.id_team == 2:
            if self.ballonApprox.x > GAME_WIDTH-40.:
                return Vector2D(GAME_WIDTH-40.,self.ballonApprox.y)
            else:
                return self.ballonApprox

    @property #Posicion donde debe estar el portero
    def posGardien(self):
        if self.id_team == 1:
            if self.ballonApprox.y > 60.:
                if self.ballon.x < 5.:
                    return Vector2D(self.ballonApprox.x,60.)
                return Vector2D(5.,60.)
            if self.ballonApprox.y < 30.:
                if self.ballonApprox.x < 5.:
                    return Vector2D(self.ballonApprox.x,30.)
                return Vector2D(5.,30.)
            if self.ballonApprox.x < 10.:
                return self.ballonApprox
            return Vector2D(10.,self.ballonApprox.y)
        if self.id_team == 2:
            if self.ballonApprox.y > 60.:
                if self.ballonApprox.x > GAME_WIDTH-5.:
                    return Vector2D(self.ballonApprox.x,60.)
                return Vector2D(GAME_WIDTH-5.,60.)
            if self.ballonApprox.y < 30.:
                if self.ballonApprox.x > GAME_WIDTH-5.:
                    return Vector2D(self.ballonApprox.x,30.)
                return Vector2D(GAME_WIDTH-5.,30.)
            if self.ballonApprox.x > GAME_WIDTH-10.:
                return self.ballonApprox
            return Vector2D(GAME_WIDTH-10.,self.ballonApprox.y)

    @property #Posicion donde debe estar el defensa
    def posDefenseur(self):
        if self.id_team == 1:
            if self.ballonApprox.x > 40:
                return Vector2D(40.,self.ballonApprox.y)
            if distanceIdJoueur(2,self.idEnnemiPlusAvance,self) > 5. and self.ballonApprox.x > self.joueurPos.x:
                posj = self.ennemiPlusAvance.position.x
                return Vector2D(posj/2,self.ballonApprox.y)
            return self.ballonApprox
        if self.id_team == 2:
            if self.ballonApprox.x < 110.:
                return Vector2D(110.,self.ballonApprox.y)
            if distanceIdJoueur(1,self.idEnnemiPlusAvance,self) > 5. and self.ballonApprox.x < self.joueurPos.x:
                posj = self.ennemiPlusAvance.position.x
                xpos = ((GAME_WIDTH-posj)/2)+posj
                return Vector2D(xpos,self.ballonApprox.y)
            return self.ballonApprox
    
    @property #Posicion donde debe estar el delantero solitario
    def posAttaquant(self):
        if self.nbCoequipiers == 1:
            return self.ballonApprox
        if self.id_team == 1:
            if self.ballonApprox.x < 45.:
                return Vector2D(45.,self.ballonApprox.y)
            return self.ballonApprox
        if self.id_team == 2:
            if self.ballonApprox.x > 105.:
                return Vector2D(105.,self.ballonApprox.y)
            return self.ballonApprox

    @property #Posicion donde debe estar el delantero derecho
    def posAttaquantDroit(self):
        if self.nbCoequipiers == 1:
            return self.ballonApprox
        if self.id_team == 1:
            if self.ballonApprox.x < 45.:
                if self.ballonApprox.y > 50.:
                    return Vector2D(45.,50.)
                return Vector2D(45.,self.ballonApprox.y)
            if self.ballonApprox.y > 50.:
                return Vector2D(self.ballonApprox.x,50.)
            return self.ballonApprox
        if self.id_team == 2:
            if self.ballonApprox.x > 105.:
                if self.ballonApprox.y < 40.:
                    return Vector2D(105.,40.)
                return Vector2D(105.,self.ballonApprox.y)
            if self.ballonApprox.y < 40:
                return Vector2D(self.ballonApprox.x,40.)
            return self.ballonApprox

    @property #Posicion donde debe estar el delantero izquierdo
    def posAttaquantGauche(self):
        if self.nbCoequipiers == 1:
            return self.ballonApprox
        if self.id_team == 1:
            if self.ballonApprox.x < 45.:
                if self.ballonApprox.y < 40.:
                    return Vector2D(45.,40.)
                return Vector2D(45.,self.ballonApprox.y)
            if self.ballonApprox.y < 40.:
                return Vector2D(self.ballonApprox.x,40.)
            return self.ballonApprox
        if self.id_team == 2:
            if self.ballonApprox.x > 105.:
                if self.ballonApprox.y > 50.:
                    return Vector2D(105.,50.)
                return Vector2D(105.,self.ballonApprox.y)
            if self.ballonApprox.y > 50:
                return Vector2D(self.ballonApprox.x,50.)
            return self.ballonApprox

    @property
    def posAttaquantStatique(self):
        if self.id_team == 1:
            return Vector2D(130,45)
        if self.id_team == 2:
            return Vector2D(20,45)

    @property
    def posMilieuStatique(self):
        if self.id_team == 1:
            return Vector2D(80,60)
        if self.id_team == 2:
            return Vector2D(60,30)

    @property
    def posDefenseurStatique(self):
        if self.id_team == 1:
            return Vector2D(30,35)
        if self.id_team == 2:
            return Vector2D(60,55)
    

    @property #Devuelve si eres el companero mas cercano al balon
    def jeSuisProche(self):
        moi = self.joueur
        for i in self.listeEquipe:
            play = self.state.player_state(self.id_team,i)
            if distanceBallon(play,self) < distanceBallon(moi,self):
                return False
        return True
    

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
   
    @property #Devuelve si debe pasar el balon a si mismo
    def jeDoisPasserAMoi(self):
        if self.distanceMurProche < 25. and self.autreEstDevant:
            if self.distanceMurProche < distanceJoueur(coequipierProche(self),self):
                return True
        return False

    @property #Devuelve si debe despejar el balon
    def jeDoisDegager(self):
        if distanceJoueur(coequipierProche(self),self) > distanceAdvProche(self.id_player,self):
            return True
        else:
            return False
    
    @property #Devuelve si debe salir el jugador a por el balon
    def jeDoisSortir(self):
        d = distanceBallon(self.joueur,self)
        if distanceAdvProche(self.id_player,self) > d*2:
            if distanceBallon(coequipierProche(self),self) > d:
                if distanceBallon(self.joueur,self) < 25.:
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
   
    @property #Devuelve si hay jugadores delante
    def autreEstDevant(self):
        advProches = adversairesProches(20.,self)
        for i in advProches:
            posAdv = i.position
            if self.id_team == 1 and self.joueurPos.x < posAdv.x:
                return True
            if self.id_team == 2 and self.joueurPos.x > posAdv.x:
                return True
        return False

    @property #Distancia al muro mas proximo
    def distanceMurProche(self): 
        dArriba = self.joueurPos.distance(Vector2D(self.joueurPos.x,GAME_HEIGHT))
        dAbajo = self.joueurPos.distance(Vector2D(self.joueurPos.x,0))
        dIzq = self.joueurPos.distance(Vector2D(0,self.joueurPos.y))
        dDer = self.joueurPos.distance(Vector2D(GAME_WIDTH,self.joueurPos.y))
        lista = [dArriba,dAbajo,dIzq,dDer]
        return min(lista)

    @property #Devuelve el muro mas proximo (0-Arriba 1-Abajo 2-Izquierda 3-Derecha)
    def murProche(self):
        dArriba = self.joueurPos.distance(Vector2D(self.joueurPos.x,GAME_HEIGHT))
        dAbajo = self.joueurPos.distance(Vector2D(self.joueurPos.x,0))
        dIzq = self.joueurPos.distance(Vector2D(0,self.joueurPos.y))
        dDer = self.joueurPos.distance(Vector2D(GAME_WIDTH,self.joueurPos.y))
        lista = [dArriba,dAbajo,dIzq,dDer]
        minimo = min(lista)
        return lista.index(minimo)

    @property #Devuelve quien esta mas cerca del balón EN PROGRESO
    def quiALeBallon(self):
        mini = self.state.player_state(self.id_team,self.id_player)
        for idteam, idplayer in self.state.players:
            j = self.state.player_state(idteam,idplayer)
            dBallon = distanceBallon(j.position,self)
            if dBallon <= self.minDistanceBallon:
                if dBallon <= distanceBallon(mini.position):
                    mini = j
        return mini
    
    @property #Devuelve si nuestro equipo tiene el balon
    def onALeBallon(self): 
        mini = self.joueur
        team = self.id_team
        for idteam, idplayer in self.state.players:
            j = self.state.player_state(idteam,idplayer)
            dBallon = distanceBallon(j,self)
            if dBallon <= self.minDistanceBallon:
                if dBallon <= distanceBallon(mini,self):
                    mini = j
                    team = idteam
        if team == self.id_team:
            return True
        if team == self.equipeEnnemi:
            return False

    @property #Devuelve el adversario mas avanzado
    def ennemiPlusAvance(self):
        maxi = self.joueur
        for idplayer in self.listeEnnemi:
            p = self.state.player_state(self.equipeEnnemi,idplayer)
            if self.equipeEnnemi == 1:
                if p.position.x > maxi.position.x:
                    maxi = p
            if self.equipeEnnemi == 2:
                if p.position.x < maxi.position.x:
                    maxi = p
        return maxi

    @property #Devuelve el companero mas avanzado
    def coequipierPlusAvance(self):
        maxi = self.joueur
        for idplayer in self.listeEquipe:
            p = self.state.player_state(self.id_team,idplayer)
            if self.id_team == 1:
                if p.position.x > maxi.position.x:
                    maxi = p
            if self.id_team == 2:
                if p.position.x < maxi.position.x:
                    maxi = p
        return maxi
    
    @property #Devuelve el id del adversario mas avanzado
    def idEnnemiPlusAvance(self):
        maxi = self.state.player_state(self.equipeEnnemi,0)
        idj = 0
        for idplayer in self.listeEnnemi:
            p = self.state.player_state(self.equipeEnnemi,idplayer)
            if self.equipeEnnemi == 1:
                if p.position.x > maxi.position.x:
                    maxi = p
                    idj = idplayer
            if self.equipeEnnemi == 2:
                if p.position.x < maxi.position.x:
                    maxi = p
                    idj = idplayer
        return idj