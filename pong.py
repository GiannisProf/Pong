import pygame
pygame.init()
import time 

#defining constants for better management
WIDTH, HEIGHT = 700, 600  #window width, height
WIN = pygame.display.set_mode((WIDTH,HEIGHT)) #create window value
pygame.display.set_caption("PONG") 
FPS=60
WHITE=(255,255,255) #rgb white
BLACK=(0,0,0)   #rgb black
PADDLE_WIDTH,PADDLE_HEIGHT = 20,100
SCORE_FONT = pygame.font.SysFont("comicsans",50)
WINNING_SCORE = 10

class Paddle: #class for paddles
    COLOR = WHITE
    VELOCITY = 5

    def __init__(self,x,y,width,height): #standard init function
        self.x= self.original_x = x
        self.y= self.original_y = y
        self.width=width
        self.height=height
    
    
    def draw(self,win):
        pygame.draw.rect(win,self.COLOR,(self.x,self.y,self.width,self.height))

    def move(self,up=True):
        if up:
            self.y -= self.VELOCITY
        else:    
            self.y += self.VELOCITY

    def reset(self): #reset paddles 
        self.x = self.original_x
        self.y = self.original_y

class Ball: #class for the ball
    MAX_VEL = -5
    COLOR = WHITE

    def __init__(self,x,y,radius):
        self.x = self.original_x = x
        self.y = self.original_y = y
        self.radius = radius
        self.x_vel = self.MAX_VEL
        self.y_vel = 0
    
    def draw(self,win):
        pygame.draw.circle(win, self.COLOR,(self.x + 5,self.y),self.radius)

    def move(self):
        self.x += self.x_vel
        self.y += self.y_vel
    
    def reset(self):
        self.y = self.original_y
        self.x = self.original_x
        self.y_vel = 0 
        self.x_vel *= -1


def draw(win,paddles,ball,left_score,right_score): #fill window
    win.fill(BLACK)

    left_score_test = SCORE_FONT.render(f"{left_score}",1,WHITE)
    right_score_test = SCORE_FONT.render(f"{right_score}",1,WHITE)

    win.blit(left_score_test,(WIDTH//4 - left_score_test.get_width()//2,20))
    win.blit(right_score_test,(WIDTH * (3/4)- right_score_test.get_width()//2,20))


    for paddle in paddles:
        paddle.draw(win)
    
    ball.draw(win)
    pygame.display.update() #use only once

def handle_collision(ball,left_paddle,right_paddle):
    if ball.y + ball.radius >= HEIGHT or ball.y - ball.radius <= 0: #top and bottom collision
        ball.y_vel *= -1
    
    if ball.x_vel < 0 : #left paddle collision
        if ball.y >= left_paddle.y and ball.y <= left_paddle.y + left_paddle.height: 
            if ball.x - ball.radius <= left_paddle.x + left_paddle.width:
                ball.x_vel *= -1

                middle_y = left_paddle.y + left_paddle.height / 2
                differnce_in_y = middle_y - ball.y
                reduction_factor = (left_paddle.height / 2) / ball.MAX_VEL
                y_vel = differnce_in_y / reduction_factor
                ball.y_vel = -1 * y_vel 

    else : #right paddle collision
        if ball.y >= right_paddle.y and ball.y <= right_paddle.y + right_paddle.height:
            if ball.x + ball.radius >= right_paddle.x:
                ball.x_vel *= -1

                middle_y = right_paddle.y + right_paddle.height/2
                differnce_in_y = middle_y - ball.y
                reduction_factor = (right_paddle.height / 2) / ball.MAX_VEL
                y_vel = differnce_in_y / reduction_factor
                ball.y_vel = -1 * y_vel 

def handle_paddle_movement(keys,left_paddle,right_paddle):
    if keys[pygame.K_w] and left_paddle.y-left_paddle.VELOCITY >=0: #if w is pressed go up
        left_paddle.move(up=True)
    if keys[pygame.K_s] and left_paddle.y + left_paddle.VELOCITY + left_paddle.height <= HEIGHT: #if s is pressed go down
        left_paddle.move(up=False) #if s is pressed go down
    if keys[pygame.K_UP] and right_paddle.y-right_paddle.VELOCITY >=0: #if up arrow is preesed go up
        right_paddle.move(up=True) 
    if keys[pygame.K_DOWN] and right_paddle.y + right_paddle.VELOCITY + right_paddle.height <= HEIGHT: #if down arrow is pressed go down
        right_paddle.move(up=False)
    


"""to movement effect dhmiourgeitai epeidh kathe fora pou pataw koumpi
kaleitai h update"""

def main():
    run = True
    clock = pygame.time.Clock()

    #initialize game objects
    left_paddle=Paddle(10,HEIGHT//2-PADDLE_HEIGHT//2,PADDLE_WIDTH,PADDLE_HEIGHT) 
    right_paddle=Paddle(WIDTH -10 - PADDLE_WIDTH,HEIGHT//2-PADDLE_HEIGHT//2,PADDLE_WIDTH,PADDLE_HEIGHT)
    dashed_line=Paddle(WIDTH//2,0,5,HEIGHT)
    ball = Ball(WIDTH//2,HEIGHT//2,7)

    left_score = 0
    right_score = 0

    
    while run: #main game loop

        clock.tick(FPS) #same fps for all computers
        draw(WIN,[left_paddle,right_paddle,dashed_line],ball, left_score,right_score) #use only once
        for event in pygame.event.get(): #for every event in game. For example click etc.
            if event.type== pygame.QUIT:
                run = False
                break

        keys = pygame.key.get_pressed() #returns map of pressed keys
        handle_paddle_movement(keys,left_paddle,right_paddle)
        ball.move()
        handle_collision(ball,left_paddle,right_paddle)

        if ball.x < 0:
            right_score += 1
            ball.reset()
        elif ball.x > WIDTH:
            left_score += 1
            ball.reset()

        won = False

        if left_score >= WINNING_SCORE:
            won = True
            win_text = "LEFT PLAYER WINS!"
        elif right_score >= WINNING_SCORE:
            won = True
            win_text = "RIGHT PLAYER WINS!"
        
        if won : 
            text = SCORE_FONT.render(win_text,1,WHITE) #create drawble object
            WIN.blit(text,(WIDTH//2 - text.get_width()//2,HEIGHT//4 + text.get_height()//2))
            pygame.display.update()
            pygame.time.delay(4000)
            ball.reset()
            left_paddle.reset()
            right_paddle.reset()
            left_score = 0 
            right_score = 0

    
    pygame.quit()


if __name__== '__main__': #only run this function if you directly run this file
    main()