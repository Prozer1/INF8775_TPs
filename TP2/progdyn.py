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
    used_objects = []
    max_list = [] #[[H, Coords, Previous, Id],...]
    for count, coords in enumerate(coords_list):
        current_l, current_p, current_h = coords[1], coords[2], coords[0]
        if (count != 0):
            potential_list = []
            for i in range(0,count):
                if coords_list[i][1] > current_l and coords_list[i][2] > current_p:
                    potential_list.append(max_list[i])
            if len(potential_list) == 0:
                max_list.append([current_h, coords, -1, count])
            else:
                previous_block = max(potential_list, key=take_H)
                max_list.append([current_h + previous_block[0], coords, previous_block[3], count])
        else:
            max_list.append([current_h, coords, -1, 0])

    highest_block = max(max_list, key=take_H) #ID du maximum block
    tower = []
    while highest_block[2] != -1:
        tower.insert(0,highest_block)
        highest_block = max_list[highest_block[2]]
    tower.insert(0,highest_block)

    for block in tower:
        coords = block[1]
        current_l, current_p, current_h = coords[1], coords[2], coords[0]
        total_height += current_h
        used_objects.append(f"{current_h} {current_l} {current_p}\n")

    return total_height, used_objects

def take_surface(elem):
    return elem[1]*elem[2]

def take_H(elem):
    return elem[0]

def quick_sort(list_to_sort):
    list_to_sort.sort(key=take_surface, reverse=True)
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

    args = parser.parse_args()
    args_list = open_file(args.file)
    now = datetime.datetime.now()
    args_list_sorted = quick_sort(args_list)
    total_height, object_string = compute_highest_tower(args_list_sorted)
    write_string(object_string)
    print(f"{total_height=}")
    calculated = datetime.datetime.now() - now
    calculated = calculated.total_seconds() * 1000.0
    if args.time:
        print(f"{calculated}ms")
        
        