from settings import * 
from sprites import * 
from groups import AllSprites
from support import * 
from random import randint
from timer import Timer

class Game:
    def __init__(self):
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption('Duckies Adventurex')
        self.clock = pygame.time.Clock()
        self.running = True

        self.all_sprites = AllSprites()
        self.collision_sprites = pygame.sprite.Group()
        self.enemy_sprites = pygame.sprite.Group()

        self.load_assets()
        self.setup()
    
    def load_assets(self):
        self.player_frames = import_folder('images', 'player') 
        self.bear_frames = import_folder('images', 'enemy')
        self.eating_frames = import_folder('images', 'eating')

        self.snowflake_images = [pygame.image.load(f'images/snowflakes/{i}.png').convert_alpha() for i in range(1, 7)]

    def setup(self):
        tmx_map = load_pygame(join('data', 'maps', 'world.tmx'))
        self.level_width = tmx_map.width * TILE_SIZE                                                                             
        self.level_height = tmx_map.height * TILE_SIZE

        for x, y, image in tmx_map.get_layer_by_name('Main').tiles():
            Sprite((x * TILE_SIZE,y * TILE_SIZE), image, (self.all_sprites, self.collision_sprites))
        
        for x, y, image in tmx_map.get_layer_by_name('Decoration').tiles():
            Sprite((x * TILE_SIZE,y * TILE_SIZE), image, self.all_sprites)
        
        for obj in tmx_map.get_layer_by_name('Entities'):
            if obj.name == 'Player':
                self.player = Player((obj.x, obj.y), self.all_sprites, self.collision_sprites, self.player_frames)
            if obj.name == 'Bear':
                Bear(self.bear_frames, pygame.Rect(obj.x, obj.y, obj.width, obj.height), (self.all_sprites, self.enemy_sprites))

        self.snowflakes = pygame.sprite.Group()
        for i in range(50): 
            size = randint(1, 6)  
            snowflake = Snowflake(
                (randint(0, WINDOW_WIDTH), randint(-50, -10)), 
                size, 
                self.snowflake_images[size - 1], 
                self.snowflakes
            )
    def run(self):
        while self.running:
            dt = self.clock.tick(FRAMERATE) / 1000 

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False 
            
            # update
            self.all_sprites.update(dt)
            self.snowflakes.update(dt)

            # for bear in self.enemy_sprites:
            #    if self.player.rect.colliderect(bear.rect):

            # draw 
            self.display_surface.fill(BG_COLOR)
            self.all_sprites.draw(self.player.rect.center)
            self.snowflakes.draw(self.display_surface)
            
            pygame.display.update()
        
        pygame.quit()

 
if __name__ == '__main__':
    game = Game()
    game.run() 