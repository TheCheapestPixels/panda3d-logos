import sys
from enum import Enum

from direct.showbase.ShowBase import ShowBase
from direct.actor.Actor import Actor
from direct.interval.IntervalGlobal import Sequence
from direct.interval.IntervalGlobal import Parallel
from direct.interval.IntervalGlobal import LerpPosHprInterval
from direct.interval.IntervalGlobal import LerpFunc
from direct.interval.IntervalGlobal import SoundInterval
from direct.interval.IntervalGlobal import Wait

from panda3d.core import AntialiasAttrib
from panda3d.core import Shader
from panda3d.core import Vec3
from panda3d.core import VBase2
from panda3d.core import VBase3
from panda3d.core import VBase4
from panda3d.core import NodePath
from panda3d.core import loadPrcFileData

from pathlib import Path


loadPrcFileData('', 'textures-power-2 none')
asset_path = Path(__file__).resolve().parent / 'assets' 


class Pattern(Enum):
    CONCENTRIC_CIRCLES = 0
    FLICKERING = 1
    SQUARESTAR = 2
    NOISE = 3
    DOUBLE_WHEEL = 4
    WHEEL = 5


class Colors(Enum):
    DIRECT = 0  # Black to white, non-wrapping
    RAINBOW = 1  # Red, yellow, green, cyan, blue, purple, red
    RGB_BANDS = 2 # Red, green, blue


class RainbowSplash:
    def __init__(self, pattern=Pattern.SQUARESTAR, colors=Colors.RGB_BANDS, pattern_freq=2, cycle_freq=10):
        self.pattern = pattern
        self.colors = colors
        self.pattern_freq = pattern_freq
        self.cycle_freq = cycle_freq

    def setup(self):
        # Store current values
        self.entry_background_color = VBase4(base.win.get_clear_color())
        self.entry_cam_pos = VBase3(base.cam.get_pos())
        self.entry_cam_hpr = VBase3(base.cam.get_hpr())
        self.entry_cam_scale = VBase3(base.cam.get_scale())
        self.entry_cam_fov = VBase2(base.cam.node().get_lens().get_fov())

        # Set values for splash
        base.win.set_clear_color((0,0,0,1))
        cam_dist = 2
        base.cam.set_pos(0, -2.2 * cam_dist, 0)
        base.cam.set_hpr(0, 0, 0)
        base.cam.set_scale(1)
        base.cam.node().get_lens().set_fov(45/cam_dist)

        # Set up the splash itself
        self.logo_animation = Actor(asset_path / "panda3d_logo.bam")
        self.logo_animation.reparent_to(render)
        self.logo_animation.set_two_sided(True)

        shader = Shader.load(
            Shader.SL_GLSL,
            vertex=asset_path / "panda3d_logo.vert",
            fragment=asset_path / "panda3d_logo.frag",
        )
        self.logo_animation.set_shader(shader)
        self.logo_animation.set_shader_input("fade", 0.0)
        self.logo_animation.set_shader_input("pattern", self.pattern.value)
        self.logo_animation.set_shader_input("colors", self.colors.value)
        self.logo_animation.set_shader_input("pattern_freq", self.pattern_freq)
        self.logo_animation.set_shader_input("cycle_freq", self.cycle_freq)
        self.logo_sound = base.loader.loadSfx(asset_path / "panda3d_logo.wav")

        # Build interval
        def shader_time(t):
            self.logo_animation.set_shader_input("time", t)
        def fade_background_to_white(t):
            base.win.set_clear_color((t,t,t,1))
            self.logo_animation.set_shader_input("time", t/3.878)
            self.logo_animation.set_shader_input("fade", t)
        def fade_to_black(t):
            base.win.set_clear_color((1-t,1-t,1-t,1))
            #self.logo_animation.set_shader_input("time", t/3.878)
            #self.logo_animation.set_shader_input("fade", t)

        # Timing:
        # 0.000     Start
        # 3.878     Logo is assembled, fade to black-on-whitey
        # 4.878     Black on white achieved
        # <+1.500>  Begin fade to black
        # <+1.741>  Black on black achieved
        # 8.119 Sound ends
        effects = Parallel(
            self.logo_animation.actorInterval(
                "splash",
                loop=False,
            ),
            SoundInterval(
                self.logo_sound,
                loop=False,
            ),
            Sequence(
                LerpFunc(
                    shader_time,
                    fromData=0,
                    toData=1,
                    duration=3.878,
                ),
                LerpFunc(
                    fade_background_to_white,
                    fromData=0,
                    toData=1,
                    duration=1.0,
                ),
                Wait(1.5),
                LerpFunc(
                    fade_to_black,
                    fromData=0,
                    toData=1,
                    duration=1.741,
                ),
            ),
        )
        return effects

    def teardown(self):
        # Store current values
        base.win.set_clear_color(self.entry_background_color)
        base.cam.set_pos(self.entry_cam_pos)
        base.cam.set_hpr(self.entry_cam_hpr)
        base.cam.set_scale(self.entry_cam_scale)
        base.cam.node().get_lens().set_fov(self.entry_cam_fov)

        self.logo_animation.cleanup()
        # FIXME: Destroy self.logo_sound


