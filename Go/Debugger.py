import pygame as pg
class Dbugger:
    def __init__(self):
        self.font=pg.font.Font(None,30)
        self.color=(0,0,0)
        self.pos=(0,0)
        self.screen=None
        self.pre_text='Debugging:'
        self.info=['Debugger']
    def update(self):
        offset=0
        text=self.font.render(self.pre_text,1,self.color)
        self.screen.blit(text,(self.pos[0],self.pos[1]+offset))
        for i in self.info:
            offset+=30
            text=self.font.render(i,1,self.color)
            self.screen.blit(text,(self.pos[0],self.pos[1]+offset))
            
