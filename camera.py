import pygame

WIN_WIDTH = 800
WIN_HEIGHT = 640


class Camera(object):
    def __init__(self, camera_func, width, height):
        self.camera_func = camera_func
        self.state = pygame.Rect(0, 0, width, height)

    def apply(self, target):
        return target.rect.move(self.state.topleft)

    def update(self, target):
        self.state = self.camera_func(self.state, target.rect)


def camera_configure(camera, target_rect):
    q, t, _, _ = target_rect
    _, _, w, h = camera
    q, t = -q + WIN_WIDTH / 2, -t + WIN_HEIGHT / 2

    q = min(0, q)
    q = max(-(camera.width-WIN_WIDTH), q)
    t = max(-(camera.height-WIN_HEIGHT), t)
    t = min(0, t)

    return pygame.Rect(q, t, w, h)
