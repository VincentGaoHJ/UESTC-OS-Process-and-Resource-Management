# -*- coding: utf-8 -*-
"""
@Date: Created on 2019/5/19
@Author: Haojun Gao
@Description:
"""

import sys
import ProcessResourceManager as Manager


def get_order(elem_list):
    command = ""
    name = ""
    num = ""
    if len(elem_list) >= 1:
        command = elem_list[0]
    else:
        print("[Error] There is no command in the input file.")
    if len(elem_list) >= 2:
        name = elem_list[1]
    if len(elem_list) == 3:
        num = int(elem_list[2])
    if len(elem_list) > 3:
        print("[Error] The command line parameters are more than two.")

    return command, name, num


def main(arg):
    input_file = open(arg, encoding="UTF-8")
    shell_order = [line.strip().split() for line in input_file.readlines()]
    input_file.close()

    prm = Manager.ProcessResourceManager()
    print("init", end=" ")
    name = ''
    num = -1

    for order_elem in shell_order:

        command, name, num = get_order(order_elem)  # 获取命令成分

        # print(command, name, num)

        if command == 'init':  # 初始化
            prm.store()
            print(prm.pcb[prm.running_process].pid, end=' ')

        elif command == 'cr':  # create
            if prm.contain(name) != -1:
                print("[Error] The process {name} is already exist.", end=' ')
                continue
            if num > 2 or num <= 0:
                print("[Error] The priority {num} is not an option.", end=' ')
                continue

            prm.create(name, num)
            print(prm.pcb[prm.running_process].pid, end=' ')

        elif command == 'de':  # destroy
            t = prm.contain(name)
            # print(t)
            if t == -1:
                print("[Error] The process {name} is not exist.", end=' ')
                continue

            prm.destroy(t)
            print(prm.pcb[prm.running_process].pid, end=' ')

        elif command == 'req' or command == 'rel':  # Request or Release
            name_id = int(name[-1]) - 1
            if name == "R1" and num == 1:
                pass
            elif name == 'R2' and 0 < num <= 2:
                pass
            elif name == 'R3' and 0 < num <= 3:
                pass
            elif name == 'R4' and 0 < num <= 4:
                pass
            else:
                print("[Error] The {command} number {num} of the process {name} is invalid.")
                continue

            if command == 'req':
                prm.request(name_id, num)
            else:
                # print(prm.pcb[prm.running_process].Other_Resource[name_id].used)
                if prm.pcb[prm.running_process].Other_Resource[name_id].used >= num:
                    prm.release(name_id, num)
                else:
                    print("[Error] The release number {} of the process {} is exceed.".format(num, name))
                    continue

            print(prm.pcb[prm.running_process].pid, end=' ')

        elif command == 'lr':  #
            prm.Resource_Listing()

        elif command == 'lp':
            prm.Process_Listing()

        elif command == 'pinfo':
            prm.Process_Info(order_elem[1:])

        elif command == 'to':
            prm.Time_Out()
            print(prm.pcb[prm.running_process].pid, end=' ')

        else:
            print("[Error] There comes an unknown error that is beyond 高浩峻's control.")

        # prm.Process_Listing()
        # prm.Resource_Listing()
        # prm.Process_Info(order_elem[1:])


if __name__ == '__main__':

    # argv = input('Please input the name of the test file')
    # main(argv)
    # print()
    # input('press enter key to exit')

    if len(sys.argv) == 1:
        main("input.txt")
    else:
        main(sys.argv[1])
