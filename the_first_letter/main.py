
import os
import random
# import time

import pygame

DEBUG = False
HIDE_LAST_LETTER = False   # Hides letter of last correct box
HIDE_ALL_LETTERS = False  # Does not show any letter

# init variables
pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption('The First Letter')
icon = pygame.image.load('controller-pad.png')
pygame.display.set_icon(icon)
images = {}
font64 = pygame.font.Font('freesansbold.ttf', 64)
font84 = pygame.font.Font('freesansbold.ttf', 84)
playing = [None]*4
# pygame.mixer.music.load( 'backgound.wav' )
# pygame.mixer.music.play( -1 )
errorimage = pygame.image.load('error-256.png')
winimage = pygame.image.load('win-256.png')
errorcount = 0
lastok = 5
latestletters = ""


class PlayImage(object):

    px = 0   # image position
    py = 0
    lx = 0   # letter position
    ly = 0
    ll = ''  # letter
    ix = 0   # index of image array
    tmpimg = None

    def __init__(self):
        if DEBUG:
            print("Init PlayImage")
        pass

    def __del__(self):
        if DEBUG:
            print("Deleted PlayImage")
        pass

    def set_pos_tuple(self, t=None):
        self.px = t[0]
        self.py = t[1]

    def set_pos(self, x=None, y=None):
        self.set_pos_tuple((x, y))

    def set_letter(self, letter=None):
        self.ll = letter
        if letter is not None:
            self.ix = random.randint(0, len(images[letter])-1)
            self.lx = 300
            self.ly = 250

    def get_text(self):
        return images[self.ll][self.ix][1]

    def get_sound(self):
        return images[self.ll][self.ix][2]

    def adjust_letter_pos(self, x=None, y=None):
        self.lx = self.lx + x
        if self.lx > 320:
            self.lx = 320
        if self.lx < 280:
            self.lx = 280
        self.ly = self.ly + y
        if self.ly > 270:
            self.ly = 270
        if self.ly < 230:
            self.ly = 230

    def get_letter(self):
        return self.ll

    def is_letter(self, letter=None):
        return self.ll == letter

    def temp_image(self, img=None):
        self.tmpimg = img

    def get_temp_image(self):
        return self.tmpimg is not None

    def blit_image(self, showletter=True):
        if self.tmpimg is None:
            screen.blit(images[self.ll][self.ix][0],
                        (self.px+75, self.py+25))
            if showletter:
                txt = font64.render(self.ll.upper(), True, (0, 0, 0))
                trec = txt.get_rect()
                trec.center = (int(self.px+self.lx-2), int(self.py+self.ly-2))
                screen.blit(txt, trec)
                txt = font64.render(self.ll.upper(), True, (255, 255, 255))
                trec = txt.get_rect()
                trec.center = (int(self.px+self.lx), int(self.py+self.ly))
                screen.blit(txt, trec)
        else:
            screen.blit(self.tmpimg, (self.px+75, self.py+25))


def add_playimage(letter=None, txt=None, fname=None):
    e = ""
    if not os.path.isfile("images/{}-256.png".format(fname)):
        e = "{} missing image file;".format(e)
    if not os.path.isfile("sounds/{}.wav".format(fname)):
        e = "{} missing sound file;".format(e)
    if len(e) > 0:
        if DEBUG:
            print("not adding={}; {}".format(fname, e))
        return False
    if letter not in images.keys():
        images[letter] = []
    images[letter].append(
          (pygame.image.load("images/{}-256.png".format(fname)),
           txt, "sounds/{}.wav".format(fname)
           )
    )
    if DEBUG:
        print("adding={}".format(fname))
    return True


def random_letter():
    global latestletters
    al = list(images.keys())
    av = []
    if DEBUG:
        print("al={}".format(al))
        print("ll={}".format(latestletters))
    for le in al:
        for i in range(4):
            if playing[i] is not None:
                if playing[i].get_letter() == le:
                    le = None
        if (le is not None) and (le not in latestletters):
            av.append(le)
        if DEBUG:
            print("av={}".format(av))
    if len(av) > 0:
        r = av[random.randint(0, len(av)-1)]
    else:
        r = None
    if DEBUG:
        print("r={}".format(r))
    return r


