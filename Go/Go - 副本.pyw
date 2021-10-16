import Board as bd
import pygame as pg
import Debugger as dbg
def update_clusters(board):
    t1='Clusters number: '+str(int(len(board.pieces_cluster)))
    t_list=[t1]
    for i in board.pieces_cluster:
        temp=''
        for j in i:
            temp=temp+'('+str(j[0])+','+str(j[1])+')'+' '
        temp+=str(board.check_qi_of_cluster(i))
        t_list.append(temp)
    return t_list

def setup1():
    pg.init()
    screen=pg.display.set_mode((1000,720))
    b=bd.TwoPlayerBoard(19,19)
    b.precision=8
    star_points=[]
    d=dbg.Dbugger()
    d.pos=(680,0)
    for i in range(1,4):
        for j in range(1,4):
            star_points.append((i*6-3,j*6-3))
    b.draw_star_position(star_points)
    back=pg.Surface(screen.get_size()).convert()
    back.fill((255,255,255))
    white=(255,255,255)
    d.screen=back
    c=pg.time.Clock()
    while True:
        back.fill(white)
        i = pg.event.get()
        for e in i:
            if e.type==pg.QUIT:
                pg.quit()
                return
        b.update(i)
        c.tick(60)
        d.info=update_clusters(b)
        d.update()
        back.blit(b.board_area,(b.rect.left,b.rect.top))
        screen.blit(back,(0,0))
        pg.display.flip()
#setup()   
import GameInterface 
def start_game_1():
    game=GameInterface.SimpleGameWithSimpleMenu(1080,720)
    game.main_loop_proc()
start_game_1()