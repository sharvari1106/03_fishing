
import random
import pygame

from game.hook import Hook, IDLE
from game.fish import Fish
from game.catch import check_catch
from game.renderer import WIDTH, HEIGHT, SURFACE_Y, MAX_DEPTH_Y

ROUND_DURATION = 30


class GameEngine:
    def __init__(self):
        self.reset()

    def reset(self):
        self.hook = Hook(
            x=WIDTH / 2,
            surface_y=SURFACE_Y,
            max_depth_y=MAX_DEPTH_Y,
            speed=5,
        )

        self.fish_list = [
            Fish(100, 180, 3, 30, 15, 10, (80, 180, 220)),
            Fish(400, 280, -2, 42, 22, 20, (80, 220, 120)),
            Fish(250, 380, 4, 52, 28, 30, (240, 170, 60)),
            Fish(550, 230, -3, 26, 14, 50, (230, 90, 140)),
        ]

        self.hooked_fish = None
        self.score = 0
        self.start_time = pygame.time.get_ticks()
        self.game_over = False

    def start_cast(self):
        if not self.game_over and self.hook.state == IDLE:
            self.hook.start_cast()

    def update(self):
        if self.game_over:
            return

        elapsed = (pygame.time.get_ticks() - self.start_time) / 1000
        if elapsed >= ROUND_DURATION:
            self.game_over = True
            self.hooked_fish = None
            return

        self.hook.update()

        for fish in self.fish_list:
            fish.update(WIDTH)

        if self.hooked_fish is not None:
            self.hooked_fish.x = self.hook.x
            self.hooked_fish.y = self.hook.y

            if self.hook.state == IDLE:
                self.score += self.hooked_fish.point_value
                self.hooked_fish = None

        else:
            caught = check_catch(self.hook, self.fish_list)
            if caught is not None:
                self.fish_list.remove(caught)
                self.hooked_fish = caught
                self.hooked_fish.x = self.hook.x
                self.hooked_fish.y = self.hook.y
                self.hook.catch_fish()

        # Replenish the school of fish after successful catches.
        while len(self.fish_list) < 4:
            fish_types = [
                (30, 15, 10, (80, 180, 220), 2),
                (42, 22, 20, (80, 220, 120), 2),
                (52, 28, 30, (240, 170, 60), 3),
                (26, 14, 50, (230, 90, 140), 4),
            ]
            w, h, points, color, speed = random.choice(fish_types)
            direction = random.choice([-1, 1])
            x = random.randint(0, WIDTH)
            y = random.choice([160, 220, 280, 340, 400])
            self.fish_list.append(
                Fish(x, y, speed * direction, w, h, points, color)
            )

    def draw(self, surface, font):
        from game import renderer

        draw_list = list(self.fish_list)
        if self.hooked_fish is not None:
            draw_list.append(self.hooked_fish)

        renderer.draw_scene(surface, self.hook, draw_list)
        renderer.draw_text(
            surface, font, f"Score: {self.score}", (10, 10)
        )

        if not self.game_over:
            elapsed = (pygame.time.get_ticks() - self.start_time) / 1000
            remaining = max(0, int(ROUND_DURATION - elapsed + 0.999))
            renderer.draw_text(
                surface, font, f"Time: {remaining}s", (570, 10)
            )
        else:
            renderer.draw_banner(
                surface, font, "TIME UP! Final score: " + str(self.score)
            )
            renderer.draw_text(
                surface, font, "Press R to restart", (235, 280)
            )
