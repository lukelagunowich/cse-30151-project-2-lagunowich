import csv

# Degree of nondeterminism -> average number of configurations that come from an average configuration
    # 1 -> deterministic; >1 -> based on degree of nondeterminism

def readTM(file):
    with open(file, 'r') as f:
        transitions = []
        for i, line in enumerate(f):
            if i == 0:
                name = line.strip()
            elif i == 1:
                states = line.strip().split(',')
            elif i == 2:
                sigma = line.strip().split(',')
            elif i == 3:
                gamma = line.strip().split(',')
            elif i == 4:
                qstart = line.strip()
            elif i == 5:
                qaccept = line.strip()
            elif i == 6:
                qreject = line.strip()
            else:
                transitions.append(line.strip().split(','))
        return name, states, sigma, gamma, qstart, qaccept, qreject, transitions

def transition(inputs, deltas, qaccept):
    output = []
    for input in inputs:
        for delta in deltas:
            state = input[1]
            head = input[2][0]
            if state != 'qrej' and state == delta[0]:
                if head == delta[1]:
                    if delta[4] == 'R':
                        next = [input[0]+delta[3], delta[2], input[2][1:]]
                        if next[1] == qaccept:
                            next[1] = 'qacc'
                        if next[2] == '':
                            next[2] = '_'
                        output.append(next)
                    elif delta[4] == 'L':
                        if delta[3] == '_':
                            prev = ''
                        else:
                            prev = delta[3]
                        next = [input[0][:len(input[0])-1], delta[2], input[0][len(input[0])-1]+prev+input[2][1:]]
                        if next[1] == qaccept:
                            next[1] = 'qacc'
                        if next[2] == '':
                            next[2] = '_'
                        output.append(next)
                else:
                    next = [input[0]+head, 'qrej', input[2][1:]]
                    if next[2] == '':
                        next[2] = '_'
                    if next not in output:
                        output.append(next)
    return output

def recurse(current_depth, transitions, qaccept, step, terminate=15):
    if not current_depth or step > terminate:
        return []
    trace_at_depth = [current_depth]
    next_depth = transition(current_depth, transitions, qaccept)
    if any(state[1] == 'qacc' for state in current_depth) or all(state[1] == 'qrej' for state in current_depth):
        return trace_at_depth
    elif next_depth:
        trace_at_depth += recurse(next_depth, transitions, qaccept, step=step+1, terminate=15)
    return trace_at_depth

def traceTM(infile, input, terminate=15):
    name, states, sigma, gamma, qstart, qaccept, qreject, transitions = readTM(infile)
    start = ['', qstart, input]
    start_depth = [start]
    trace = recurse(start_depth, transitions, qaccept, step=0, terminate=terminate)
    final_states = [transition[1] for transition in trace[-1]]
    
    if 'qacc' not in final_states:
        accepted = False
    else:
        accepted = True

    if not accepted and any(state != 'qrej' and state != 'qacc' for state in final_states):
        decided = False
    else:
        decided = True
    
    total_transitions = sum([len(depth) for depth in trace[1:]])
    depth = len(trace) - 1

    non_leaves = 0
    for d in trace:
        for t in d:
            if t[1] != 'qrej' and t[1] != 'qacc':
                non_leaves += 1
    nondeterminism = round(total_transitions/non_leaves, 2)

    

    return name, input, total_transitions, depth, nondeterminism, accepted, decided, trace 


def output(outfile, inputs):
    f = open(outfile, 'w')
    f.write(f'Name: {inputs[0]}\n')
    f.write(f'Initial string: {inputs[1]}\n')
    f.write(f'Total transitions simulated: {inputs[2]}\n')
    f.write(f'Nondeterminism: {inputs[4]}\n')
    
    if inputs[5]:
        f.write(f'String accepted in {inputs[3]} transitions.\n')
        for line in inputs[7]:
            f.write(f'{line}\n')
    elif inputs[6]:
        f.write(f'String string rejected in {inputs[3]} transitions.\n')
        for line in inputs[7]:
            f.write(f'{line}\n')
    else:
        f.write(f'Execution stopped after {inputs[3]} transitions (max depth limit).\n')

    f.close()
    