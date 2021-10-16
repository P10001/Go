import pygame as pg
class Board(pg.sprite.Sprite):
    COLOR_LIST=[(0,0,0),(60,0,0),(0,60,0),(0,0,60),(120,0,0),(0,120,0),(0,0,120)]
    def __init__(self,rows,columns,board_file=''):
        pg.sprite.Sprite.__init__(self)
        self.rows=rows
        self.columns=columns
        self.grids=[]
        self.pieces_cluster=[]
        for i in range(0,self.rows):
            self.grids.append([])
            for j in range(0,self.columns):
                self.grids[i].append(0)
        self.precision=5
        if board_file=='':
            
            self.board_area=pg.Surface(pg.display.get_surface().get_size()).convert()
            self.board_area=pg.transform.scale(self.board_area,(int(self.board_area.get_rect().height*0.85),int(self.board_area.get_rect().height*0.85)))
            self.rect=self.board_area.get_rect().move((self.board_area.get_rect().width/8,self.board_area.get_rect().height/8))
            self.boundary_offset=self.rect.width/12
            self.star_flag=False
            self.init_board_reset()
            
    def init_board_reset(self):
        
        self.board_area.fill((	255 ,228 ,181	))
        
        self.draw_boundary()
        self.draw_grid()
        if self.star_flag:
            self.draw_star_position(self.star_points)
    def draw_circle_in_board(self,pos,radius,color=(0,0,0)):#pos的参数为X方向的坐标和Y方向的坐标，与行号-列号的结构正好相反
        x=self.inner_rect.left-self.rect.left+pos[0]*self.inner_rect.width/(self.columns-1)
        y=self.inner_rect.top-self.rect.top+pos[1]*self.inner_rect.height/(self.rows-1)
        pg.draw.circle(self.board_area,color,(int(x),int(y)),radius)
    def draw_star_position(self,points):
        for i in points:
            self.draw_circle_in_board(i,3)
        self.star_flag=True
        self.star_points=points
    def display_pieces_clusters(self):
        k=0
        for i in self.pieces_cluster:
            color=Board.COLOR_LIST[k]
            for j in i:
                self.draw_circle_in_board((j[1],j[0]),10,color)
            k+=1
    def draw_all_pieces(self):
        for i in range(0,self.rows):
            for j in range(0,self.columns):
                if self.grids[i][j]!=0:
                    pos=(j,i)
                    self.draw_circle_in_board(pos,10)
    def update(self,events):
        for i in events:
            pos=self.msg_proc(i)
            self.init_board_reset()
            if pos is not None:
                self.make_move(pos)
        #self.draw_all_pieces()
        self.display_pieces_clusters()
        
    def draw_boundary(self):
        offset=self.boundary_offset
        recta=(offset,offset,self.rect.width-offset,self.rect.height-offset)
        self.inner_rect=self.rect.move(offset,offset)
        self.inner_rect.width=self.rect.width-offset*2
        self.inner_rect.height=self.inner_rect.width
        points=[(recta[0],recta[1]),(recta[2],recta[1]),(recta[2],recta[3]),(recta[0],recta[3])]
        pg.draw.lines(self.board_area,(10,10,10),True,points)
    def draw_grid(self):
        i=0
        x1=self.inner_rect.left-self.rect.left
        y1=self.inner_rect.top-self.rect.top
        x2=x1
        y2=y1+self.inner_rect.height
        x_step=self.inner_rect.width/(self.columns-1)
        y_step=self.inner_rect.height/(self.rows-1)
        while i<self.columns-1:
            pg.draw.line(self.board_area,(10,10,10),(x1,y1),(x2,y2))
            i+=1
            x1+=x_step
            x2+=x_step
        x1=self.inner_rect.left-self.rect.left
        #x2-=x_step
        y2=y1
        i=0
        while i<self.rows-1:
            pg.draw.line(self.board_area,(10,10,10),(x1,y1),(x2,y2))
            i+=1
            y1+=y_step
            y2+=y_step
    def check_piece_link(self,pos1,pos2):
        if pos1[0]==pos2[0] and abs(pos1[1]-pos2[1])==1 or pos1[1]==pos2[1] and abs(pos1[0]-pos2[0])==1:
            return True
        else:
            return False
    def make_move(self,pos,extra_mark=None):
        flag=False
        linked_clusters=[]
        for i in self.pieces_cluster:
            for j in i:
                if self.check_piece_link(j,pos) and (extra_mark is None or extra_mark==self.grids[j[0]][j[1]]):
                    linked_clusters.append(i)
                    flag=True
                    break
        if not flag:
            self.pieces_cluster.append([pos])
        else:
            newcluster=[pos]
            for i in linked_clusters:
                self.pieces_cluster.remove(i)
                newcluster+=i
            self.pieces_cluster.append(newcluster)
        if extra_mark is None:
            self.grids[pos[0]][pos[1]]=1
        else:
            self.grids[pos[0]][pos[1]]=extra_mark
    def msg_proc(self,e):
        if e.type==pg.MOUSEBUTTONDOWN:
            x_pixels=self.inner_rect.width/(self.columns-1)
            y_pixels=self.inner_rect.height/(self.rows-1)
            x=e.pos[0]-self.inner_rect.left
            y=e.pos[1]-self.inner_rect.top
            x_off=x%x_pixels
            y_off=y%y_pixels
            x_off_square=min([x_off*x_off,(x_off-x_pixels)*(x_off-x_pixels)])
            y_off_square=min([y_off*y_off,(y_off-y_pixels)*(y_off-y_pixels)])
            newpos=(round(x/x_pixels),round(y/y_pixels))
            if x>0 and x<self.inner_rect.width and y>0 and y< self.inner_rect.height and x_off_square< self.precision*self.precision and y_off_square<self.precision*self.precision:
                return (newpos[1],newpos[0])
            else:
                pass
        return None
    def check_qi_of_cluster(self):
        pass
    def game_system_update(self):
        pass
