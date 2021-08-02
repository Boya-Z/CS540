import copy
import random


# given a state of the board, return a list of all valid successor states
def succ(state, boulderX, boulderY):
    successor = list()
    size = len(state)
    m = 0
    while m < size:
        n = 0
        while n < size:
            if not (m == boulderX and n == boulderY):
                if get_succ(state, m, n) != state:
                    successor.append(get_succ(state, m, n))
            n = n + 1
        m = m + 1
    return successor


def get_succ(state, col, row):
    new_state = copy.deepcopy(state)
    new_state[col] = row
    return new_state


# given a state of the board, return an integer score such that the goal state is the highest score
def f(state, boulderX, boulderY):
    size = len(state)
    score = size
    m = 0
    while m < size:
        # print(m, 'times')
        if issafe(state, m, state[m], boulderX, boulderY, size):
            score = score - 1
            # print(m)
        m = m + 1
    return score


# given the current state, use succ() to generate the successors and return the selected next state
def choose_next(curr, boulderX, boulderY):
    successor = succ(curr, boulderX, boulderY)
    successor.append(curr)
    f_list = []
    f_lowest = []
    for i in successor:
        d = {'state': i, 'f': f(i, boulderX, boulderY)}
        f_list.append(d)
    order_f = sorted(f_list, key=lambda i: (i['f']))
    # print(order_f, '\n')
    lowest = order_f[0].get('f')
    for j in order_f:
        if j.get('f') == lowest:
            f_lowest.append(j.get('state'))
    # print(f_lowest, '\n')
    if len(f_lowest) == 1:
        result = f_lowest[0]
    if len(f_lowest) > 1:
        reorder = sorted(f_lowest)
        result = reorder[0]
        # print(reorder, '\n')
    if result == curr:
        return None
    return result


# run the hill-climbing algorithm from a given initial state, return the convergence state
def nqueens(initial_state, boulderX, boulderY):
    cur_state = initial_state
    cur_f = f(cur_state, boulderX, boulderY)
    print(cur_state, ' - f=', cur_f,sep = '')
    while cur_state is not None and cur_f != 0:
        next_state = choose_next(cur_state, boulderX, boulderY)
        if next_state is None:
            return cur_state
        if cur_f == 0:
            return cur_state
        next_f = f(next_state, boulderX, boulderY)
        cur_state = next_state
        cur_f = next_f
        print(cur_state, ' - f=', cur_f,sep = '')
    return cur_state


# run the hill-climbing algorithm on an n*n board with random restarts
def nqueens_restart(n, k, boulderX, boulderY):
    generate = []
    cur_f = n
    try_times=0
    best_move = []
    best_solu = []
    for i in range(n):
        generate.append(random.randint(0, n))
    # n = random.randint(0, n)
    while try_times<k:
        # generate = [random.randrange(0, n, 1) for i in range(n)]
        #print(generate)
        while generate[boulderX] == boulderY:
            generate.clear()
            for i in range(n):
                generate.append(random.randint(0, n))
        solu = nqueens(generate, boulderX, boulderY)
        cur_f = f(solu, boulderX, boulderY)
        if cur_f != 0:
            d = {'solu': solu, 'f': cur_f}
            best_move.append(d)
            cur_f=n
        else:
            print('Best Solutions:')
            nqueens(solu, boulderX, boulderY)
            cur_f = 0
            break
        try_times=try_times+1
        generate.clear()
        for i in range(n):
            generate.append(random.randint(0, n))
    if cur_f!=0:
        order_by_f = sorted(best_move, key=lambda i: (i['f']))
        for n in best_move:
            if n.get('f')==order_by_f[0].get('f'):
                best_solu.append(n.get('solu'))
        final_solu=sorted(best_solu)
        print('Best Solutions:')
        for i in final_solu:
            nqueens(i, boulderX, boulderY)
    return



def issafe(state, col, row, boulderX, boulderY, size):
    new_state = state
    new_state[col] = row

    # check the boulder is in the target position of not
    # if boulderX == col and boulderY == row:
    #   return False

    # check the row
    count = 0
    pos = []
    for ele in new_state:
        if ele == new_state[col]:
            count = count + 1
            if len(pos) == 0:
                pos.append(new_state.index(ele))
            else:
                pos.append(new_state.index(ele, pos[-1] + 1))
    # print('count',count,'pos',pos)
    if count > 1 and new_state[col] != boulderY:
        return False
    if count == 2 and (not pos[0] < boulderX < pos[1]):
        return False
    if count > 2:
        # the position index of the examing queen
        # print('check')
        if not (pos.index(col) == 0 and pos[0] < boulderX < pos[1]) and not (
                pos[-2] < boulderX < pos[-1] and pos[-1] == col):
            return False

    # Check upper diagonal /
    b_difference = boulderX - boulderY
    difference = col - row
    # count num of queen in same upper diagonal
    diagonal1 = 0
    pos1 = []
    for i in range(size):
        if i - new_state[i] == difference:
            diagonal1 = diagonal1 + 1
            pos1.append(i)
    # print('dia1', diagonal1, b_difference, difference, pos1, col, row)
    if diagonal1 > 1 and b_difference != difference:
        return False
    if diagonal1 == 2 and not (pos1[0] < boulderX < pos1[1]):
        return False
    if diagonal1 > 2:
        # print('check')
        if not ((pos1.index(col) == 0 and pos1[0] < boulderX < pos1[1]) or (
                pos1[-2] < boulderX < pos1[-1] and pos1[-1] == col)):
            return False

    # Check lower diagonal \
    b_sum = boulderX + boulderY
    sum = col + row
    # count num of queen in same lower diagonal
    diagonal2 = 0
    pos2 = []
    for j in range(size):
        if j + new_state[j] == sum:
            diagonal2 = diagonal2 + 1
            pos2.append(j)
    if diagonal2 > 1 and sum != b_sum:
        return False
    elif diagonal2 == 2 and not (pos2[0] < boulderX < pos2[1]):
        return False
    elif diagonal2 > 2:
        if not (pos2.index(col) == 0 and pos2[0] < boulderX < pos2[1]) and not (
                pos2[-2] < boulderX < pos2[-1] and pos2[-1] == col):
            return False
    # print('pass')
    return True
