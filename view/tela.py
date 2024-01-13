import pygame.sprite
from controller.extrutura import *
from sys import exit
from pygame.locals import *

# CONSTANTES NO PYTHON
LARGURA = 600
ALTURA = 500
TITULO = "MARIOS BROS (Luiz Felipe)"
BRANCO = (255, 255, 255)
FPS = 30

pygame.init()

tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption(TITULO)
relogio = pygame.time.Clock()

todas_as_sprites = pygame.sprite.Group()
obstaculos = pygame.sprite.Group()
sprite_menu_incial = pygame.sprite.Group()
sprite_titulo = pygame.sprite.Group()

fundo_branco = pygame.surface.Surface((LARGURA, ALTURA), pygame.SRCALPHA)
fundo_branco = tela.fill((255, 255, 255, 102))

for contador in range(2):
    chao = BackGround(contador)
    todas_as_sprites.add(chao)
    sprite_menu_incial.add(chao)

jogo_mario = JogoMario()
todas_as_sprites.add(jogo_mario)
sprite_menu_incial.add(jogo_mario)

nuvens = Nuvens()
todas_as_sprites.add(nuvens)
sprite_menu_incial.add(nuvens)

cano = Cano()
todas_as_sprites.add(cano)
obstaculos.add(cano)

menu = MenuJogo()
sprite_titulo.add(menu)


def reiniciar_jogo():
    cano.rect.topleft = 600, 409
    nuvens.rect.center = 600, 70
    cano.pontuacao = 0
    jogo_mario.rect.topleft = 0, 400
    jogo_mario.image = jogo_mario.mario[0]
    cano.velocidade = 10 


def exibe_mensagem(mensagem, tamanho_fonte, cor_texto, cor_fundo, posicao, tm1, tm2):
    fonte = pygame.font.SysFont("comicsansms", tamanho_fonte, True, False)
    msg = f"{mensagem}"
    texto_formatado = fonte.render(msg, True, cor_texto)
    retangulo_texto = texto_formatado.get_rect()
    retangulo_texto.center = posicao

    # Crie uma superfície para o fundo preto transparente
    largura_fundo = retangulo_texto.width + tm1
    altura_fundo = retangulo_texto.height + tm2
    fundo = pygame.Surface((largura_fundo, altura_fundo), pygame.SRCALPHA)
    pygame.draw.rect(fundo, cor_fundo, (0, 0, largura_fundo, altura_fundo), border_radius=5)

    # Combine a superfície do fundo com a superfície do texto
    fundo.blit(texto_formatado, (tm1 // 2, tm2 // 2))
    retangulo_fundo = fundo.get_rect(center=posicao)

    return fundo, retangulo_fundo



def main():
    colidiu = False
    menu = True
    while True:
        relogio.tick(FPS)
        tela.fill(BRANCO)
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == K_SPACE and colidiu == False:
                    if jogo_mario.rect.y != jogo_mario.pos_y_inicial:
                        pass
                    else:
                        jogo_mario.jump()
                if event.key == K_r and colidiu == True:
                    reiniciar_jogo()
                    colidiu = False
                if event.key == K_RETURN:
                    menu = False

        if menu:
            sprite_menu_incial.draw(tela)
            FUNDO_PRETO, RECT = exibe_mensagem(
                " ",
                40,
                (255, 0, 0),
                (0, 0, 0, 180),
                (LARGURA - 300, ALTURA - 270),
                LARGURA,
                ALTURA + 50
            )
            texto1, RECT2 = exibe_mensagem(
                "Aperte ENTER pra começar",
                20,
                (255, 0, 0),
                (0, 0, 0, 0),
                (LARGURA - 300, ALTURA - 210),
                LARGURA,
                ALTURA + 50
            )
            tela.blit(FUNDO_PRETO, RECT)
            sprite_titulo.draw(tela)
            tela.blit(texto1, RECT2)
            sprite_menu_incial.update()
        else:

            colisoes = pygame.sprite.collide_mask(jogo_mario, cano)
            todas_as_sprites.draw(tela)

            if colisoes and colidiu != True:
                jogo_mario.gamer_over()
                colidiu = True
            elif colidiu:
                FUNDO_PRETO, RECT = exibe_mensagem(
                    "GAME OVER",
                    40,
                    (255, 0, 0),
                    (0, 0, 0, 230),
                    (LARGURA - 300, ALTURA - 270),
                    LARGURA,
                    ALTURA + 50
                )
                INITI, RECT2 = exibe_mensagem(
                    "Aperte R pra começar",
                    25,
                    (255, 255, 255),
                    (0, 0, 0, 0),
                    (LARGURA - 300, ALTURA - 270 + 35),
                    LARGURA,
                    ALTURA + 50
                )
                tela.blit(FUNDO_PRETO, RECT)
                tela.blit(INITI, RECT2)
            else:
                todas_as_sprites.update()
                STRING_PONTUACAO, rectangle = exibe_mensagem(
                    "PONTUACÃO:",
                    15,
                    (255, 255, 255),
                    (0, 0, 0, 200),
                    (500, 50),
                    50,
                    30
                )
                PONTUACAO, retangulo = exibe_mensagem(
                    cano.pontuacao,
                    13,
                    (255, 255, 255),
                    (0, 0, 0, 200),
                    (500, 100),
                    144,
                    30
                )

                tela.blit(STRING_PONTUACAO, rectangle)
                tela.blit(PONTUACAO, retangulo)

        pygame.display.flip()
