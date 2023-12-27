import pygame
from modelo.imgs.path_imgs import *
from modelo.music.music_path import *


class JogoMario(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.caminho_absoluto = caminho()
        self.path_music = path_music()
        self.music_jump = pygame.mixer.Sound(os.path.join(self.path_music, "jump.wav"))
        self.music_gamer_over = pygame.mixer.Sound(os.path.join(self.path_music, "game_over.mp3"))
        sprite_sheet = pygame.image.load(os.path.join(self.caminho_absoluto, 'mario.png')).convert_alpha()

        self.gamer_over_image = pygame.image.load(os.path.join(self.caminho_absoluto, 'game-over.png'))

        # mario caminhando
        self.img1 = sprite_sheet.subsurface((481, 12), (78, 100))  # parado
        self.img2 = sprite_sheet.subsurface((409, 12), (78, 100))  # inicio da caminhada
        self.img3 = sprite_sheet.subsurface((329, 12), (78, 100))  # caminhado dois
        self.img4 = sprite_sheet.subsurface((249, 12), (78, 100))  # caminhado tres

        # salto do mario
        self.img5 = sprite_sheet.subsurface((223, 115), (78, 100))  # primeira img do salto
        self.img6 = sprite_sheet.subsurface((370, 115), (78, 100))  # pulando maos pra baixo
        self.img7 = sprite_sheet.subsurface((450, 115), (78, 100))  # pulando maos pra cima
        self.img8 = sprite_sheet.subsurface((8, 12), (78, 100))     # descendo do pulo
        self.img9 = sprite_sheet.subsurface((180, 12), (78, 100))   # caiu no chao

        self.mario = [

            self.img1,
            self.img2,
            self.img3,
            # self.img4 # aqui ta levantando o braço quando coloca, vai de cada um
        ]

        self.mario_salto = [
            # sem self.img5            # tirando primeira img do salto
            self.img6,            # pulando com as maos pra baixo
            self.img7,  # com as maos pra cima
            # sem self.img8,  # descendo no pulo
            # sem self.img9   # caiu no chao
        ]

        self.animation = 0
        self.animation_movimento = 0
        self.image = self.mario[self.animation]
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.animation_timer = pygame.time.get_ticks()
        self.pos_y_inicial = 400
        self.rect.topleft = 0, 400
        self.salto = False
        self.tocando_musica = False

    def jump(self):
        self.salto = True
        self.music_jump.play()

    def update(self):
        # mario andando
        if self.animation > (len(self.mario) - 1):
            self.animation = 0
        self.animation += 0.25
        self.image = self.mario[int(self.animation)]

        # mario saltando
        if self.salto:
            self.image = self.img5
            if self.rect.y <= 220:
                self.image = self.img6
                self.salto = False
            self.rect.y -= 15
        else:
            if self.rect.y < self.pos_y_inicial:
                if self.animation_movimento > (len(self.mario_salto) - 1):
                    self.animation_movimento = 0
                self.animation_movimento += 0.30
                self.image = self.mario_salto[int(self.animation_movimento)]
                self.rect.y += 10
            else:
                self.rect.y = self.pos_y_inicial

    def gamer_over(self):
        self.image = self.gamer_over_image
        self.image = pygame.transform.scale(self.image, (231 // 4.2, 347 // 4.2))
        self.music_gamer_over.play()


class Nuvens(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.caminho_absoluto = caminho()
        self.desenhando_nuvens = pygame.image.load(os.path.join(self.caminho_absoluto, 'clouds.png')).convert_alpha()
        self.image = self.desenhando_nuvens
        self.image = pygame.transform.scale(self.image, (1084//5, 498//5))
        self.rect = self.image.get_rect()
        self.rect.center = 600, 70
        self.velocidade = 10
        self.passou = 0

    def update(self):
        if self .rect.topright[0] < 0:
            self.rect.x = 600
            self.passou += 10
            if self.passou % 100 == 0:
                if self.velocidade >= 23:
                    self.velocidade += 0
                else:
                    self.velocidade += 1
        self.rect.x -= self.velocidade


class BackGround(pygame.sprite.Sprite):
    def __init__(self, pos_x):
        pygame.sprite.Sprite.__init__(self)
        self.caminho_absoluto = caminho()
        self.path_music = path_music()
        pygame.mixer.music.load(os.path.join(self.path_music, "music_background.mp3"))
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1)
        self.fundo = pygame.image.load(os.path.join(self.caminho_absoluto, 'background.jpg'))
        self.image = self.fundo
        self.rect = self.image.get_rect()
        self.rect.y = 0
        self.rect.x = pos_x * 600
        self.animation_timer = pygame.time.get_ticks()

    def update(self):
        if self.rect.topright[0] <= 0:
            self.rect.x = 600
        self.rect.x -= 10


class Cano(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.numero = 1
        self.caminho_absoluto = caminho()
        self.path_music = path_music()
        self.musica_100_pontuacao = pygame.mixer.Sound(os.path.join(self.path_music, "rum_victory.mp3"))
        self.cano = pygame.image.load(os.path.join(self.caminho_absoluto, 'pipe.png')).convert_alpha()
        self.image = self.cano
        self.image = pygame.transform.scale(self.image, (293//4.7, 375//4.7))
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.topleft = 600, 409
        self.velocidade = 10
        self.pontuacao = 0

    def update(self):
        if self.rect.topright[0] <= 0:
            self.rect.x = 600
            self.pontuacao += 10
            if self.pontuacao % 100 == 0:
                self.musica_100_pontuacao.play()
                if self.velocidade >= 23:
                    self.velocidade += 0
                else:
                    self.velocidade += 1
        self.rect.x -= self.velocidade


class MenuJogo(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.caminho_absoluto = caminho()
        self.titulo = pygame.image.load(os.path.join(self.caminho_absoluto, 'tittle.webp')).convert_alpha()
        self.image = self.titulo
        self.image = pygame.transform.scale(self.image, (1980 // 5, 1080 // 5))
        self.rect = self.image.get_rect()
        self.rect.center = 300, 180