class WindowSplash:
    def setup(self):
        x_size, y_size = base.win.get_x_size(), base.win.get_y_size()
        bg_buffer = base.win.makeTextureBuffer(
            "Background Scene",
            x_size,
            y_size,
        )
        bg_buffer.set_clear_color_active(True)
        bg_buffer.set_clear_color(VBase4(0, 1, 0, 1))
        bg_buffer.set_sort(-100)  # render buffer before main scene.

        bg_texture = bg_buffer.get_texture()
        self.bg_texture = bg_texture
        bg_camera = base.make_camera(bg_buffer)

        self.setup_background_scene(bg_camera)

        # Foreground Scene
        base.win.set_clear_color((0, 0, 0, 1))
        cam_dist = 2
        base.cam.set_pos(0, -2.2 * cam_dist, 0)
        base.cam.node().get_lens().set_fov(45/cam_dist)

        self.logo_animation = Actor(asset_path / "panda3d_logo.bam")
        self.logo_animation.reparent_to(render)
        self.logo_animation.set_two_sided(True)

        shader = Shader.load(
            Shader.SL_GLSL,
            vertex=asset_path / "splash_window.vert",
            fragment=asset_path / "splash_window.frag",
        )
        self.logo_animation.set_shader(shader)
        self.logo_animation.set_shader_input("background", bg_texture)
        self.logo_animation.set_shader_input("fade", 0.0)
        self.logo_sound = base.loader.loadSfx(asset_path / "panda3d_logo.wav")

        # Build interval
        def fade_background_to_white(t):
            base.win.set_clear_color((t,t,t,1))
            self.logo_animation.set_shader_input("fade", t)
        def set_background_texture(t):
            self.logo_animation.set_shader_input(
                "background",
                self.bg_texture,
            )
                    
        effects = Parallel(
            self.logo_animation.actorInterval(
                "splash",
                loop=False,
            ),
            SoundInterval(
                self.logo_sound,
                loop=False,
            ),
            Sequence(
                LerpFunc(
                    set_background_texture,
                    fromData=0,
                    toData=1,
                    duration=3.878,
                ),
                LerpFunc(
                    fade_background_to_white,
                    fromData=0,
                    toData=1,
                    duration=1.0,
                ),
            ),
        )
        return effects

    def teardown(self):
        self.teardown_background_scene()
        self.logo_animation.cleanup()
        # FIXME: Destroy self.logo_sound
        # FIXME: Destroy the extra buffer stuff

    def setup_background_scene(self, bg_camera):
        """
        Override this to set up the scene that will be seen through the
        splash's shards.

        bg_camera
          The camera watching the background scene
        """
        # The scene to be rendered to texture
        bg_scene = NodePath("My Scene")
        bg_camera.reparent_to(bg_scene)
        bg_camera.set_pos(0, -100, 50)
        bg_camera.look_at(0, 0, 0)

        model = base.loader.loadModel('models/environment')
        model.reparent_to(bg_scene)
        model.set_scale(0.25)

    def teardown_background_scene(self):
        """
        Override this to tear down your scene again.
        """
        pass
