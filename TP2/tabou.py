import argparse
import datetime
import random


def open_file(path):
    args_list = []
    with open(path, 'r') as file:
        for line in file:
            splitted_lines = line.split()
            args_list.append((int(splitted_lines[0]), int(splitted_lines[1]), int(splitted_lines[2])))
    return args_list

def compute_highest_tower(coords_list):
    total_height, tower = glouton(coords_list)
    used_objects = []
    tabou_list = []
    iteration = 0
    current_tower = tower
    while iteration < 100:
        neighbor_height, neighbor_tower, tabou_list = get_best_neighbor(current_tower, tabou_list, coords_list)
        current_tower = neighbor_tower
        if neighbor_height > total_height:
            iteration = 0
            tower = neighbor_tower
            total_height = neighbor_height
        else:
            iteration += 1
        tabou_list = check_tabou(tabou_list)

    quick_sort_area(tower)
    for block in tower:
        coords = block
        current_l, current_p, current_h = coords[1], coords[2], coords[0]
        used_objects.append(f"{current_h} {current_l} {current_p}\n")

    return total_height, used_objects

def check_tabou(tabou_list):
    blocks_to_remove = []
    for block in tabou_list:
        if block[1] > 0:
            block[1] -= 1
        else:
            blocks_to_remove.append(block)

    for block in blocks_to_remove:
        tabou_list.remove(block)
    return tabou_list

def get_best_neighbor(tower, tabou_list, coords_list):
    tabou = [coords[0] for coords in tabou_list]
    blocks_to_test = [block for block in coords_list if block not in tower and block not in tabou]
    best_height = 0
    best_block = []
    for block_to_test in blocks_to_test:
        current_l, current_p, current_h = block_to_test[1], block_to_test[2], block_to_test[0]
        current_tower_height = current_h
        for block in tower:
            l, p, h = block[1], block[2], block[0]
            if l < current_l and p < current_p:
                current_tower_height += h
            elif current_l < l and current_p < p:
                current_tower_height += h
        if current_tower_height > best_height:
            best_block = block_to_test
    new_tower, tabou_list = build_neighbor(tower, best_block, tabou_list)

    return best_height, new_tower, tabou_list

def build_neighbor(tower, new_block, tabou_list):
    new_tower = []
    current_l, current_p, current_h = new_block[1], new_block[2], new_block[0]
    new_tower.append(new_block)
    for block in tower:
        l, p, h = block[1], block[2], block[0]
        if l < current_l and p < current_p:
            new_tower.append(block)
        elif current_l < l and current_p < p:
            new_tower.append(block)
        else:
            tabou_list.append([block, random.randint(7,10)])

    quick_sort_area(new_tower)
    return new_tower, tabou_list

def glouton(coords_list):
    height = 0
    prev_l, prev_p = 0, 0
    tower = []
    for count, coords in enumerate(coords_list):
        current_l, current_p, current_h = coords[1], coords[2], coords[0]
        if (prev_l > current_l and prev_p > current_p) or (count == 0):
            height += current_h
            prev_l, prev_p = current_l, current_p
            tower.append(coords)
    return height, tower

def take_second(elem):
    return elem[1]

def take_third(elem):
    return elem[2]

def take_surface(elem):
    return elem[1]*elem[2]

def quick_sort_area(list_to_sort):
    list_to_sort.sort(key=take_surface, reverse=True)
    return list_to_sort

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