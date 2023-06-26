# from flask import Flask, render_template

# tu3 = Flask(__name__)

# @tu3.route('/')
# def index():
#     return render_template('game.html')

# if __name__ == '__main__':
#     tu3.run()



import pygame
import random

pygame.init()

# 전역변수 선언
WHITE = (255, 255, 255)
size = (800, 600)
screen = pygame.display.set_mode(size)

done = False
clock = pygame.time.Clock()

# 게임 이미지 경로
bg_image_path = 'background.png'
plane_image_path = 'plane.png'
bird_image_path = 'bird.png'

# 배경 이미지 로드
bg_image = pygame.image.load(bg_image_path)
bg_image = pygame.transform.scale(bg_image, size)

# 비행기 클래스
class Airplane(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load(plane_image_path)
        self.image = pygame.transform.scale(self.image, (180, 135))
        self.rect = self.image.get_rect()
        self.rect.x = 20
        self.rect.y = 24
        self.speed_y = 0
        self.speed_x = 0

    def move_up(self):
        self.speed_y = -5

    def move_down(self):
        self.speed_y = 5

    def move_left(self):
        self.speed_x = -5

    def move_right(self):
        self.speed_x = 5

    def stop_vertical(self):
        self.speed_y = 0

    def stop_horizontal(self):
        self.speed_x = 0

    def update(self):
        self.rect.y += self.speed_y
        self.rect.x += self.speed_x

        if self.rect.y <= 0:
            self.rect.y = 0
        elif self.rect.y >= size[1] - self.rect.height:
            self.rect.y = size[1] - self.rect.height

        if self.rect.x <= 0:
            self.rect.x = 0
        elif self.rect.x >= size[0] - self.rect.width:
            self.rect.x = size[0] - self.rect.width

    def draw(self):
        screen.blit(self.image, self.rect)

# 새 클래스
class Bird(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load(bird_image_path)
        self.image = pygame.transform.scale(self.image, (120, 90))
        self.rect = self.image.get_rect()
        self.rect.x = size[0]
        self.rect.y = random.randint(20, size[1] - 20)
        self.speed_x = random.randint(3, 6)
        self.is_outside = False

    def update(self):
        self.rect.x -= self.speed_x

        if self.rect.right <= 0:
            self.is_outside = True

    def draw(self):
        screen.blit(self.image, self.rect)

# 점수 클래스
class Scoreboard(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.score = 0
        self.font = pygame.font.Font(None, 36)

    def increase_score(self):
        self.score += 1

    def draw(self):
        score_text = self.font.render("Score: " + str(self.score), True, (0, 0, 0))
        screen.blit(score_text, (10, 10))

    def increase_bird_size(self):
        for bird in birds:
            if self.score > 5:
                bird.image = pygame.transform.scale(bird.image, (int(bird.rect.width * 1.2), int(bird.rect.height * 1.2)))

# 객체 생성
airplane = Airplane()
birds = pygame.sprite.Group()
scoreboard = Scoreboard()

# pygame 무한루프
def runGame():
    global done

    bird_timer = pygame.USEREVENT + 1
    pygame.time.set_timer(bird_timer, random.randint(3000, 5000))

    while not done:
        clock.tick(60)
        screen.blit(bg_image, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    airplane.move_up()
                elif event.key == pygame.K_DOWN:
                    airplane.move_down()
                elif event.key == pygame.K_LEFT:
                    airplane.move_left()
                elif event.key == pygame.K_RIGHT:
                    airplane.move_right()
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    airplane.stop_vertical()
                elif event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    airplane.stop_horizontal()
            elif event.type == bird_timer:
                bird = Bird()
                birds.add(bird)
                pygame.time.set_timer(bird_timer, random.randint(3000, 5000))

        airplane.update()

        birds.update()

        for bird in birds:
            if pygame.sprite.collide_rect(airplane, bird):
                done = True

            if bird.is_outside:
                scoreboard.increase_score()
                bird.kill()

        birds.draw(screen)
        airplane.draw()
        scoreboard.draw()
        scoreboard.increase_bird_size()

        pygame.display.update()

runGame()
pygame.quit()
