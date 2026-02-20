from collections import defaultdict
from copy import deepcopy
from functools import cache
import heapq
import time

from game_world.racetrack import RaceTrack

Point = tuple[int, int]


class Bot_Action:

    def __init__(self) -> None:
        self.path: None | list[Point] = None
        self.frontier = []
        self.g_scores = defaultdict(lambda: float("inf"))
        self.backtracking: dict[tuple[Point, bytes], tuple[Point, bytes] | None] = {}
        self.tie_break = 0

    def __call__(self, location: Point, track: RaceTrack) -> Point:
        if self.path is None:

            if self.frontier == [] or self.g_scores == {} or self.backtracking == {}:
                heapq.heappush(
                    self.frontier,
                    (
                        distance(location, track.target),
                        0,
                        self.tie_break,
                        location,
                        deepcopy(track),
                    ),
                )
                self.g_scores[(location, track.active.tobytes())] = 0
                self.backtracking = {}

            self.backtracking[(location, track.active.tobytes())] = None

            path, early_escape = self.plan(location, track)

            if early_escape and path:
                return (path[0][0] - location[0], path[0][1] - location[1])
            else:
                self.path = path

        if self.path is None:
            raise Exception("No possible path")

        next_move = self.path.pop(0)
        return (next_move[0] - location[0], next_move[1] - location[1])

    def plan(
        self, start_point: Point, track: RaceTrack
    ) -> tuple[list[Point] | None, bool]:
        start = time.time()

        found_path: bool = False
        need_to_make_a_move = False

        curr = start_point
        curr_track = deepcopy(track)

        while self.frontier != []:
            _, curr_g, _, curr, curr_track = heapq.heappop(self.frontier)

            if curr == track.target:
                found_path = True
                break

            if curr_g > self.g_scores[(curr, curr_track.active.tobytes())]:
                continue

            for act_point, act_track in actions_from_state(curr, deepcopy(curr_track)):
                new_cost = self.g_scores[(curr, curr_track.active.tobytes())] + 1
                act_track = deepcopy(act_track)
                if self.g_scores[(act_point, act_track.active.tobytes())] > new_cost:
                    self.g_scores[(act_point, act_track.active.tobytes())] = new_cost
                    self.tie_break += 1
                    heapq.heappush(
                        self.frontier,
                        (
                            new_cost + distance(act_point, act_track.target),
                            new_cost,
                            self.tie_break,
                            act_point,
                            act_track,
                        ),
                    )
                    self.backtracking[(act_point, act_track.active.tobytes())] = (
                        curr,
                        curr_track.active.tobytes(),
                    )

            if time.time() - start >= (5 - 1e-5):
                need_to_make_a_move = True
                break

        if not found_path and not need_to_make_a_move:
            # if the while ends and we never found a path then there are no paths
            print("path not found", need_to_make_a_move)
            return None, False

        last: tuple[Point, bytes] | None = (curr, curr_track.active.tobytes())
        moves: list[Point] = []
        while last is not None:
            moves.append(last[0])
            last = self.backtracking[last]

        return moves[::-1][1:], need_to_make_a_move


def distance(point_a: Point, point_b: Point):
    return abs(point_b[0] - point_a[0]) + abs(point_b[1] - point_a[1])


def find_button_color(track: RaceTrack, pt: Point):
    return track.button_colors[pt[0]][pt[1]] if track.buttons[pt[0]][pt[1]] == 1 else 0


@cache
def actions_from_state(
    location: Point, track: RaceTrack
) -> set[tuple[Point, RaceTrack]]:
    actions = set()
    max_x, max_y = track.active.shape
    for opt in [(1, 0), (0, 1), (-1, 0), (0, -1)]:
        neighbor = (location[0] + opt[0], location[1] + opt[1])
        if (
            neighbor[0] < 0
            or neighbor[1] < 0
            or neighbor[0] >= max_x
            or neighbor[1] >= max_y
            or (
                track.active[neighbor[0]][neighbor[1]] == 1
                and track.walls[neighbor[0]][neighbor[1]] != 0
            )
        ):
            continue
        button = find_button_color(track, neighbor)
        new_track = deepcopy(track)
        if button != 0:
            new_track.toggle(button)
        actions.add((neighbor, new_track))
    return actions
