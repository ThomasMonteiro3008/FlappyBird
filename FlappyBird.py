import pygame
import os
import random

TELA_LARGURA = 500
TELA_ALTURA = 800

IMAGEM_TUBO= pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'pipe.png')))
IMAGEM_CHAO= pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'base.png')))
IMAGEM_FUNDO= pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'bg.png')))
IMAGENS_PASSARO= [pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'bird1.png'))),
                  pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'bird2.png'))),
                  pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'bird3.png')))]

pygame.font.init()
FONTE_PONTOS = pygame.font.SysFont('arial', 50)


class Passaro:
    imgs = IMAGENS_PASSARO
    rotacao_maxima = 25
    velocidade_rotacao = 20
    tempo_animacao = 5

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.angulo = 0
        self.velocidade = 0
        self.altura = self.y
        self.tempo = 0
        self.contagem_img = 0
        self.imagem = self.imgs[0]

    def pular(self):
        self.velocidade = -10.5
        self.tempo = 0
        self.atura = self.y

    def movimento(self):
        self.tempo += 1
        deslocamento = 1.5 * (self.tempo**2) + self.velocidade * self.tempo

        #restricao do deslocamento
        if deslocamento > 16:
            deslocamento = 16
        elif deslocamento < 0:
            deslocamento -= 2

        self.y += deslocamento

        if deslocamento < 0 or self.y < (self.altura + 50):
            if self.angulo < self.rotacao_maxima:
                self.angulo = self.rotacao_maxima

        else:
            if self.angulo > -90:
                self.angulo -= self.velocidade_rotacao

    def desenhar(self, tela):

        #Definimos qual imagem do pássaro será utilizada

        self.contagem_img += 1

        if self.contagem_img < self.tempo_animacao:
            self.imagem = self.imgs[0]
        elif self.contagem_img < self.tempo_animacao*2:
            self.imagem = self.imgs[1]
        elif self.contagem_img < self.tempo_animacao*3:
            self.imagem = self.imgs[2]
        elif self.contagem_img < self.tempo_animacao*4:
            self.imagem = self.imgs[1]
        elif self.contagem_img < self.tempo_animacao*4 + 1:
            self.imagem = self.imgs[0]
            self.contagem_img = 0

        #Pássaro em queda não bate asas
        if self.angulo <= 80:
            self.imagem = self.imgs[1]
            self.contagem_img = self.tempo_animacao*2

        #Desenhar imagem
        imagem_rotacionada = pygame.transform.rotate(self.imagem, self.angulo)
        pos_centro_img = self.imagem.get_rect(topleft=(self.x, self.y)).center
        retangulo = imagem_rotacionada.get_rect(center= pos_centro_img)
        tela.blit(imagem_rotacionada, retangulo.topleft)

    def get_mask(self):
        return pygame.mask.from_surface(self.imagem)


class Tubo:
    distancia =  200
    velocidade = 5

    def __init__(self,x):
        self.x = x
        self.altura = 0
        self.topo = 0
        self.base = 0
        self.TUBO_topo = pygame.transform.flip(IMAGEM_TUBO, False, True)
        self.TUBO_base = IMAGEM_TUBO
        self.passou = False
        self.definir_altura()

    def definir_altura(self):
        self.altura = random.randrange(50,450)
        self.pos_topo = self.altura - self.TUBO_topo.get_height()
        self.pos_base = self.altura + self.distancia

    def mover(self):
        self.x -= self.velocidade

    def desenhar(self, tela):
        tela.blit(self.TUBO_topo, (self.x, self.pos_topo))
        tela.blit(self.TUBO_base, (self.x, self.pos_base))

    def colidir(self, passaro):
        passaro_mask = passaro.get_mask()
        topo_mask = pygame.mask.from_surface(self.TUBO_topo)
        base_mask = pygame.mask.from_surface(self.TUBO_base)

        distancia_topo = (self.x - passaro.x, self.pos_topo - round(passaro.y) )
        distancia_base = (self.x - passaro.x, self.pos_base - round(passaro.y) )

        topo_ponto = passaro_mask.overlap(topo_mask, distancia_topo)
        base_ponto = passaro_mask.overlap(base_mask, distancia_base)

        if topo_ponto or base_ponto:
            return True
        else:
            return False


class Chao:
    velocidade = 5
    largura = IMAGEM_CHAO.get_width()
    imagem = IMAGEM_CHAO

    def __init__(self, y):
       self.y = y
       self.x0 = 0
       self.x1 = self.largura

    def mover(self):
        self.x0 -= self.velocidade
        self.x1 -= self.velocidade

        if self.x0 + self.largura < 0:
            self.x0 = self.x1 + self.largura
        if self.x1 + self.largura < 0:
            self.x1 = self.x0 + self.largura

    def desenhar(self, tela):
        tela.blit(self.imagem, (self.x0, self.y))
        tela.blit(self.imagem, (self.x1, self.y))

def desenhar_tela(tela, passaros, tubos, chao, pontos):
    tela.blit(IMAGEM_CHAO, (0,0))
    for passaro in passaros:
        passaro.desenhar(tela)
    for tubo in tubos:
        tubo.desenhar(tela)
    texto = FONTE_PONTOS.render(f"Pontuação: {pontos}", 1, (255, 255, 255))
    tela.blit(texto, (TELA_LARGURA - 10 - texto.get_width(), 10))
    chao.desenhar(tela)
    pygame.display.update()

def main():
    passaros = [Passaro(230, 350)]
    chao = Chao(730)
    tubos = [Tubo(700)]
    tela = pygame.display.set_mode((TELA_LARGURA, TELA_ALTURA))
    pontos = 0
    relogio = pygame.time.Clock()

    loading = True
    while loading:
        relogio.tick(30)

        # intergindo com o player
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                loading = False
                pygame.quit()
                quit()
            if evento == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE:
                    for passaro in passaros:
                        passaro.pular()
        # movimentos
        for passaro in passaros:
            passaro.movimento()
        chao.mover()

        adicionar_tubo = False
        remover_tubos = []
        for tubo in tubos:
            for i, passaro in enumerate(passaros):
                if tubo.colidir(passaro):
                    passaros.pop(i)
                if not tubo.passou and passaro.x > tubo.x:
                    tubo.passou = True
                    adicionar_tubo = True

            tubo.mover()
            if tubo.x + tubo.TUBO_topo.get_width() < 0:
                remover_tubos.append(tubo)
        if adicionar_tubo:
            pontos += 1
            tubos.append(Tubo(600))
        for tubo in remover_tubos:
            tubos.remove(tubo)
        for i, passaro in enumerate(passaros):
            if (passaro.y + passaro.imagem.get_height()) > chao.y or passaro.y < 0:
                passaros.pop(i)

        desenhar_tela(tela, passaros, tubos, chao, pontos)

if __name__ == '__main__':
    main()