# fill(state, max, which) — return a copy of state which fills the jug corresponding to the index in which (0 or 1)
# to its maximum capa
def fill(state, max, which):
    state1 = state
    if which == 0:
        state1[0] = max[0]
    elif which == 1:
        state1[1] = max[1]

    return state1


# empty(state, max, which) — return a copy of state which empties the jug corresponding to the index in which (0 or 1).

def empty(state, max, which):
    state1 = state
    if which == 0:
        state1[0] = 0
    elif which == 1:
        state1[1] = 0

    return state1


# xfer(state, max, source, dest) — return a copy of state which pours the contents of the jug at
# index source into the jug at index dest, until source is empty or dest is full.
def xfer(state, max, source, dest):
    state1 = state
    if source == 0 and dest == 1:
        while state1[0] != 0 and state1[1] != max[1]:
            state1[0] = state1[0] - 1
            state1[1] = state1[1] + 1

    elif source == 1 and dest == 0:
        while state1[1] != 0 and state1[0] != max[0]:
            state1[1] = state1[1] - 1
            state1[0] = state1[0] + 1

    return state1


# succ(state, max) — display the list of unique successor states of the current state in any order.

def succ(state, max):
    successor = []
    successor.append([state[0], state[1]])
    if state != [state[0], 0]:
        successor.append([state[0], 0])
    if state != [max[0], state[1]] and [max[0], state[1]] not in successor:
        successor.append([max[0], state[1]])
    if state != [0, state[1]] and [0, state[1]] not in successor:
        successor.append([0, state[1]])
    if state != [state[0], max[1]] and [state[0], max[1]] not in successor:
        successor.append([state[0], max[1]])
    if state != xfer(state, max, 1, 0) and xfer(state, max, 1, 0) not in successor:
        successor.append(xfer(state, max, 1, 0))
    if state != xfer(state, max, 0, 1) and xfer(state, max, 0, 1) not in successor:
        successor.append(xfer(state, max, 0, 1))
    return successor
