import argparse, datetime

def import_data(path):
    args_list = []
    string_list = []
    with open(path, 'r') as file:
        index = 0
        range
        for line in file:
            if index == 0:
                index += 1
                continue
            args_list.append(line.split())

        # fill the memory list of 0 of the size of this dataset (plus 1 to make sure we have enough space)
        memory_list = [0 for temp in range(max(int(coords[1]) for coords in args_list)+1)]
        for coords in args_list: # for each set of x1, x2, h of the list
            for x_coords in range(int(coords[0]), int(coords[1])): # for each x1 and x2 of the list
                if int(coords[2]) > memory_list[x_coords]:
                    memory_list[x_coords]=int(coords[2])
        
        no_building = True # value used to get to the first x where y is not 0
        current_height = 0
        for position in range(len(memory_list)):
            temp_height=memory_list[position]
            if no_building and temp_height==0:
                continue
            elif temp_height!=current_height:
                no_building = False
                string_list.append(f"{position} {temp_height}\n")
            current_height = temp_height
        return string_list

def write_string(string_list):
    with open('./TP1/data/result.txt', 'w') as file:
        index = 0
        total_string = len(string_list)
        for string in string_list:
            if index == total_string - 1:
                string = string[:-1]
            file.write(string)
            index += 1

if __name__ == '__main__':
    # Parse arguments
    now = datetime.datetime.now()
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file", \
                        help="Data file to import", \
                        action='store', required=True, metavar='DATA_FILE')

    args = parser.parse_args()
    write_string(import_data(args.file))
    calculated = datetime.datetime.now() - now
    print('time elapse : ', calculated)
