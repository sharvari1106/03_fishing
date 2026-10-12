
"""
catch: hook-vs-fish catch detection.
"""

import pygame


def check_catch(hook, fish_list):
    """
    Returns the fish caught by the hook only when their
    bounding rectangles overlap.
    """
    hook_rect = pygame.Rect(
        int(hook.x - 7),
        int(hook.y - 7),
        14,
        14
    )

    for fish in fish_list:
        if hook_rect.colliderect(fish.get_rect()):
            return fish

    return None
