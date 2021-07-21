import numpy as np
import math
from scipy.optimize import least_squares

from data import ReceiveRecord
from gps import get_mean_latlong, LatLongToPoint, PointToLatLong, Point
from typing import List

def records_to_np(records: List[ReceiveRecord]):
    rec_times = np.array([
        rec.ts for rec in records
        ])

    mean_latlong = get_mean_latlong([rec.receiverCoord for rec in records])

    towers = np.array([
          [p.x, p.y] for p in (LatLongToPoint(rec.receiverCoord, mean_latlong) for rec in records)
        ])

    return rec_times, towers, mean_latlong

def solve(rec_times, towers):

    v = 3e8

    c = np.argmin(rec_times)
    p_c = np.expand_dims(towers[c], axis=0)
    t_c = rec_times[c]

    # Remove the c tower to allow for vectorization.
    all_p_i = np.delete(towers, c, axis=0)
    all_t_i = np.delete(rec_times, c, axis=0)

    def eval_solution(x):
        """ x is 2 element array of x, y of the transmitter"""
        return (
              np.linalg.norm(x - p_c, axis=1)
            - np.linalg.norm(x - all_p_i, axis=1)
            + v*(all_t_i - t_c)
        )

    # Initial guess.
    x_init = [0, 0]

    # Find a value of x such that eval_solution is minimized.
    # Remember the receive times have error added to them: rec_time_noise_stdd.
    res = least_squares(eval_solution, x_init)

    return res

def solve_gps(records: List[ReceiveRecord]):
    rec_times, towers, mean_latlong = records_to_np(records)

    solution = solve(rec_times, towers)

    solution_gps = PointToLatLong(Point(solution.x[0], solution.x[1]), mean_latlong)

    return solution_gps
