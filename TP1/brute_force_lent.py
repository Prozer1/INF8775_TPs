import argparse
import datetime

def open_file(path):
    args_list = []
    with open(path, 'r') as file:
        index = 0
        range
        for line in file:
            if index == 0:
                index += 1
                continue
            args_list.append(line.split())
    return args_list

def create_crit_point(args_list):
    crit_points = []
    for coords in args_list: # for each set of x1, x2, h of the list
        crit_points.append((int(coords[0]), int(coords[2]))) # x1, h
        crit_points.append((int(coords[1]), 0)) # x2, 0
    crit_points.sort()
    return crit_points

def compute_skyline(args_list, crit_points):
    solution = []
    last_point = (-1,-1)
    for coords in crit_points:
        crit_x = int(coords[0])
        crit_y = int(coords[1])
        for buildings in args_list:
            x_1, x_2, h = int(buildings[0]), int(buildings[1]), int(buildings[2])
            if ((crit_x >= x_1 and crit_x < x_2) and (crit_y >= 0 and crit_y <= h)):
                if crit_y < h:
                    crit_y = h
        if crit_y != last_point[1]:
            solution.append(f"{crit_x} {crit_y}\n")
            last_point = (crit_x, crit_y)
    return solution


def write_string(string_list):
    with open('./data/result.txt', 'w') as file:
        index = 0
        total_string = len(string_list)
        for string in string_list:
            if index == total_string - 1:
                string = string[:-1]
            file.write(string)
            index += 1

if __name__ == '__main__':
    # Parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file", \
                        help="Data file to import", \
                        action='store', required=True, metavar='DATA_FILE')
    parser.add_argument("-t", "--time", help="time display")

    args = parser.parse_args()
    args_list = open_file(args.file)
    now = datetime.datetime.now()
    write_string(compute_skyline(args_list, create_crit_point(args_list)))
    calculated = datetime.datetime.now() - now
    calculated = calculated.total_seconds() * 1000.0
    if args.time == "True":
        print(calculated)