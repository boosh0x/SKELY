import pyxel

TILE = 8
TRANSPARENT_COLOR = 0  # currently have it as 0 for black but might want to change if I update the colors
WINCODE = "HACK"

COIN_IMG = 0
COIN_UV = (32, 0)
COIN_W = 16
COIN_H = 16

# player animations
IDLE_FRAMES = [(16, 0)]
RUN_FRAMES = [(48, 0), (64, 0)]
JUMP_FRAMES = [(80, 0)]
FALL_FRAMES = [(96, 0)]
ANIM_SPEED = 6  


class App:
    def __init__(self):
        pyxel.init(160, 120, title="SKELY", fps=60)
        pyxel.load("my_resource.pyxres")

        self.tm = pyxel.tilemaps[0]
        self.tm.imgsrc = 0

        self.x, self.y = 0.0, 80.0
        self.vy = 0.0
        self.w, self.h = 16, 16
        self.on_ground = True
        self.score = 0
        self.dir = 1
        self.anim = "idle"

        self.coins = [
            (8, 40),
            (24, 40),
            (40, 40),
            (72, 40),
            (88, 40),
            (104, 40),
        ]
        self.total_coins = len(self.coins)

        self.state = "menu"  

        # music
        pyxel.playm(0, loop=True)

        pyxel.run(self.update, self.draw)

    @staticmethod
    def aabb(ax, ay, aw, ah, bx, by, bw, bh):
        return ax < bx + bw and ax + aw > bx and ay < by + bh and ay + ah > by

    def reset_run(self):
        self.x, self.y = 0.0, 80.0
        self.vy = 0.0
        self.on_ground = True
        self.score = 0
        self.dir = 1
        self.anim = "idle"
        self.coins = [
            (8, 40),
            (24, 40),
            (40, 40),
            (72, 40),
            (88, 40),
            (104, 40),
        ]
        self.total_coins = len(self.coins)

    def update(self):
        if self.state == "menu":
            self.update_menu()
        elif self.state == "play":
            self.update_play()
        elif self.state == "win":
            self.update_win()

    def update_menu(self):
        if pyxel.btnp(pyxel.KEY_Q) or pyxel.btnp(pyxel.KEY_ESCAPE):
            pyxel.quit()
        if (
            pyxel.btnp(pyxel.KEY_RETURN)
            or pyxel.btnp(pyxel.KEY_SPACE)
            or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_START)
        ):
            self.reset_run()
            self.state = "play"

    def update_play(self):
        if pyxel.btnp(pyxel.KEY_Q) or pyxel.btnp(pyxel.KEY_ESCAPE):
            pyxel.quit()
        if pyxel.btnp(pyxel.KEY_R):
            self.reset_run()

        moving_left = pyxel.btn(pyxel.KEY_A) or pyxel.btn(
            pyxel.GAMEPAD1_BUTTON_DPAD_LEFT
        )
        moving_right = pyxel.btn(pyxel.KEY_D) or pyxel.btn(
            pyxel.GAMEPAD1_BUTTON_DPAD_RIGHT
        )

        if moving_left:
            self.x -= 1.5
            self.dir = -1
        if moving_right:
            self.x += 1.5
            self.dir = 1

        if self.on_ground and (
            pyxel.btnp(pyxel.KEY_SPACE) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_A)
        ):
            self.vy = -4
            self.on_ground = False
            pyxel.play(3, 12)

        self.vy += 0.25
        self.y += self.vy

        self.on_ground = False

        if self.y >= 89:
            self.y = 89
            self.vy = 0
            self.on_ground = True
        elif (160 >= self.x >= 135) and (68 > self.y >= 65):
            self.y = 65
            self.vy = 0
            self.on_ground = True
        elif (115 >= self.x >= 61) and (44 > self.y >= 41):
            self.y = 41
            self.vy = 0
            self.on_ground = True
        elif (self.x <= 52) and (44 > self.y >= 41):
            self.y = 41
            self.vy = 0
            self.on_ground = True

        self.x = max(0, min(self.x, pyxel.width - self.w))

        if not self.on_ground:
            self.anim = "jump" if self.vy < 0 else "fall"
        else:
            self.anim = "run" if (moving_left or moving_right) else "idle"

        # coin pickup
        remaining = []
        for cx, cy in self.coins:
            if self.aabb(self.x, self.y, self.w, self.h, cx, cy, COIN_W, COIN_H):
                self.score += 100
                pyxel.play(3, 11)
            else:
                remaining.append((cx, cy))
        self.coins = remaining

        if not self.coins:
            self.state = "win"

    def update_win(self):
        if pyxel.btnp(pyxel.KEY_Q) or pyxel.btnp(pyxel.KEY_ESCAPE):
            pyxel.quit()
        if pyxel.btnp(pyxel.KEY_RETURN) or pyxel.btnp(pyxel.KEY_SPACE):
            self.reset_run()
            self.state = "play"
        if pyxel.btnp(pyxel.KEY_M):
            self.state = "menu"

    def draw(self):
        if self.state == "menu":
            self.draw_menu()
        elif self.state == "play":
            self.draw_play()
        elif self.state == "win":
            self.draw_win()

    def draw_menu(self):
        pyxel.cls(0)
        pyxel.blt(0, 0, 0, 0, 48, 160, 120, TRANSPARENT_COLOR)
        self._centered_text(36, "S K E L Y", 10)
        self._centered_text(56, "Press ENTER or SPACE", 7)
        self._centered_text(70, "A/D to move, SPACE to jump", 6)
        self._centered_text(84, "Q=Quit", 13)

    def draw_play(self):
        pyxel.cls(0)
        pyxel.blt(0, 0, 0, 0, 48, 160, 120, TRANSPARENT_COLOR)

        # World
        pyxel.bltm(0, 0, 0, 0, 0, 160, 120, TRANSPARENT_COLOR)

        # Coins
        for cx, cy in self.coins:
            pyxel.blt(
                cx,
                cy,
                COIN_IMG,
                COIN_UV[0],
                COIN_UV[1],
                COIN_W,
                COIN_H,
                TRANSPARENT_COLOR,
            )

        self.draw_player()

        pyxel.text(4, 4, f"SCORE: {self.score}", 7)
        pyxel.text(
            4, 12, f"COINS: {self.total_coins - len(self.coins)}/{self.total_coins}", 7
        )
        pyxel.text(4, 20, "R=Restart  Q=Quit", 5)

    def draw_player(self):
        u, v = self.current_frame()
        fw, fh = 16, 16
        if self.dir == 1:
            pyxel.blt(int(self.x), int(self.y), 0, u, v, fw, fh, TRANSPARENT_COLOR)
        else:
            pyxel.blt(
                int(self.x) + (fw - 13),
                int(self.y),
                0,
                u,
                v,
                -fw,
                fh,
                TRANSPARENT_COLOR,
            )

    def current_frame(self):
        if self.anim == "run":
            frames = RUN_FRAMES
        elif self.anim == "jump":
            frames = JUMP_FRAMES
        elif self.anim == "fall":
            frames = FALL_FRAMES
        else:
            frames = IDLE_FRAMES

        idx = (pyxel.frame_count // ANIM_SPEED) % len(frames)
        return frames[idx]

    def draw_win(self):
        pyxel.cls(0)
        pyxel.blt(0, 0, 0, 0, 48, 160, 120, TRANSPARENT_COLOR)
        self._centered_text(40, "CONGRATS, YOU WON!", 11)
        self._centered_text(56, f"Score: {self.score}", 7)
        self._centered_text(68, f"CODE: {WINCODE}", 10) 
        self._centered_text(82, "ENTER/SPACE: Play Again", 7)
        self._centered_text(94, "M: Menu   Q: Quit", 13)

    def _centered_text(self, y, text, col):
        x = (pyxel.width - len(text) * 4) // 2
        pyxel.text(x + 1, y + 1, text, 1)
        pyxel.text(x, y, text, col)


App()