class TwoPlayerBoard(Board):

    def __init__(self,rows,columns):
        Board.__init__(self,rows,columns)
        self.player_color1=(0,0,0)
        self.player_color2=(255,255,255)
        self.color_map={1:self.player_color1,2:self.player_color2}
        self.player_turn=1
        self.last_move=None
    def update(self,events):
        self.init_board_reset()
        for i in events:
            pos=self.msg_proc(i)
            if pos is not None:
                self.move_operation(pos)
                self.game_system_update()
        self.draw_all_pieces()

    def draw_all_pieces(self):
        for i in range(0,self.rows):
            for j in range(0,self.columns):
                if self.grids[i][j]!=0:
                    Board.draw_circle_in_board(self,(j,i),10,self.color_map[self.grids[i][j]])

    def msg_proc(self,e):
        return Board.msg_proc(self,e)
    def move_operation(self,pos):
        if self.grids[pos[0]][pos[1]]!=0:
            return
        Board.make_move(self,pos,self.player_turn)
        self.last_move=(pos,self.player_turn)
        if self.player_turn==1:
            self.player_turn=2
        else:
            self.player_turn=1
        
    def game_system_update(self):
        for i in self.pieces_cluster:
            j=i[0]
            if self.grids[j[0]][j[1]]!=self.player_turn:
                    pass
            else:
                if self.check_qi_of_cluster(i)!=0:
                    pass
                else:
                    self.kill_cluster(i)
                    self.pieces_cluster.remove(i)
    def check_qi_of_piece(self,pos):
        num=0
        if pos[0]>0 and self.grids[pos[0]-1][pos[1]]==0:
            num+=1
        if pos[1]>0 and self.grids[pos[0]][pos[1]-1]==0:
            num+=1
        if pos[0]<self.rows-1 and self.grids[pos[0]+1][pos[1]]==0:
            num+=1
        if pos[1]<self.columns-1 and self.grids[pos[0]][pos[1]+1]==0:
            num+=1
        return num
    def check_qi_of_cluster(self,cluster):
        total_qi=0
        for i in cluster:
            total_qi+=self.check_qi_of_piece(i)
        return total_qi
    def kill_cluster(self,cluster):
        for i in cluster:
            self.grids[i[0]][i[1]]=0
    def delete_piece(self,pos,player_turn=None):
        if self.grids[pos[0]][pos[1]]!=0 and (player_turn is None or player_turn==self.grids[pos[0]][pos[1]]):
            for i in self.pieces_cluster:
                i.remove(pos)
            self.grids[pos[0]][pos[1]]=0