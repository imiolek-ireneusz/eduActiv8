import os

try:
    import android
except ImportError:
    android = None

try:
    import pygame.mixer as mixer
except ImportError:
    if android is not None:
        try:
            import android.mixer as mixer
        except ImportError:
            mixer = None


class SoundFX:
    def __init__(self, mainloop):
        self.mainloop = mainloop
        self.initialized = False
        try:
            sounds = mixer
            sounds.init()

            # reload game
            self.s1 = sounds.Sound(os.path.join('res', 'sounds', 'sfx_select06_rev.ogg'))

            # showing dialog
            self.s2 = sounds.Sound(os.path.join('res', 'sounds', 'sfx_whistle02_rstartx.ogg'))

            # category selected
            self.s3 = sounds.Sound(os.path.join('res', 'sounds', 'sfx_select02.ogg'))

            # game selected
            self.s4 = sounds.Sound(os.path.join('res', 'sounds', 'sfx_select01.ogg'))

            # category group open
            self.s5 = sounds.Sound(os.path.join('res', 'sounds', 'sfx_select03_rev.ogg'))

            # close group close
            self.s6 = sounds.Sound(os.path.join('res', 'sounds', 'sfx_select03.ogg'))

            # increase level
            self.s7 = sounds.Sound(os.path.join('res', 'sounds', 'sfx_select04.ogg'))

            # decrease level
            self.s9 = sounds.Sound(os.path.join('res', 'sounds', 'sfx_select05.ogg'))

            # game failed
            self.s8 = sounds.Sound(os.path.join('res', 'sounds', '146731__fins__game-fail.ogg'))

            # object motion
            self.s10 = sounds.Sound(os.path.join('res', 'sounds', 'sfx_slide05.ogg'))

            # object unable to move
            self.s11 = sounds.Sound(os.path.join('res', 'sounds', 'sfx_noise01.ogg'))

            # hit the mole - deactivated
            self.s12 = sounds.Sound(os.path.join('res', 'sounds', '188043__antumdeluge__mouse.ogg'))

            # level completed
            self.s13 = sounds.Sound(os.path.join('res', 'sounds', 'sfx_whistle03.ogg'))

            # game completed
            self.s14 = sounds.Sound(os.path.join('res', 'sounds', 'sfx_whistle04.ogg'))

            # keyboard press
            self.s15 = sounds.Sound(os.path.join('res', 'sounds', 'sfx_press01.ogg'))

            # keyboard wrong btn
            self.s16 = sounds.Sound(os.path.join('res', 'sounds', 'sfx_press02_rev.ogg'))

            self.initialized = True
        except:
            self.initialized = False

    def play(self, sound_id):
        if self.mainloop.config.settings["sounds"]:
            try:
                if self.initialized:
                    eval("self.s%i.play()" % sound_id)
            except:
                pass
