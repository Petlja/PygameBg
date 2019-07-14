import pygame as pg
import inspect

class pg_frame:
    def __init__(self, rate, seq, surf):
        self.sequence = seq
        self.events = []
        self.rate = rate
        self.period = 1 / rate
        self.surface = surf
        self._mouse_left_index = 0
        self.mouse_pos = None

    def _key_count(self, key):
        cnt = 0
        for e in self.events:
            if e.type == pg.KEYDOWN and e.key == key:
                cnt += 1
        return cnt

    def key_left_count(self):
        return self._key_count(pg.K_LEFT)

    def key_right_count(self):
        return self._key_count(pg.K_RIGHT)

    def key_up_count(self):
        return self._key_count(pg.K_UP)

    def key_down_count(self):
        return self._key_count(pg.K_DOWN)

    def key_space_count(self):
        return self._key_count(pg.K_SPACE)

    def mouse_left_clicked(self):
        while (self._mouse_left_index < len(self.events) and
               self.events[self._mouse_left_index].type != pg.MOUSEBUTTONDOWN):
            self._mouse_left_index += 1
        if self._mouse_left_index < len(self.events):
            e = self.events[self._mouse_left_index]
            self.mouse_pos = e.pos
            self._mouse_left_index += 1
            return True
        return None

def frames(rate, width=None, height=None, caption=None):
    if pg.get_init():
        if width is not None:
            raise ValueError("Argument 'width' is not expected when pygame is allready initialized")
        if height is not None:
            raise ValueError("Argument 'width' is not expected when pygame is allready initialized")
        if caption is not None:
            raise ValueError("Argument 'height' is not expected when pygame is allready initialized")
        surf = None
        manage_init = False
    else:
        pg.init()
        if width is not None:
            surf = pg.display.set_mode((width,height))
        else:
            surf = pg.display.set_mode((500,500))
        if caption is not None:
            pg.display.set_caption(caption)
        pg.key.set_repeat(500, 10)  
        manage_init = True

    sat = pg.time.Clock() 
    kraj = False
    seq = 0
    while not kraj:
        frm = pg_frame(rate, seq, surf)
        seq += 1
        for dogadjaj in pg.event.get():
            if dogadjaj.type == pg.QUIT:
                kraj = True
            else:
                frm.events.append(dogadjaj)
        yield frm
        pg.display.update()
        sat.tick(rate)
    if manage_init:
        pg.quit()

def init(width=None, height=None, caption=None):
    pg.init()
    if width is not None:
        surf = pg.display.set_mode((width,height))
    else:
        surf = pg.display.set_mode((500,500))
    if caption is not None:
        pg.display.set_caption(caption)
    pg.key.set_repeat(500, 10)
    return surf


def run(rate = None, process_frame=None):
    if rate is None:
        rate = 30
    for frm in frames(rate):
        if process_frame:
            params = inspect.signature(process_frame).parameters
            if not params:
                process_frame()
            else:
                process_frame(frm)


