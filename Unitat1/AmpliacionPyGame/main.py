import os
import random
import sqlite3
import time
from sqlite3 import Error

import pygame
from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
    RLEACCEL
)


# Clase Enemic
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super(Enemy, self).__init__()
        self.surf = pygame.image.load(os.path.join(resources, "missile.png")).convert()
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surf.get_rect(
            center=(
                random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
                random.randint(0, SCREEN_HEIGHT),
            )
        )

        # Velocitat enemics
        self.speed = random.randint(2 * nivel, 10 + 3 * nivel)

    # Fa que els enemics es meregen a l'esquerre y els mate quan ixquen de la pantalla
    def update(self):
        global punts
        global nivel
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            for e in enemies:
                if e.rect.right <= 1:
                    punts += 10
                    if punts % 500 == 0:
                        nivel += 1
            self.kill()


# Clase jugador
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.surf = pygame.image.load(os.path.join(resources, "jet.png")).convert()
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surf.get_rect()
        self.rect.center = (100, SCREEN_HEIGHT // 2)

    # Moviments del jugador
    def update(self, pressed_keys):
        if pressed_keys[K_UP]:
            self.rect.move_ip(0, -5)
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0, 5)
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-5, 0)
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(5, 0)

        # Mantenim al jugador dins la pantalla
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT


# Clase nubes
class Cloud(pygame.sprite.Sprite):
    def __init__(self):
        super(Cloud, self).__init__()
        self.surf = pygame.image.load(os.path.join(resources, "cloud.png")).convert()
        self.surf.set_colorkey((0, 0, 0), RLEACCEL)
        self.rect = self.surf.get_rect(
            center=(
                random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
                random.randint(20, SCREEN_HEIGHT)
            )
        )

    # Els nuvols es meregen a l'esquerre y es destrueixen al ixir de la pantalla
    def update(self):
        self.rect.move_ip(-5, 0)
        if self.rect.right < 0:
            self.kill()


# Paleta de colors
blanc = (255, 255, 255)
negre = (0, 0, 0)
roig = (255, 0, 0)
blau = (0, 0, 255)
verd = (0, 255, 0)
groc = (255, 255, 0)
cian = (0, 255, 255)
magenta = (255, 0, 255)

if __name__ == '__main__':

    # Inicia el joc
    pygame.init()

    # ruta de la carpeta de recursos
    resources = os.path.join(os.path.dirname(__file__), "resources")

    # Mostra la puntuació i el nivell
    def mostar(surface, text, text2, size, x, y):
        font = pygame.font.SysFont("arial", size)  # fuente del marcador
        if Fondos == True:
            text_surface = font.render("{} : {}".format(text, text2), True, negre)  # color y tamaño de la letra
        elif Fondos == False:
            text_surface = font.render("{} : {}".format(text, text2), True, blanc)
        text_rect = text_surface.get_rect()
        text_rect.midright = (x, y)
        surface.blit(text_surface, text_rect)

    # Es conecta a la base de dades
    def conectar():
        try:
            sqliteConnection = sqlite3.connect((os.path.join(resources, "puntuacion.db")))
            return sqliteConnection
        except Error:
            print(Error)

    # Llig la puntuació maxima
    def lSQL():
        cursor = conectar().cursor()
        cursor.execute("SELECT score FROM puntuacion")
        row = cursor.fetchone()
        return row[0]

    # Comprova si has superat o no la puntuació maxima
    def uSQL():
        curs = conectar().cursor()
        if lSQL() > punts:
            print("Record no superado")
            print(f"Puntuacion: {str(punts)}")
        if lSQL() < punts:
            curs.execute(f"Update puntuacion set score = {str(punts)}")
            print(f"Nuevo record: {punts}")
            curs.execute("select * from puntuacion")
            conectar().commit()

    # Afegix la nova puntuació
    def iSQL(punts):
        obj = conectar().cursos()
        if lSQL() == 0:
            obj.execute(f'INSERT INTO puntuacion VALUES({punts})')

        if lSQL() > punts:
            return
        else:
            uSQL()

        conectar().comit()


# Altura y llargaria del joc
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600

# Agrega la altura y la llargaria per a crear la finestra del joc
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Titol del joc
pygame.display.set_caption("NAVETRIS")

# Variable per si volem tornar a iniciar el joc
empezar = True