def playing_letters():
    r = []
    for i in range(4):
        if playing[i] is not None:
            r.append(playing[i].get_letter())
    return r


def index_to_pos(idx=None):
    if idx == 0:
        return (0, 0)
    if idx == 1:
        return (400, 0)
    if idx == 2:
        return (0, 300)
    if idx == 3:
        return (400, 300)
    return (None, None)


# MAIN #
for ai in [('a', 'Abeja', 'abeja'),
           ('a', 'Auto de Carreras', 'auto-carrera'),
           ('a', 'Avión', 'avion'),
           ('b', 'Ballena', 'ballena'),
           ('b', 'Banana', 'banana'),
           ('b', 'Barco', 'barco'),
           ('c', 'Caramelo', 'caramelo'),
           ('c', 'Corazón', 'corazon'),
           ('c', 'Conejo', 'conejo'),
           ('d', 'Delfín', 'delfin'),   # record
           ('d', 'Dinosaurio', 'dinosaurio'),  # record
           ('e', 'Elefante', 'elefante'),
           ('e', 'Estrella', 'estrella'),  # record
           ('f', 'Faro', 'faro'),   # record
           ('f', 'Flores', 'flores'),
           ('g', 'Gato', 'gato'),
           ('g', 'Guitarra', 'guitarra'),
           ('h', 'Helado', 'helado'),
           ('h', 'Helicoptero', 'helicoptero'),
           ('h', 'Hipopotamo', 'hipo'),
           ('i', 'Iguana', 'iguana'),
           ('i', 'Imán', 'iman'),
           ('i', 'Isla', 'isla'),
           ('j', 'Jirafa', 'jirafa'),
           ('j', 'Juguito', 'juguito'),
           ('k', 'Ketchup', 'ketchup'),
           ('k', 'Kiwi', 'kiwi'),
           ('k', 'Koala', 'koala'),
           ('l', 'Leon', 'leon'),
           ('l', 'Limon', 'limon'),
           ('l', 'Linterna', 'linterna'),
           ('l', 'Loro', 'loro'),
           ('m', 'Mano', 'mano'),
           ('m', 'Manzana', 'manzana'),
           ('m', 'Mariposa', 'mariposa'),
           ('m', 'Mickey', 'mickey'),
           ('m', 'Moño', 'monio'),
           ('n', 'Naranja', 'naranja'),
           ('n', 'Nido', 'nido'),
           ('n', 'Nubes', 'nubes'),
           ('n', 'Nuez', 'nuez'),
           ('o', 'Ojo', 'ojo'),
           ('o', 'Olla', 'olla'),
           ('o', 'Oso', 'oso'),
           ('o', 'Oveja', 'oveja'),
           ('p', 'Palmera', 'palmera'),
           ('p', 'Paragüas', 'paraguas'),
           ('p', 'Pato', 'pato'),
           ('p', 'Pez', 'pez'),
           ('p', 'Pingüino', 'pinguino'),
           ('q', 'Queso', 'queso'),
           ('q', 'Querubín', 'querubin'),  # record
           ('q', 'Quetzal', 'quetzal'),  # record
           ('q', 'Quinoa', 'quinoa'),    # record
           ('r', 'Rio', 'rio'),   # record
           ('r', 'Ratón', 'raton'),
           ('r', 'Regalo', 'regalo'),   # record
           ('r', 'Rana', 'rana'),
           ('s', 'Silla', 'silla'),
           ('s', 'Sandia', 'sandia'),
           ('s', 'Sombrero', 'sombrero'),
           ('t', 'Teléfono', 'telefono'),   # record
           ('t', 'Televisión', 'television'),  # record
           ('t', 'Tenedor', 'tenedor'),    # record
           ('t', 'Tigre', 'tigre'),       # record
           ('u', 'Uniciclo', 'uniciclo'),  # record
           ('u', 'Uña', 'unia'),           # record
           ('u', 'Uvas', 'uvas'),            # record
           ('u', 'Unicornio', 'unicornio'),  # record
           ('v', 'Vaca', 'vaca'),            # record
           ('v', 'Vela', 'vela'),            # record
           ('v', 'Vestido', 'vestido'),      # record
           ('v', 'Volcán', 'volcan'),        # record
           ('w', 'Whiskey', 'whiskey'),      # record
           ('w', 'Waffle', 'waffle'),        # record
           ('w', 'Wallabe', 'wallabe'),      # record
           ('w', 'Windsurf', 'windsurf'),    # record
           ('x', 'Xilofón', 'xilofon'),      # record
           ('x', 'X-Box', 'xbox'),           # record
           ('y', 'Yate', 'yate'),
           ('y', 'Yo-Yo', 'yoyo'),
           ('y', 'Yogurt', 'yogurt'),        # record
           ('z', 'Zancos', 'zancos'),        # record
           ('z', 'Zanahorias', 'zanahorias'),  # record
           ('z', 'Zapatillas', 'zapatillas'),  # record
           ('z', 'Zorro', 'zorro')           # record
           ]:
    add_playimage(ai[0], ai[1], ai[2])

