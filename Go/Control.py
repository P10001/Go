#控件类
import pygame as pg
class Control:
    def __init__(self,pos):
        self.pos=pos
        self.acting=False
    def update(self):
        if self.acting==True:
            self.activate()
        else:
            pass
    def activate(self):
        pass
class Button(Control):
    def __init__(self,pos):
        Control.__init__(self,pos)
    def update(self,action):
        self.acting=action
        Control.update(self)
    def activate(self):
        pass
class ClickButton(Button):
    def __init__(self,pos):
        Button.__init__(self,pos)
    def update(self,events):
        for i in events:
            if i.type==pg.MOUSEBUTTONDOWN and self.check_click(i.pos):
                Button.update(self,True)
    def check_click(self,pos):
        if self.pos==pos:
            return True
        else:
            return False
    def activate(self):
        pass
class RectangleClickButton(ClickButton,pg.sprite.Sprite):
    SPRITES_LISTS=[]
    def __init__(self,pos,width,height,color=(0,0,0)):#对于矩形按钮，pos为左上顶点坐标
        pg.sprite.Sprite.__init__(self)
        ClickButton.__init__(self,pos)
        self.image=pg.Surface((width,height)).convert()
        self.rect=self.image.get_rect()
        self.rect=self.rect.move((pos[0]-self.rect.left,pos[1]-self.rect.top))
        self.color=color
        self.image.fill(color)
        for i in RectangleClickButton.SPRITES_LISTS:
            i.add(self)
    def update(self,events):
        ClickButton.update(self,events)#与ClickButton的区别只在于其点击检定不同
    def check_click(self, pos):
        if pos[0]>=self.rect.left and pos[0]<=self.rect.right and pos[1]>=self.rect.top and pos[1]<=self.rect.bottom:
            return True
        else:
            return False
    def activate(self):
        pass
    def round_angles(self,back_color,radius):
        radius=int(radius)
        square=pg.Surface((radius,radius)).convert()
        square.fill(back_color)
        self.image.blit(square,(0,0))
        self.image.blit(square,(self.rect.width-radius,0))
        self.image.blit(square,(0,self.rect.height-radius))
        self.image.blit(square,(self.rect.width-radius,self.rect.height-radius))
        width=self.rect.width
        height=self.rect.height
        pg.draw.circle(self.image,self.color,(radius,radius),radius)
        pg.draw.circle(self.image,self.color,(width-radius,radius),radius)
        pg.draw.circle(self.image,self.color,(radius,height-radius),radius)
        pg.draw.circle(self.image,self.color,(width-radius,height-radius),radius)
class CircleClickButton(ClickButton,pg.sprite.Sprite):
    SPRITES_LISTS=[]
    def __init__(self, pos,radius,color=(0,0,0)):#对圆形按钮，pos是其圆心坐标
        ClickButton.__init__(self,pos)
        pg.sprite.Sprite.__init__(self)
        self.radius=radius
        self.color=color
        self.image=pg.Surface((radius*2,radius*2)).convert()
        self.rect=self.image.get_rect()
        self.rect=self.rect.move((pos[0]-radius-self.rect.left,pos[1]-radius-self.rect.right))
        pg.draw.circle(self.image,self.color,pos,radius)
        for i in CircleClickButton.SPRITES_LISTS:
            i.add(self)
    def update(self, events):
        return super().update(events)
    def check_click(self, pos):
        if (pos[0]-self.pos[0])*(pos[0]-self.pos[0])+(pos[1]-self.pos[1])*(pos[1]-self.pos[1])<=self.radius*self.radius:
            return True
        else:
            return False
    def activate(self):
        return super().activate()