# Bucle per si vols tornar a iniciar el joc
while empezar:

    # Iniciem els punts del joc a 0 i el nivell a 1
    punts = 0
    nivel = 1

    # Afegir els nuvols
    ADDCLOUD = pygame.USEREVENT + 2
    pygame.time.set_timer(ADDCLOUD, 2000)

    # Per a afegir els enemics
    ADDENEMY = pygame.USEREVENT + 1

    # Instantiate player. Right now, this is just a rectangle.
    player = Player()

    enemies = pygame.sprite.Group()
    clouds = pygame.sprite.Group()
    all_sprites = pygame.sprite.Group()
    all_sprites.add(player)

    # Setup the clock for a decent framerate
    fps = 30
    clock = pygame.time.Clock()

    # Variables per a controlar si obrim el menu de inici, el joc y el menu final
    running = True
    menu = True
    menuFinal = True

    # Musica per al menu
    pygame.mixer.music.load(os.path.join(resources, "MusicaMenu.ogg"))
    pygame.mixer.music.play(loops=-1)
    pygame.mixer.music.set_volume(0.1)

    while menu:

        for i in pygame.event.get():
            if i.type == pygame.QUIT:
                quit()

        # Fondo del menu
        fondoMenu = pygame.image.load(os.path.join(resources, "fondoMenu.png")).convert()
        screen.blit(fondoMenu, (0, 0))

        # Titul del joc
        textoNombre = pygame.image.load(os.path.join(resources, "NombreJuego.png")).convert()
        textoNombre.set_colorkey(negre, RLEACCEL)
        screen.blit(textoNombre, (300, 50))

        # Format del menu
        texto = pygame.font.SysFont("none", 60).render("Pulsa 'p' para jugar", 1, negre)
        screen.blit(texto, (310, 250))

        eixir = pygame.font.SysFont("serif", 40).render("Pulsa 'ESC' para salir", 1, negre)
        screen.blit(eixir, (10, 550))

        # Si apretes la p inicies el joc
        if pygame.key.get_pressed()[pygame.K_p]:
            menu = False

        # Si apretes el escape ix del joc
        if pygame.key.get_pressed()[pygame.K_ESCAPE]:
            menu = False
            running = False
            menuFinal = False
            empezar = False

        pygame.display.update()

    # Afegim una image, per defecte la del dia
    fondo = pygame.image.load(os.path.join(resources, "Fondo1.jpg")).convert()
    Fondos = True

    # Canvi de fondo entre el dia i la nit
    ADDTIME = pygame.USEREVENT + 3
    pygame.time.set_timer(ADDTIME, 20000)

    # Inicialitzem la musica
    pygame.mixer.init()

    # Musica per al joc principal, es reprodueix infinitament
    pygame.mixer.music.load(os.path.join(resources, "Chiptronical.ogg"))
    pygame.mixer.music.play(loops=-1)
    pygame.mixer.music.set_volume(0.1)

    # Sonido per a la col·lisió
    collision_sound = pygame.mixer.Sound(os.path.join(resources, "Collision.wav"))

    # Variable per al fondo en moviment
    movimentFondo = 0
    crear = 0

    # Main loop
    while running:
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
            elif event.type == QUIT:
                quit()

            # Afegix un enemic
            elif event.type == ADDENEMY:
                new_enemy = Enemy()
                enemies.add(new_enemy)
                all_sprites.add(new_enemy)

            # Afegix un nuvol
            elif event.type == ADDCLOUD:
                new_cloud = Cloud()
                clouds.add(new_cloud)
                all_sprites.add(new_cloud)

            # Depenent de si es de dia o de nit afegira una image o altra
            elif event.type == ADDTIME:
                if Fondos:
                    Fondos = False
                    fondo = pygame.image.load(os.path.join(resources, "Fondo2.jpg")).convert()
                elif not Fondos:
                    Fondos = True
                    fondo = pygame.image.load(os.path.join(resources, "Fondo1.jpg")).convert()

        # Els fondos estan en constant moviment i tornen a començar quan acaben
        mover = movimentFondo % fondo.get_rect().width
        screen.blit(fondo, (mover - fondo.get_rect().width, 0))
        if mover < SCREEN_WIDTH:
            screen.blit(fondo, (mover, 0))

        movimentFondo -= 1

        # Aumentar la creacio dels enemics segons el nivell
        creacioEne = int(50 + (450 / nivel))
        if crear != creacioEne:
            crear = creacioEne
            pygame.time.set_timer(ADDENEMY, crear)

        pressed_keys = pygame.key.get_pressed()
        player.update(pressed_keys)

        # Actualizem els nuvols
        clouds.update()

        # Actualizem els enemics
        enemies.update()

        # Per a controlar al jugador
        player.update(pressed_keys)

        # Dibuixa els sprites
        for entity in all_sprites:
            screen.blit(entity.surf, entity.rect)

        # Colisió del jugador
        if pygame.sprite.spritecollideany(player, enemies):
            # If so, then remove the player and stop the loop
            collision_sound.play()
            time.sleep(1)
            conectar()
            print(f"Record: {lSQL()}")
            print("--------------------------------------------")
            uSQL()

            player.kill()
            running = False

        # Mostrem els punts que portem y el nivell
        mostar(screen, "Puntos ", str(punts), 30, 950, 30)
        mostar(screen, "Nivel ", str(nivel), 30, 950, 80)

        pygame.display.flip()
        clock.tick(fps)

    # Musica per a la pantalla final
    pygame.mixer.music.load(os.path.join(resources, "MusicaMenu.ogg"))
    pygame.mixer.music.play(loops=-1)
    pygame.mixer.music.set_volume(0.1)

    # Bucle per a la pantalla final
    while menuFinal:
        for i in pygame.event.get():
            if i.type == pygame.QUIT:
                quit()

        # Fons del final del joc
        fondoMenu = pygame.image.load(os.path.join(resources, "GameOver.jpg")).convert()
        fondoMenu1 = pygame.transform.scale(fondoMenu, (SCREEN_WIDTH, SCREEN_HEIGHT))
        screen.blit(fondoMenu1, (0, 0))

        # Format de la pantalla final
        texto = pygame.font.SysFont("serif", 40).render("Si quieres volver a jugar pulse 'S'", 1, blanc)
        screen.blit(texto, (230, 400))

        ultimo = pygame.font.SysFont("arial", 25).render(f"Record: {lSQL()}", 1, roig)
        screen.blit(ultimo, (10, 10))

        punt = pygame.font.SysFont("arial", 25).render(f"Puntuación: {punts}", 1, roig)
        screen.blit(punt, (10, 50))

        eixir = pygame.font.SysFont("serif", 40).render("Pulsa 'E' para salir", 1, blanc)
        screen.blit(eixir, (10, 550))

        # Si apretes la s tornes a començar
        if pygame.key.get_pressed()[pygame.K_s]:
            menuFinal = False

        # Si apretes la e s'acaba el joc
        if pygame.key.get_pressed()[pygame.K_e]:
            menuFinal = False
            empezar = False

        pygame.display.update()

# Final del joc
pygame.mixer.music.stop()
pygame.mixer.quit()
pygame.quit()
