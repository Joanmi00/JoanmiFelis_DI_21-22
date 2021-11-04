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
        global score
        global nivel
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            for e in enemies:
                if e.rect.right <= 1:
                    score += 10
                    if score % 500 == 0:
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

        # Keep player on the screen
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

    # Inicia el juego
    pygame.init()

    # ruta de la carpeta de recursos
    resources = os.path.join(os.path.dirname(__file__), "resources")


    #
    def marcador(surface, text, text2, size, x, y):

        font = pygame.font.SysFont("arial", size)  # fuente del marcador
        if Fondos == True:
            text_surface = font.render("{} : {}".format(text, text2), True, negre)  # color y tamaño de la letra
        elif Fondos == False:
            text_surface = font.render("{} : {}".format(text, text2), True, blanc)
        text_rect = text_surface.get_rect()
        text_rect.midright = (x, y)
        surface.blit(text_surface, text_rect)


    # Conexion DB
    def conectar():
        try:
            sqliteConnection = sqlite3.connect((os.path.join(resources, "puntuacion.db")))
            return sqliteConnection
        except Error:
            print(Error)


    con = conectar()


    # insertar datos para nueva puntuacion
    def iSQL(punts):
        obj = con.cursos()
        if lSQL() == 0:
            obj.execute('INSERT INTO puntuacion VALUES({})'.format(score))

        if lSQL() > punts:
            return
        else:
            uSQL()

        con.comit()


    def lSQL():
        cursor = con.cursor()
        cursor.execute("SELECT score FROM puntuacion")
        row = cursor.fetchone()
        return row[0]


    def uSQL():
        curs = con.cursor()
        if lSQL() > punts:
            print("Record no superado")
            print("Puntuacion: " + str(punts))
        if lSQL() < punts:
            curs.execute("Update puntuacion set score = " + str(punts))
            print("Nuevo record: ", punts)
            curs.execute("select * from puntuacion")
            con.commit()

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

    punts = 0
    nivel = 1

    # Afegir els nuvols
    ADDCLOUD = pygame.USEREVENT + 2
    pygame.time.set_timer(ADDCLOUD, 2000)

    ADDENEMY = pygame.USEREVENT + 1

    # Instantiate player. Right now, this is just a rectangle.
    player = Player()

    # Create groups to hold enemy sprites and all sprites
    # - enemies is used for collision detection and position updates
    # - all_sprites is used for rendering
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

    pygame.mixer.music.load(os.path.join(resources, "MusicaMenu.ogg"))
    pygame.mixer.music.play(loops=-1)  # Se reproduzca infinitamente
    pygame.mixer.music.set_volume(0.1)  # volumen del juego

    while menu:

        for i in pygame.event.get():
            if i.type == pygame.QUIT:
                quit()

        fondoMenu = pygame.image.load(os.path.join(resources, "fondoMenu.png")).convert()
        screen.blit(fondoMenu, (0, 0))

        textoNombre = pygame.image.load(os.path.join(resources, "NombreJuego.png")).convert()
        textoNombre.set_colorkey(negre, RLEACCEL)
        screen.blit(textoNombre, (300, 50))

        texto = pygame.font.SysFont("none", 60).render("Pulsa 'p' para jugar", 1, negre)
        screen.blit(texto, (310, 250))

        # ultimo = pygame.font.SysFont("arial", 25).render(f"Maxima Puntuación: {leersql()}", 1, roig)
        # screen.blit(ultimo, (400, 250))

        eixir = pygame.font.SysFont("serif", 40).render("Pulsa 'ESC' para salir", 1, negre)
        screen.blit(eixir, (10, 550))

        if pygame.key.get_pressed()[pygame.K_p]:
            menu = False

        if pygame.key.get_pressed()[pygame.K_ESCAPE]:
            menu = False
            running = False
            menuFinal = False
            empezar = False

        pygame.display.update()

    # Agrega una image de fondo
    fondo = pygame.image.load(os.path.join(resources, "Fondo1.jpg")).convert()
    Fondos = True

    # Cambio de fondo del juego
    ADDTIME = pygame.USEREVENT + 3
    pygame.time.set_timer(ADDTIME, 20000)

    # Setup fr sounds.Default are good.
    pygame.mixer.init()

    # Load and play background music
    pygame.mixer.music.load(os.path.join(resources, "Chiptronical.ogg"))
    pygame.mixer.music.play(loops=-1)  # Se reproduzca infinitamente
    pygame.mixer.music.set_volume(0.1)  # volumen del juego

    # Load all sound files
    # Sound sources: Jon Fincher
    collision_sound = pygame.mixer.Sound(os.path.join(resources, "Collision.wav"))

    # Variable per al fondo en moviment
    movimentFondo = 0
    crear = 0

    # Main loop
    while running:
        # for loop through the event queue
        for event in pygame.event.get():
            # Check for KEYDOWN event
            if event.type == KEYDOWN:
                # If the Esc key is pressed, then exit the main loop
                if event.key == K_ESCAPE:
                    running = False
            elif event.type == QUIT:
                quit()
            # Add a new enemy?
            elif event.type == ADDENEMY:
                # Create the new enemy and add it to sprite groups
                new_enemy = Enemy()
                enemies.add(new_enemy)
                all_sprites.add(new_enemy)
            # Add a new cloud
            elif event.type == ADDCLOUD:
                # Create the new cloud and add it to sprite groups
                new_cloud = Cloud()
                clouds.add(new_cloud)
                all_sprites.add(new_cloud)
            # Add a new background color
            elif event.type == ADDTIME:
                if Fondos:
                    Fondos = False
                    fondo = pygame.image.load(os.path.join(resources, "Fondo2.jpg")).convert()
                elif not Fondos:
                    Fondos = True
                    fondo = pygame.image.load(os.path.join(resources, "Fondo1.jpg")).convert()

        # UPDATE ENEMY
        creacioEne = int(50 + (450 / nivel))
        if crear != creacioEne:
            crear = creacioEne
            pygame.time.set_timer(ADDENEMY, crear)

        mover = movimentFondo % fondo.get_rect().width
        screen.blit(fondo, (mover - fondo.get_rect().width, 0))
        if mover < SCREEN_WIDTH:
            screen.blit(fondo, (mover, 0))

        movimentFondo -= 1
        # Get the set of keys pressed and check for user input
        pressed_keys = pygame.key.get_pressed()
        player.update(pressed_keys)

        # update cloud position
        clouds.update()

        # Update enemy position
        enemies.update()

        # Update the player sprite based on user keypresses
        player.update(pressed_keys)

        # Draw all sprites
        for entity in all_sprites:
            screen.blit(entity.surf, entity.rect)

        # COLISION
        # Check if any enemies have collided with the player
        if pygame.sprite.spritecollideany(player, enemies):
            # If so, then remove the player and stop the loop
            collision_sound.play()
            time.sleep(1)
            conectar()
            print("\n--------------------------------------------")
            print(f"Record: {lSQL()}")
            print("--------------------------------------------")
            uSQL()

            player.kill()
            running = False

        marcador(screen, "Puntos: ", str(punts), 30, 950, 30)
        marcador(screen, "Nivel: ", str(nivel), 30, 950, 80)

        # Update the display
        pygame.display.flip()
        clock.tick(fps)

    pygame.mixer.music.load(os.path.join(resources, "MusicaMenu.ogg"))
    pygame.mixer.music.play(loops=-1)  # Se reproduzca infinitamente
    pygame.mixer.music.set_volume(0.1)  # volumen del juego

    while menuFinal:
        for i in pygame.event.get():
            if i.type == pygame.QUIT:
                quit()

        fondoMenu = pygame.image.load(os.path.join(resources, "GameOver.jpg")).convert()
        fondoMenu1 = pygame.transform.scale(fondoMenu, (SCREEN_WIDTH, SCREEN_HEIGHT))
        screen.blit(fondoMenu1, (0, 0))

        texto = pygame.font.SysFont("serif", 40).render("Si quieres volver a jugar pulse 'S'", 1, blanc)
        screen.blit(texto, (230, 400))

        ultimo = pygame.font.SysFont("arial", 25).render(f"Record: {lSQL()}", 1, roig)
        screen.blit(ultimo, (10, 10))

        punt = pygame.font.SysFont("arial", 25).render(f"Puntuación: {punts}", 1, roig)
        screen.blit(punt, (10, 50))

        eixir = pygame.font.SysFont("serif", 40).render("Pulsa 'N' para salir", 1, blanc)
        screen.blit(eixir, (10, 550))

        if pygame.key.get_pressed()[pygame.K_s]:
            menuFinal = False

        if pygame.key.get_pressed()[pygame.K_n]:
            menuFinal = False
            empezar = False

        pygame.display.update()

# All done! Stop and quit the mixer.
pygame.mixer.music.stop()
pygame.mixer.quit()
pygame.quit()
