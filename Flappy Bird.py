import pygame, os, random, sys, time
from pygame.locals import *
path = os.path.abspath(sys.argv[0])
path = path.replace("Swappy Bird.py", "")
def draw_text(screen, text, size, color, x, y):
    font = pygame.font.SysFont(None, size)
    img = font.render(text, True, color)
    screen.blit(img, (x, y))
def game():
    # VARIABLES
    SCREEN_WIDTH = 1000
    SCREEN_HEIGHT = 600
    SPEED = 20
    GRAVITY = 2.5
    GAME_SPEED = 15
    GROUND_WIDTH = 2 * SCREEN_WIDTH
    GROUND_HEIGHT = 100
    PIPE_WIDTH = 80
    PIPE_HEIGHT = 500
    PIPE_GAP = 150
    SCORE = 0
    SPEED_TRACK = 0
    wing = path+'assets/audio/wing.wav'
    hit = path+'assets/audio/hit.wav'
    bgmusic = path+'assets/audio/Fields of Ice.mp3'
    game_over_music = path+'assets/audio/Music Box Game Over III.mp3'
    GAME_OVER = path+'assets/sprites/gameover.png'
    pygame.mixer.init()
    wing_sound = pygame.mixer.Sound(wing)
    hit_sound = pygame.mixer.Sound(hit)
    class Bird(pygame.sprite.Sprite):
        def __init__(self):
            pygame.sprite.Sprite.__init__(self)
            self.images = [pygame.image.load(path+'assets/sprites/bluebird-upflap.png').convert_alpha(),
                           pygame.image.load(path+'assets/sprites/bluebird-midflap.png').convert_alpha(),
                           pygame.image.load(path+'assets/sprites/bluebird-downflap.png').convert_alpha()]
            self.speed = SPEED
            self.current_image = 0
            self.image = self.images[self.current_image]
            self.mask = pygame.mask.from_surface(self.image)
            self.rect = self.image.get_rect()
            self.rect[0] = SCREEN_WIDTH / 6
            self.rect[1] = SCREEN_HEIGHT / 2
        def update(self):
            self.current_image = (self.current_image + 1) % 3
            self.image = self.images[self.current_image]
            self.speed += GRAVITY
            # UPDATE HEIGHT
            self.rect[1] += self.speed
        def bump(self):
            self.speed = -SPEED
        def begin(self):
            self.current_image = (self.current_image + 1) % 3
            self.image = self.images[self.current_image]
    class Pipe(pygame.sprite.Sprite):
        def __init__(self, inverted, xpos, ysize):
            pygame.sprite.Sprite.__init__(self)
            self.image = pygame.image.load(path+'assets/sprites/pipe-green.png').convert_alpha()
            self.image = pygame.transform.scale(self.image, (PIPE_WIDTH, PIPE_HEIGHT))
            self.rect = self.image.get_rect()
            self.rect[0] = xpos
            if inverted:
                self.image = pygame.transform.flip(self.image, False, True)
                self.rect[1] = - (self.rect[3] - ysize)
            else:
                self.rect[1] = SCREEN_HEIGHT - ysize
            self.mask = pygame.mask.from_surface(self.image)
        def update(self):
            self.rect[0] -= GAME_SPEED
    class Ground(pygame.sprite.Sprite):
        def __init__(self, xpos):
            pygame.sprite.Sprite.__init__(self)
            self.image = pygame.image.load(path+'assets/sprites/base.png').convert_alpha()
            self.image = pygame.transform.scale(self.image, (GROUND_WIDTH, GROUND_HEIGHT))
            self.mask = pygame.mask.from_surface(self.image)
            self.rect = self.image.get_rect()
            self.rect[0] = xpos
            self.rect[1] = SCREEN_HEIGHT - GROUND_HEIGHT
        def update(self):
            self.rect[0] -= GAME_SPEED
    def is_off_screen(sprite):
        return sprite.rect[0] < -(sprite.rect[2])
    def get_random_pipes(xpos):
        size = random.randint(100, 300)
        pipe = Pipe(False, xpos, size)
        pipe_inverted = Pipe(True, xpos, SCREEN_HEIGHT - size - PIPE_GAP)
        return pipe, pipe_inverted
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('Swappy Bird')
    BACKGROUND = pygame.image.load(path+'assets/sprites/background-day.png')
    BACKGROUND = pygame.transform.scale(BACKGROUND, (SCREEN_WIDTH, SCREEN_HEIGHT))
    BEGIN_IMAGE = pygame.image.load(path+'assets/sprites/message.png').convert_alpha()
    begin_rect = BEGIN_IMAGE.get_rect()
    begin_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
    bird_group = pygame.sprite.Group()
    bird = Bird()
    bird_group.add(bird)
    ground_group = pygame.sprite.Group()
    for i in range(2):
        ground = Ground(GROUND_WIDTH * i)
        ground_group.add(ground)
    pipe_group = pygame.sprite.Group()
    for i in range(2):
        pipes = get_random_pipes(SCREEN_WIDTH * i + 800)
        pipe_group.add(pipes[0])
        pipe_group.add(pipes[1])
    clock = pygame.time.Clock()
    begin = True
    while begin:
        clock.tick(15)
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_SPACE or event.key == K_UP:
                    bird.bump()
                    wing_sound.play()
                    begin = False
                if event.key == K_q:
                    pygame.quit()
                    sys.exit()
        screen.blit(BACKGROUND, (0, 0))
        screen.blit(BEGIN_IMAGE, (120, 150))
        if is_off_screen(ground_group.sprites()[0]):
            ground_group.remove(ground_group.sprites()[0])
            new_ground = Ground(GROUND_WIDTH - 20)
            ground_group.add(new_ground)
        bird.begin()
        ground_group.update()
        bird_group.draw(screen)
        ground_group.draw(screen)
        draw_text(screen, f'Score: {SCORE}', 32, (255, 255, 255), 10, 10)
        pygame.display.update()
    pygame.mixer.music.load(bgmusic)
    pygame.mixer.music.play(-1)  # The -1 makes it loop indefinitely
    while True:
        clock.tick(GAME_SPEED)
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                return  # Exit the game loop
            if event.type == KEYDOWN:
                if event.key == K_SPACE or event.key == K_UP:
                    bird.bump()
                    wing_sound.play()
                if event.key == K_q:
                    pygame.quit()
                    sys.exit()
        screen.blit(BACKGROUND, (0, 0))
        if is_off_screen(ground_group.sprites()[0]):
            ground_group.remove(ground_group.sprites()[0])
            new_ground = Ground(GROUND_WIDTH - 20)
            ground_group.add(new_ground)
        if(is_off_screen(pipe_group.sprites()[0])):
            pipe_group.remove(pipe_group.sprites()[0])
            pipe_group.remove(pipe_group.sprites()[0])
            if(GAME_SPEED<31):
                SCORE += 1
                SPEED_TRACK += 1
                if(SPEED_TRACK==7):
                    SPEED_TRACK = 0
                    GAME_SPEED += 1
                    PIPE_GAP -= 1
            pipes = get_random_pipes(SCREEN_WIDTH * 2)
            pipe_group.add(pipes[0])
            pipe_group.add(pipes[1])
        bird_group.update()
        ground_group.update()
        pipe_group.update()
        bird_group.draw(screen)
        pipe_group.draw(screen)
        ground_group.draw(screen)
        draw_text(screen, f'Score: {SCORE}', 32, (255, 255, 255), 10, 10)
        pygame.display.update()
        # Collision detection and game over handling
        if (pygame.sprite.groupcollide(bird_group, ground_group, False, False, pygame.sprite.collide_mask) or pygame.sprite.groupcollide(bird_group, pipe_group, False, False, pygame.sprite.collide_mask) or bird.rect[1] < 0):
            hit_sound.play()
            # Load game over image and center it
            game_over_image = pygame.image.load(GAME_OVER).convert_alpha()
            game_over_rect = game_over_image.get_rect()
            game_over_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
            # Pause briefly and display game over screen
            pygame.mixer.music.load(game_over_music)
            pygame.mixer.music.play(1)
            # Display game over image
            screen.blit(game_over_image, game_over_rect)
            pygame.display.update()
            time.sleep(7)
            break
while True:
    game()
