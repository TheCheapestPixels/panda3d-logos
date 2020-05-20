import sys

from direct.showbase.ShowBase import ShowBase

from panda3d_logos.splashes import RainbowSplash

#loadPrcFileData('', 'fullscreen true')
#loadPrcFileData('', 'framebuffer-multisample 1')
#loadPrcFileData('', 'multisamples 2')


class SplashBase(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        self.accept('escape', sys.exit)

        splash = RainbowSplash()
        self.interval = splash.setup()
        self.interval.start()
        base.task_mgr.add(self.quit_after_interval, sort=25)

    def quit_after_interval(self, task):
        if self.interval.isStopped():
            sys.exit()
        return task.cont


def main():
    app = SplashBase()
    app.run()


if __name__ == '__main__':
    main()
