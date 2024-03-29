import pygame as pg

__version__ = "0.9.3"

def open_window(width, height, caption):
    pg.init()
    surface = pg.display.set_mode((width,height))
    pg.display.set_caption(caption)
    return surface

def wait_loop():
    pg.display.update()
    while pg.event.wait().type != pg.QUIT:
        pass
    pg.quit()

def frame_loop(rate, update_frame, handle_event=None):
    clock = pg.time.Clock()
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                return
            _call_event_handler(handle_event, event)
        update_frame()
        pg.display.update()
        clock.tick(rate)

def event_loop(draw, handle_event):
    draw()
    pg.display.update()
    while True:
        need_to_redraw = False
        for event in [pg.event.wait()] + pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                return
            if _call_event_handler(handle_event, event):
                need_to_redraw = True
        if need_to_redraw:
            draw()
            pg.display.update()

def _call_event_handler(handle_event, event):
    if isinstance(handle_event, dict):
        if event.type in handle_event:
            return handle_event[event.type](event)
    elif handle_event:
        return handle_event(event)
    return None
