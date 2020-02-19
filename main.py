import sys
from direct.showbase.ShowBase import ShowBase
from direct.actor.Actor import Actor
from direct.interval.IntervalGlobal import Sequence
from direct.interval.IntervalGlobal import LerpFunc
from panda3d.core import loadPrcFileData
from panda3d.core import AntialiasAttrib

loadPrcFileData('', 'fullscreen true')
loadPrcFileData('', 'framebuffer-multisample 1')
loadPrcFileData('', 'multisamples 2')

class SplashBase(ShowBase):
    def __init__(self):
        ShowBase.__init__(self) 
        self.accept('escape', sys.exit)
        base.win.set_clear_color((0,0,0,1))
        base.cam.set_pos(0, 1, 0.1)
        #base.cam.look_at(0, 6.3, -0.1)
        #base.cam.set_pos(0, -50, 0)

        # Load and prepare content
        self.logo_animation = Actor("panda3d_logo.bam")  # Centered around 0, 6.3, 0
        self.logo_animation.reparent_to(render)
        render.set_antialias(AntialiasAttrib.MMultisample)
        self.logo_sound = base.loader.loadSfx("panda3d_logo.wav")
        def null_effect(t):
            pass
        def fade_background_to_white(t):
            base.win.set_clear_color((t,t,t,1))
        self.effects = Sequence(
            LerpFunc(
                null_effect,
                fromData=0,
                toData=1,
                duration=3.878,
            ),
            LerpFunc(
                fade_background_to_white,
                fromData=0,
                toData=1,
                duration=1,
            ),
        )

        self.logo_animation.play("splash")
        #print("currently playing: " + self.logo_animation.getCurrentAnim())
        self.logo_sound.play()
        self.effects.start()

        #render.ls()
        #render.analyze()


app = SplashBase()
app.run()
