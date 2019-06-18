# -*- coding: utf-8 -*-
"""
@Date: Created on 2019/5/19
@Author: Haojun Gao
@Description:
"""


class PCB:
    def __init__(self):
        self.pid = " "
        self.type = "ready"
        self.id = -1
        self.parent = -1
        self.child = -1
        self.younger = -1
        self.elder = -1
        self.priority = -1
        tmp_resource = []
        for i in range(4):
            tmp_resource.append(resource())
        self.Other_Resource = tmp_resource


class RCB:
    def __init__(self):
        self.rid = "Ri"  # Resource's ID
        self.initial = 0  # Initial number of Resource
        self.remain = 0  # Available number of Resource currently
        self.waiting_list = []  # List of blocked process


class resource:
    def __init__(self):
        self.rid = -1
        self.used = 0
        self.waiting_request = 0


def print_output(output):
    if len(output) >= 4:
        end = "\t\t"
    else:
        end = "\t\t\t"
    print(output, end=end)


class ProcessResourceManager:
    def __init__(self):
        self.R1 = RCB()
        self.R1.rid = "R1"
        self.R1.initial = 1
        self.R1.remain = 1

        self.R2 = RCB()
        self.R2.rid = "R2"
        self.R2.initial = 2
        self.R2.remain = 2

        self.R3 = RCB()
        self.R3.rid = "R3"
        self.R3.initial = 3
        self.R3.remain = 3

        self.R4 = RCB()
        self.R4.rid = "R4"
        self.R4.initial = 4
        self.R4.remain = 4

        self.rl = [[], [], []]
        self.del_num = -1
        self.running_process = None

        tmp_rcb = []
        for i in range(4):
            tmp_rcb.append(RCB())
        self.rcb = tmp_rcb
        self.rcb[0] = self.R1
        self.rcb[1] = self.R2
        self.rcb[2] = self.R3
        self.rcb[3] = self.R4

        tmp_pcb = []
        for i in range(20):
            tmp_pcb.append(PCB())
        self.pcb = tmp_pcb
        for i in range(20):
            self.pcb[i].id = i
        self.pcb[0].pid = 'init'
        self.pcb[0].priority = 0
        self.rl[0].append(0)
        self.running_process = 0

    def Scheduler(self):
        # print(self.rl[2])
        # print(self.rl[1])
        # print(self.rl[0])
        if len(self.rl[2]) != 0:
            p = self.pcb[self.running_process].priority
            if p < 2:
                # print("新加入的进程优先级为{}，高于当前进程优先级{}，插入，当前进程滚去排队。".format(2, p))
                if self.running_process in self.rl[p]:  # 如果当前进程还在的话（根据测试用例5，有可能当前进程直接被干掉了）
                    self.rl[p].remove(self.running_process)
                    self.pcb[self.running_process].type = "ready"
                    self.rl[p].append(self.running_process)

            self.running_process = self.rl[2][0]
            self.pcb[self.running_process].type = "running"
            return self.rl[2][0]

        elif len(self.rl[1]) != 0:
            p = self.pcb[self.running_process].priority
            if p < 1:
                # print("新加入的进程优先级为{}，高于当前进程优先级{}，插入，当前进程滚去排队。".format(1, p))
                if self.running_process in self.rl[p]:  # 如果当前进程还在的话（根据测试用例5，有可能当前进程直接被干掉了）
                    self.rl[p].remove(self.running_process)
                    self.pcb[self.running_process].type = "ready"
                    self.rl[p].append(self.running_process)

            self.running_process = self.rl[1][0]
            self.pcb[self.running_process].type = "running"
            return self.rl[1][0]
        else:
            self.running_process = 0
            self.pcb[self.running_process].type = "running"
            return 0

    def Time_Out(self):
        p = self.pcb[self.running_process].priority
        self.rl[p].remove(self.running_process)
        self.pcb[self.running_process].type = "ready"
        self.rl[p].append(self.running_process)
        self.Scheduler()

    def release_control(self, n, unit, i=-1):
        # print("++++++++++++++++++++")
        # print(n)
        # print(unit)
        if i != -1:
            # print(i)
            # print(self.pcb[i].Other_Resource[n].used)
            self.pcb[i].Other_Resource[n].used -= unit
            # print(self.pcb[i].Other_Resource[n].used)
        else:
            # print(self.running_process)
            # print(self.pcb[self.running_process].Other_Resource[n].used)
            self.pcb[self.running_process].Other_Resource[n].used -= unit
        #     print(self.pcb[self.running_process].Other_Resource[n].used)
        # print(self.rcb[n].remain)
        self.rcb[n].remain += unit
        # print(self.rcb[n].remain)
        # print("等待进程")
        if self.rcb[n].waiting_list:
            # print(self.rcb[n].waiting_list)
            tmp_pcb = self.rcb[n].waiting_list[0]
            while (tmp_pcb != 0 and
                   self.pcb[tmp_pcb].Other_Resource[n].waiting_request <= self.rcb[n].remain):
                self.rcb[n].remain -= self.pcb[tmp_pcb].Other_Resource[n].waiting_request
                self.rcb[n].waiting_list.remove(tmp_pcb)
                self.pcb[tmp_pcb].type = "ready"
                self.pcb[tmp_pcb].Other_Resource[n].used += self.pcb[tmp_pcb].Other_Resource[n].waiting_request
                self.rl[self.pcb[tmp_pcb].priority].append(tmp_pcb)
                if len(self.rcb[n].waiting_list):
                    tmp_pcb = self.rcb[n].waiting_list[0]
                else:
                    tmp_pcb = 0

    def release(self, n, unit):
        self.release_control(n, unit)
        self.Scheduler()

    def request(self, n, unit):
        if self.rcb[n].remain >= unit:
            # print("aaaaaaaaaaaaaaaaaaaaaa")
            # print(self.running_process)
            self.rcb[n].remain -= unit
            # print(self.rcb[n].remain)
            self.pcb[self.running_process].Other_Resource[n].rid = n

            # print(self.pcb[self.running_process].Other_Resource[n].used)
            self.pcb[self.running_process].Other_Resource[n].used += unit
            # print(self.pcb[self.running_process].Other_Resource[n].used)
        else:
            self.pcb[self.running_process].type = "blocked"
            self.pcb[self.running_process].Other_Resource[n].waiting_request += unit
            self.rcb[n].waiting_list.append(self.running_process)
            self.rl[self.pcb[self.running_process].priority].remove(self.running_process)
        self.Scheduler()

    def isequal(self, value):
        return value == self.del_num

    def destroy(self, n):
        # print("开始释放{}".format(n))
        for i in range(4):
            if self.pcb[n].Other_Resource[i].used != 0:
                # print("进程{}占用了{}个资源{}，需要释放".format(n, self.pcb[n].Other_Resource[i].used, i))
                self.release_control(i, self.pcb[n].Other_Resource[i].used, n)
                if self.rcb[i].remain > self.rcb[i].initial:
                    print("error in destroy: delete resources exit initial units")
                self.pcb[n].Other_Resource[i].rid = -1
                self.pcb[n].Other_Resource[i].used = 0
            else:
                # print("进程{}占用了{}个资源{}，不需要释放".format(n, self.pcb[n].Other_Resource[i].used, i))
                pass
        if self.pcb[n].type == "ready" or self.pcb[n].type == "running":
            p = self.pcb[n].priority
            self.rl[p].remove(n)
        elif self.pcb[n].type == "blocked":
            for i in range(4):
                if n in self.rcb[i].waiting_list:
                    self.rcb[i].waiting_list.remove(n)
        distroy_list = []
        for i in range(20):
            if self.pcb[i].parent == n:
                distroy_list.append(i)
        if distroy_list:
            # print("又有要删除的了{}".format(distroy_list))
            for item in distroy_list:
                self.destroy(self.pcb[item].id)

        self.pcb[n].pid = " "
        self.pcb[n].type = "ready"
        self.pcb[n].parent = -1
        elder = self.pcb[n].elder
        self.pcb[n].elder = -1
        younger = self.pcb[n].younger
        self.pcb[n].younger = -1
        self.pcb[n].priority = -1
        for j in range(4):
            self.pcb[n].Other_Resource[j].rid = -1
            self.pcb[n].Other_Resource[j].used = 0
            self.pcb[n].Other_Resource[0].waiting_request = 0

        for i in range(20):
            if self.pcb[i].elder == n:
                self.pcb[i].elder = elder
            if self.pcb[i].younger == n:
                self.pcb[i].younger = younger
        self.Scheduler()

    def contain(self, name):
        for i in range(20):
            if name == self.pcb[i].pid:
                return i
        return -1

    def create(self, name, p):
        for i in range(20):
            if self.pcb[i].pid == " ":  # 寻找一个空的pcb
                self.pcb[i].pid = name  # 赋名字
                self.pcb[i].priority = p  # 赋优先级
                self.rl[p].append(self.pcb[i].id)  # 加入到优先级队列中
                self.pcb[i].parent = self.running_process  # 父节点就是当前运行的节点
                if self.pcb[self.running_process].child == -1:  # 如果当前运行的父节点没有子节点，那么新增的节点就是子节点
                    self.pcb[self.running_process].child = i
                for j in range(20):
                    if j < i and self.pcb[j].parent == self.pcb[i].parent:
                        if self.pcb[j].younger == -1:  # 如果当前运行的父节点的子节点没有弟弟，那么新增的节点就是子节点的弟弟
                            self.pcb[j].younger = i
                            self.pcb[i].elder = j  # 那么新增的节点的哥哥，就是当前运行的父节点的没有弟弟的子节点
                break
        self.Scheduler()

    def store(self):
        for i in range(20):
            self.pcb[i].pid = " "
            self.pcb[i].type = "ready"
            self.pcb[i].parent = -1
            self.pcb[i].children = -1
            self.pcb[i].elder = -1
            self.pcb[i].younger = -1
            self.pcb[i].priority = -1
            for j in range(4):
                self.pcb[i].Other_Resource[j].rid = -1
                self.pcb[i].Other_Resource[j].used = 0
                self.pcb[i].Other_Resource[j].waiting_request = 0
        self.running_process = 0
        for i in range(4):
            self.rcb[i].initial = i + 1
            self.rcb[i].remain = i + 1
            while len(self.rcb[i].waiting_list) != 0:
                del self.rcb[i].waiting_list[0]
        for i in range(3):
            while len(self.rl[i]) != 0:
                self.rl[i].pop()

    def Resource_Listing(self):
        print('\n\n' + '=' * 71)
        print(' ' * 30 + "Resource_List")
        print('=' * 71)
        print('Initial\t\t\tRemain\t\t\tWait\t\t\tList')

        Input_Dict = {}
        for i in range(20):
            Input_Dict[i] = self.pcb[i].pid
        for i in range(4):
            print(self.rcb[i].rid + ':', end="\t\t\t\t")
            print(self.rcb[i].initial, end="\t\t\t\t")
            print(self.rcb[i].remain, end="\t\t\t\t")
            if len(self.rcb[i].waiting_list) != 0:
                for process in self.rcb[i].waiting_list:
                    print(Input_Dict[process], end=';')
            else:
                print('None Process is Waiting', end='')
            print()
        print('=' * 71 + "\n\n")

    def Process_Listing(self):
        print('\n\n' + '=' * 47)
        print(' ' * 15 + "Process_List")
        print('=' * 47)
        print('PID\t\t\t\tStatus\t\t\t\tPriority')
        for i in range(20):
            if self.pcb[i].pid != ' ':
                if self.pcb[i].pid == 'init':
                    print(self.pcb[i].pid, end="\t\t\t")
                else:
                    print(self.pcb[i].pid, end="\t\t\t\t")
                print(self.pcb[i].type, end="\t\t\t\t")
                print(self.pcb[i].priority, end="\n")
        print('=' * 47 + '\n\n')

    def Process_Info(self, pidList):

        print('\n\n' + '=' * 73)
        print(' ' * 26 + "Process_Information")
        print('=' * 73)
        print('PID\t\tStatus\t\tPriority\tParent\t\tChild\t\tElder\t\tYoung')

        Input_Dict = {}
        for i in range(20):
            Input_Dict[i] = self.pcb[i].pid

        for i in range(20):
            if Input_Dict[i] == ' ':
                continue
            if self.pcb[i].pid == "init":
                print(self.pcb[i].pid, end="\t")
            else:
                print(self.pcb[i].pid, end="\t\t")
            print(self.pcb[i].type, end="\t\t")
            print(self.pcb[i].priority, end="\t\t\t")
            if self.pcb[i].parent != -1:
                output = Input_Dict[self.pcb[i].parent]
            else:
                output = 'None'
            print_output(output)

            if self.pcb[i].child != -1:
                output = Input_Dict[self.pcb[i].child]

            else:
                output = 'None'
            print_output(output)

            if self.pcb[i].elder != -1:
                output = Input_Dict[self.pcb[i].elder]
            else:
                output = 'None'
            print_output(output)

            if self.pcb[i].younger != -1:
                output = Input_Dict[self.pcb[i].younger]
            else:
                output = 'None'
            print_output(output)

            print()
        print('=' * 73 + '\n\n')
