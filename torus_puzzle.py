import copy


# print_succ(state) — given a state of the puzzle, represented as a single list of integers with a 0 in the empty space,
# print to the console all of the possible successor states
def print_succ(state):
    ordered = successor(state)
    for i in ordered:
        print(i, end=" ")
        # heuristic(i)
        print('h=', heuristic(i), sep='')


def successor(state):
    successor = []
    x = 0
    pos = state.index(x)
    if pos == 0 or pos == 3 or pos == 6:
        # horizontal
        successor.append(switch(state, pos, pos + 1))
        successor.append(switch(state, pos, pos + 2))
    elif pos == 1 or pos == 4 or pos == 7:
        # horizontal
        successor.append(switch(state, pos, pos - 1))
        successor.append(switch(state, pos, pos + 1))
    elif pos == 2 or pos == 5 or pos == 8:
        # horizontal
        successor.append(switch(state, pos, pos - 1))
        successor.append(switch(state, pos, pos - 2))
    if pos == 0 or pos == 1 or pos == 2:
        # vertical
        successor.append(switch(state, pos, pos + 3))
        successor.append(switch(state, pos, pos + 6))
    elif pos == 3 or pos == 4 or pos == 5:
        # vertical
        successor.append(switch(state, pos, pos - 3))
        successor.append(switch(state, pos, pos + 3))
    elif pos == 6 or pos == 7 or pos == 8:
        # vertical
        successor.append(switch(state, pos, pos - 3))
        successor.append(switch(state, pos, pos - 6))

    orderedlist = sorted(successor)
    return orderedlist


# solve(state) — given a state of the puzzle, perform the A* search algorithm and print the path from the current state
# to the goal state
def solve(state):
    d = {'state': state, 'h': heuristic(state), 'g': 0, 'parent': None, 'f': heuristic(state)}
    closed = []
    index = len(closed) - 1

    opened = PriorityQueue()
    opened.enqueue(d)
    if opened.is_empty():
        exit()
    closed.append(opened.pop())
    while closed[-1].get('state') != [1, 2, 3, 4, 5, 6, 7, 8, 0]:
        next_state = successor(closed[-1].get('state'))
        for i in next_state:
            dic = {}
            dic['state'] = i
            dic['h'] = heuristic(i)
            dic['g'] = closed[-1].get('g') + 1
            dic['parent'] = closed[-1]
            dic['f'] = dic.get('g') + dic.get('h')
            # check closed empty or not
            if not closed:
                for j in closed:
                    if j.get('state') != dic.get('state'):
                        opened.enqueue(dic)
                    if j.get('state') == dic.get('state'):
                        if j.get('g') > dic.get('g'):
                            closed.remove(j)
                            # j = dic
                            # last=len(closed)-1
                            # del closed[closed.index(j):last]
                            opened.requeue(dic)
            else:
                opened.enqueue(dic)
        if opened.is_empty():
            exit()
        closed.append(opened.pop())

    goal = closed[-1]
    sol = [closed[-1]]
    while goal['parent'] is not None:
        goal = goal['parent']
        sol.append(goal)
    sol=reversed(sol)
    for k in sol:
        print(k.get('state'), end=" ")
        print('h=', k.get('h'), sep='', end=" ")
        print('moves:', k.get('g'), sep='')
    print('Max queue length: ', opened.max_len)


# heuristic, we will use the count of tiles which are not in their goal spaces.
def heuristic(state):
    count = 0
    i = 0
    while i < len(state) - 1:
        if state[i] != i + 1:
            count += 1
        i += 1
    # print('h=', count, sep='')
    return count
    # result="h="+count
    # return result


def switch(state, scr, des):
    successor = copy.deepcopy(state)
    temp = successor[scr]
    temp1 = successor[des]
    successor[scr] = temp1
    successor[des] = temp
    return successor


''' author: hobbes
    source: cs540 canvas
    TODO: complete the enqueue method
'''


class PriorityQueue(object):
    def __init__(self):
        self.queue = []
        self.max_len = 0

    def __str__(self):
        return ' '.join([str(i) for i in self.queue])

    def is_empty(self):
        return len(self.queue) == 0

    def enqueue(self, state_dict):
        # raise a underflow exception if the priority queue is empty
        # if self.is_empty(self):
        #    raise Exception("Priority queue underflow")

        """ Items in the priority queue are dictionaries:
             -  'state': the current state of the puzzle
             -      'h': the heuristic value for this state, not in right pos
             - 'parent': a reference to the item containing the parent state
             -      'g': the number of moves to get from the initial state to
                         this state, the "cost" of this state
             -      'f': the total estimated cost of this state, g(n)+h(n)

            For example, an item in the queue might look like this:
             {'state':[1,2,3,4,5,6,7,8,0], 'parent':[1,2,3,4,5,6,7,0,8],
              'h':0, 'g':14, 'f':14}

            Please be careful to use these keys exactly so we can test your
            queue, and so that the pop() method will work correctly.

            TODO: complete this method to handle the case where a state is
                  already present in the priority queue
        """
        in_open = False
        # TODO: set in_open to True if the state is in the queue already
        # TODO: handle that case correctly
        for i in self.queue:
            if i.get('state') == state_dict.get('state'):
                in_open = True
                # only replace the original by the new one if the new one has lower g value
                if i.get('g') > state_dict.get('g'):
                    i = state_dict  # ？

        if not in_open:
            self.queue.append(state_dict)

        # track the maximum queue length
        if len(self.queue) > self.max_len:
            self.max_len = len(self.queue)

    def requeue(self, from_closed):
        """ Re-queue a dictionary from the closed list (see lecture slide 21)
        """
        self.queue.append(from_closed)

        # track the maximum queue length
        if len(self.queue) > self.max_len:
            self.max_len = len(self.queue)

    def pop(self):
        """ Remove and return the dictionary with the smallest f(n)=g(n)+h(n)
        """
        minf = 0
        for i in range(1, len(self.queue)):
            if self.queue[i]['f'] < self.queue[minf]['f']:
                minf = i
        state = self.queue[minf]
        del self.queue[minf]
        return state
