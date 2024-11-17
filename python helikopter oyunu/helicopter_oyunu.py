
import random

# Oyun ayarları
WIDTH, HEIGHT = 1920,1080
FPS = 60
HELICOPTER_SPEED = 5
OBSTACLE_SPEED = 7
OBSTACLE_WIDTH = 70

# Renkler
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Pygame'i başlat
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Helikopter Oyunu")
clock = pygame.time.Clock()

# Helikopter sınıfı
class Helicopter:
    def __init__(self):
        self.image = pygame.image.load('helicopter.png')  # Resmi yükle
        self.image = pygame.transform.scale(self.image, (50, 30))  # Resmi boyutlandır
        self.rect = self.image.get_rect(center=(100, HEIGHT // 2))
    
    def move(self, direction):
        if direction == 'up' and self.rect.top > 0:
            self.rect.y -= HELICOPTER_SPEED
        elif direction == 'down' and self.rect.bottom < HEIGHT:
            self.rect.y += HELICOPTER_SPEED
    
    def draw(self, screen):
        screen.blit(self.image, self.rect)

# Engel sınıfı
class Obstacle:
    def __init__(self):
        self.width = OBSTACLE_WIDTH
        self.height = random.randint(100, 400)  # Rastgele yükseklik
        self.x = WIDTH
        self.y = random.randint(0, HEIGHT - self.height)  # Rastgele y konumu

    def move(self):
        self.x -= OBSTACLE_SPEED
    
    def draw(self, screen):
        pygame.draw.rect(screen, RED, (self.x, self.y, self.width, self.height))

# Oyun döngüsü
def game_loop():
    helicopter = Helicopter()
    obstacles = []
    score = 0
    running = True

    while running:
        screen.fill(WHITE)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            helicopter.move('up')
        if keys[pygame.K_DOWN]:
            helicopter.move('down')

        # Engel oluşturma
        if random.randint(1, 20) == 1:
            obstacles.append(Obstacle())

        # Engel hareket ettir
        for obstacle in obstacles:
            obstacle.move()
            obstacle.draw(screen)

            # Engel ekranın dışına çıktığında sil
            if obstacle.x < -OBSTACLE_WIDTH:
                obstacles.remove(obstacle)
                score += 1

            # Çarpışma kontrolü
            if helicopter.rect.colliderect(pygame.Rect(obstacle.x, obstacle.y, obstacle.width, obstacle.height)):
                running = False  # Oyun bitince döngüden çık

        helicopter.draw(screen)

        # Skoru ekrana yazdır
        font = pygame.font.SysFont(None, 48)  # Font oluştur
        score_text = font.render(f'Skor: {score}', True, (0, 0, 0))  # Skoru oluştur
        text_rect = score_text.get_rect(topright=(WIDTH - 10, 10))  # Skorun sağ üst köşede yer alması için ayarla
        screen.blit(score_text, text_rect)  # Skoru ekrana yerleştir

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    game_loop()