for i in range(4):
    playing[i] = PlayImage()
    playing[i].set_pos_tuple(index_to_pos(i))
    playing[i].set_letter(random_letter())

running = True
whilesound = None
f = 0
while running:
    keypressed = None
    for event in pygame.event.get():
        if DEBUG:
            print("event = {}".format(event))
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.TEXTINPUT:
            keypressed = event.text.lower()
            if DEBUG:
                print("text = {}".format(keypressed))
            if keypressed in playing_letters():
                if DEBUG:
                    print("you win")
                errorcount = 0
                latestletters = "{}{}".format(keypressed, latestletters)[0:12]
            else:
                if errorcount < 10:
                    if errorcount < 7:
                        pygame.mixer.music.load('error-eseno.wav')
                    else:
                        pygame.mixer.music.load('error-buzz.wav')
                    pygame.mixer.music.play()
                    whilesound = pygame.Surface((800, 300),
                                                pygame.SRCALPHA, 32)
                    whilesound.blit(errorimage, (400-125, 0))
                    errorcount = errorcount + 1
                keypressed = None
                if DEBUG:
                    print("you loose")

    screen.fill((50, 50, 50))
    for x in range(4):
        playing[x].blit_image(((x != lastok) or (not HIDE_LAST_LETTER)) and
                              (not HIDE_ALL_LETTERS))
        playing[x].adjust_letter_pos(2*(random.random()-0.5),
                                     random.random()-0.5)
        if playing[x].get_letter() == keypressed:
            lastok = x
            whilesound = pygame.Surface((800, 300), pygame.SRCALPHA, 32)
            txt = font84.render(playing[x].get_text(), True, (0, 0, 0))
            trec = txt.get_rect()
            trec.center = (398, 148)
            whilesound.blit(txt, trec)
            trec.center = (402, 152)
            whilesound.blit(txt, trec)
            txt = font84.render(playing[x].get_text(), True, (255, 0, 128))
            trec = txt.get_rect()
            trec.center = (400, 150)
            whilesound.blit(txt, trec)
            playing[x].temp_image(winimage)
            if playing[x].get_sound() is None:
                pygame.mixer.music.load('backgound.wav')
            else:
                pygame.mixer.music.load(playing[x].get_sound())
            pygame.mixer.music.play()

    if whilesound is not None:
        if pygame.mixer.music.get_busy():
            screen.blit(whilesound, (0, 300-125))
        else:
            whilesound = None
            for x in range(4):
                if playing[x].get_temp_image():
                    playing[x].set_letter(None)
                    playing[x].temp_image(None)
                    playing[x].set_letter(random_letter())

    pygame.display.update()
    clock.tick(10)

pygame.quit()
