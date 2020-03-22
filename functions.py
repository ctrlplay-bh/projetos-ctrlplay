from operator import itemgetter


def sort_and_sweep(balls):
    active_balls = []
    markers_list = []
    for ball in balls:
        markers_list.append((ball._x_start, ball, 'start'))
        markers_list.append((ball._x_end, ball, 'end'))
    markers_list.sort(key=itemgetter(0))

    for marker in markers_list:
        test_ball_collision = marker[1]
        if marker[2] == 'start':
            for ball in active_balls:
                test_ball_collision.collision(ball)
            active_balls.append(marker[1])
        elif marker[2] == 'end':
            active_balls.remove(test_ball_collision)