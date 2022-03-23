import argparse
import datetime

def open_file(path):
    args_list = []
    with open(path, 'r') as file:
        for line in file:
            splitted_lines = line.split()
            args_list.append((int(splitted_lines[0]),int(splitted_lines[1]),int(splitted_lines[2])))
    return args_list

def compute_highest_tower(coords_list):
    total_height = 0
    prev_l, prev_p = 0,0
    used_objects = []
    for count, coords in enumerate(coords_list):
        current_l, current_p, current_h = coords[1], coords[2], coords[0]
        if (prev_l > current_l and prev_p > current_p) or (count == 0):
            total_height += current_h
            prev_l, prev_p = current_l, current_p
            used_objects.append(f"{current_h} {current_l} {current_p}\n")
    return total_height, used_objects

def take_second(elem):
    return elem[1]

def take_third(elem):
    return elem[2]

def quick_sort(by, list_to_sort):
    if by == 'h':
        list_to_sort.sort(reverse=True)
    elif by == 'l':
        list_to_sort.sort(key=take_second, reverse=True)
    elif by == 'p':
        list_to_sort.sort(key=take_third, reverse=True)
    return list_to_sort
            

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
    parser.add_argument("-t", "--time", action='store_true', help="time display")
    parser.add_argument("-b", "--by", help="sorted by.", choices=['h', 'l', 'p'], default='l')

    args = parser.parse_args()
    args_list = open_file(args.file)
    now = datetime.datetime.now()
    args_list_sorted = quick_sort(args.by, args_list)
    total_height, object_string = compute_highest_tower(args_list_sorted)
    write_string(object_string)
    print(f"{total_height=}")
    calculated = datetime.datetime.now() - now
    calculated = calculated.total_seconds() * 1000.0
    if args.time:
        print(f"{calculated}ms")
        
        