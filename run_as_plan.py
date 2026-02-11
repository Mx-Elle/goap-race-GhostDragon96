from game import Game, watch_replay
from jack_bot import plan
from game_world.racetrack import load_track

TRACK = load_track("./tracks/complicated_test.pkl")
PLAYER = plan
REPLAY_SPEED = .01  # seconds per move in the replay. (lower is faster)
SHOW_REPLAY = True

def main():
    path = PLAYER(TRACK.spawn, TRACK)
    if path is None:
        print('Failed to make plan')
        return
    
    vector_path = []
    prev_point = (0, 0)

    for point in path:
        vector_path.append((point[0] - prev_point[0], point[1] - prev_point[1]))
        prev_point = point
    path_len = len(vector_path)
    if SHOW_REPLAY:
        watch_replay(TRACK, vector_path, REPLAY_SPEED)
    print(f'Player took {path_len} moves to finish.')


if __name__ == "__main__":
    main()