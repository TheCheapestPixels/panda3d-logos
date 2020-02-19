import sys
#import simplepbr
from direct.showbase.ShowBase import ShowBase
from direct.actor.Actor import Actor


class SplashBase(ShowBase):
    def __init__(self):
        ShowBase.__init__(self) 
        self.accept('escape', sys.exit)
        base.win.set_clear_color((0,0,0,1))
        #simplepbr.init()

        self.logo_animation = Actor("panda3d_logo.bam")
        self.logo_animation.reparent_to(render)
        self.logo_animation.play("splash")
        self.logo_animation.set_two_sided(True)

        self.logo_sound = base.loader.loadSfx("panda3d_logo.wav")
        self.logo_sound.play()

        render.ls()
        render.analyze()

app = SplashBase()
app.run()