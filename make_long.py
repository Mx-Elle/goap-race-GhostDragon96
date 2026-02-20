# use to make a track really long with pattern. 

from game_world.racetrack import load_track

location = "tracks/step11101.pkl"

track = load_track(location)
track.walls[1::2] = 1
track.wall_colors[1::2] = 1
track.walls[::2, 2::2] = 1
track.wall_colors[::2, 2::10] = 2
track.wall_colors[::2, 4::10] = 3
track.wall_colors[::2, 6::10] = 4
track.wall_colors[::2, 8::10] = 5
track.wall_colors[::2, 10::10] = 6
track.buttons[::2, 1::2] = 1
track.button_colors[::2, 1::10] = 2
track.button_colors[::2, 3::10] = 3
track.button_colors[::2, 5::10] = 4
track.button_colors[::2, 7::10] = 5
track.button_colors[::2, 9::10] = 6
track.button_colors[::2, -1] = 7
track.wall_colors[1::2, 0] = 7
track.active[::2, 2::2] = 0
track.active[3::4, 0] = 0
track.save(location)