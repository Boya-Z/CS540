import random


# this function expects two boolean parameter (whether you switch envelopes or not, and whether you want to see the
# printed explanation of the simulation) and returns True or False based on whether you selected the correct envelope
def pick_envelope(switch, verbose):
    ball = ['b', 'b', 'b', 'r']
    env0 = []
    env1 = []
    contain = -1
    # Randomly distribute the three black/one red balls into two envelopes
    while (len(ball) > 0):
        ballNumber = random.randrange(len(ball))
        if (len(ball) > 2):
            env0.append(ball.pop(ballNumber))
        else:
            env1.append(ball.pop(ballNumber))

    if verbose:
        print("Envelope 0: " + env0[0] + " " + env0[1])
        print("Envelope 1: " + env1[0] + " " + env1[1])
    # Randomly select one envelope
    picked = random.randint(0, 1)
    if verbose:
        print("I picked envelope " + str(picked))
    # Randomly select a ball from the envelope
    if picked == 0:
        drew = random.randrange(len(env0))
        result = env0[drew]
        if 'r' in env0:
            contain = 0
    elif picked == 1:
        drew = random.randrange(len(env1))
        result = env1[drew]
        if 'r' in env1:
            contain = 1
    if verbose:
        print("and drew a " + result)
    if result == 'r':
        return True
    if switch == True:
        picked1 = 1 - picked
        if verbose:
            print("Switch to envelope " + str(picked1))
        if picked1 == 0:
            if 'r' in env0:
                return True
        elif picked1 == 1:
            if 'r' in env1:
                return True
        else:
            return False
    elif contain == picked:
        return True
    return False


# this function runs n simulations of envelope picking under both strategies (switch n times, don't switch n times)
# and prints the percent of times the correct envelope was chosen for each
def run_simulation(n):
    # After n simulations:
    print("After " + str(n) + " simulations:")
    switch = 0
    no_switch = 0
    for i in range(n):
        result = pick_envelope(True, verbose=False)
        if result == True:
            switch = switch + 1

    for i in range(n):
        result = pick_envelope(False, verbose=False)
        if result == True:
            no_switch = no_switch + 1

    print("  Switch successful: " + str(switch / n * 100) + "%")
    print("  No-switch successful: " + str(no_switch / n * 100) + "%")
