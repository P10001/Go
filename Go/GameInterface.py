import pygame as pg
import Debugger as dbg
import Board as bd
import MyBase as mb
import GameControls as gmctrl
class SimpleGame:
    WHITE_COLOR=(255,255,255)
    BLACK_COLOR=(0,0,0)
    def __init__(self,width,height):
        pg.init()
        self.screen=pg.display.set_mode((width,height))
        self.game_end=False
        self.clock=pg.time.Clock()
        self.debugg_on=False
        self.back=pg.Surface(self.screen.get_size()).convert()
        self.back.fill(SimpleGame.WHITE_COLOR)
        self.board=None
    def close(self):
        pg.quit()
    def set_up_classic_game(self,rows,columns):#经典19路棋盘
        self.board=bd.TwoPlayerBoard(rows,columns)
        self.board.precision=9
        star_points=[]
        #待修改，若行列未定，星位位置应变化
        for i in range(1,4):
            for j in range(1,4):
                star_points.append((i*6-3,j*6-3))
        self.board.draw_star_position(star_points)
        self.debugger=dbg.Dbugger()
        self.debugger.screen=self.back
    def update(self,events):
        #重置背景
        self.back.fill(SimpleGame.WHITE_COLOR)
        #棋盘处理消息，在背景上绘制棋盘
        if self.board is not None:
            self.board.update(events)
            self.back.blit(self.board.board_area,(self.board.rect.left,self.board.rect.top))
        #debugger更新用于调试的信息，绘制在背景上
        if self.debugg_on==True:
            self.debugger.info=self.update_clusters_info()
            self.debugger.update()
        #在屏幕上绘制背景
        self.screen.blit(self.back,(0,0))
    def main_loop_proc(self):#游戏主循环
        while not self.game_end:
            self.clock.tick(60)
            e=pg.event.get()
            for i in e:
                if i.type==pg.QUIT:
                    self.close()
                    self.game_end=True
                    return
            self.update(e)
            #翻转缓冲区
            pg.display.flip()
    def update_clusters_info(self):
        board=self.board
        t1='Clusters number: '+str(int(len(board.pieces_cluster)))
        t_list=[t1]
        for i in board.pieces_cluster:
            temp=''
            for j in i:
                temp=temp+'('+str(j[0])+','+str(j[1])+')'+' '
            temp+=str(board.check_qi_of_cluster(i))
            t_list.append(temp)
        return t_list
class SimpleGameWithSimpleMenu(SimpleGame):
    MENU_STATE=0
    GAME_STATE=1


    BUTTON_ID_1=1
    BUTTON_ID_2=2
    BUTTON_ID_3=3
    
    BUTTON_ID_RETRY=4
    BUTTON_ID_UNDO=5
    BUTTON_ID_SAVE=6
    BUTTON_ID_LOAD=7
    BUTTON_ID_BRANCH=8
    BUTTON_ID_RESIGN=9
    FUNC_SWITCH={}
    BUTTON_ID_LIST=[BUTTON_ID_1,BUTTON_ID_2,BUTTON_ID_3, #主菜单界面按钮
        BUTTON_ID_RETRY,BUTTON_ID_UNDO,BUTTON_ID_SAVE,BUTTON_ID_LOAD,BUTTON_ID_BRANCH,BUTTON_ID_RESIGN]
    UN_INIT=True
    def __init__(self,width,height):
        SimpleGame.__init__(self,width,height)
        self.state=SimpleGameWithSimpleMenu.MENU_STATE#主选单状态
        self.menu_buttons=pg.sprite.RenderPlain()
        self.init_main_menu()
        if SimpleGameWithSimpleMenu.UN_INIT:
            self._init_Class_States()
        
    def _init_Class_States(self):
        SimpleGameWithSimpleMenu.FUNC_SWITCH={\
            SimpleGameWithSimpleMenu.BUTTON_ID_1:self.button_action_start_game,\
            SimpleGameWithSimpleMenu.BUTTON_ID_2:self.button_action2,\
            SimpleGameWithSimpleMenu.BUTTON_ID_3:self.button_action3}
    def update(self, events):
        super().update(events)
        if self.state==SimpleGameWithSimpleMenu.MENU_STATE:
            self.display_main_menu()
            '''temp=pg.Surface(self.screen.get_size()).convert()
            temp.fill((0,250,120))
            self.back.blit(temp,(0,600))'''
            for i in self.menu_buttons:
                i.update(events)
        else:
            pass
    def display_main_menu(self):
        self.menu_buttons.draw(self.screen)
        
    def init_main_menu(self):
        buttons=[0,0,0]
        button_width=320
        button_height=140
        color=(0,0,0)
        left1=self.screen.get_rect().width/2-button_width/2
        top1=120
        pos=[(left1,top1),(left1,top1+button_height+button_height/3),(left1,top1+(button_height+button_height/3)*2)]
        for i in range(0,3):
            gmctrl.MenuButton.SPRITES_LISTS.append(self.menu_buttons)
            buttons[i]=gmctrl.MenuButton(pos[i],button_width,button_height,color,SimpleGameWithSimpleMenu.BUTTON_ID_LIST[i],[SimpleGameWithSimpleMenu.button_action],self)#1号到3号按钮
            buttons[i].round_angles(SimpleGame.WHITE_COLOR,button_height/4)
        start_text=mb.load_image('start_text.png','',-1)
        start_text=pg.transform.scale(start_text,(button_width,button_height))
        buttons[0].image.blit(start_text,(0,0))
    def init_game_buttons(self):
        button_radius=35
        distance_to_right_border=120#按钮的排列离右边界的距离
        top=30#距离上边界的距离
        color=(0,0,0)
        f=pg.font.Font(None,15)
        texts=[f.render('重来',1,color),f.render('悔棋',1,color),f.render('认输')]
        pos=(self.screen.right-distance_to_right_border,top)
        button_retry=gmctrl.GamePlayButton(pos,button_radius,color,texts[0],SimpleGameWithSimpleMenu.BUTTON_ID_RETRY,[],self)

    def button_action(self,button_id):
        return (SimpleGameWithSimpleMenu.FUNC_SWITCH[button_id])()
    def button_action_start_game(self):
        self.state=SimpleGameWithSimpleMenu.GAME_STATE
        SimpleGame.set_up_classic_game(self,19,19)
    def button_action2(self):
        pass
    def button_action3(self):
        pass
    def button_action_undo(self):
        last_pos=self.board.last_move()[0]
        self.board.delete_piece(last_pos)
    def main_loop_proc(self):
        return super().main_loop_proc()

