import Control as ctrl
class MessageButton:
    def __init__(self,id,activation_procs=[],msg_reciever=None):
        self.id=id
        self.action_list=activation_procs
        self.msg_target=msg_reciever
    def activate(self):
        for i in self.action_list:
            if self.msg_target is None:
                i(self.id)
            else:
                i(self.msg_target,self.id)
class MenuButton(ctrl.RectangleClickButton,MessageButton):
    SPRITES_LISTS=[]
    def __init__(self,pos,width,height,color,button_id,activation_procs=[],msg_reciever=None):
        ctrl.RectangleClickButton.SPRITES_LISTS=MenuButton.SPRITES_LISTS
        ctrl.RectangleClickButton.__init__(self,pos,width,height,color)
        MessageButton.__init__(self,button_id,activation_procs,msg_reciever)
    def update(self,events):
        ctrl.RectangleClickButton.update(self,events)
    def check_click(self, pos):
        return ctrl.RectangleClickButton.check_click(self,pos)
    def activate(self):
        return MessageButton.activate(self)
class GamePlayButton(ctrl.CircleClickButton,MessageButton):
    SPRITES_LIST=[]
    def __init__(self, pos, radius,color, text,button_id,activation_procs=[],msg_reciever=None):
        ctrl.CircleClickButton.SPRITES_LISTS=GamePlayButton.SPRITES_LIST
        ctrl.CircleClickButton(self,pos,radius,color)
        MessageButton.__init__(self,button_id,activation_proc,msg_reciever)
    def update(self,events):
        return ctrl.RectangleClickButton.update(self,events)
    def check_click(self,pos):
        return ctrl.CircleClickButton.check_click(self,pos)
    def activate(self):
        return MessageButton.activate(self)
        


