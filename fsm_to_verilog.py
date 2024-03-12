import json


def encode_onehot(list):
    '''
    gets a list and returns a dictionary of the items
    and their respective onehot encodings
    '''
    dictionary = {}
    for i,s in enumerate(list):
        dictionary[s] = f"{len(list)}\'b{'0'*i}1{'0'*(len(list)-i-1)}"
    return dictionary


def module_definition(inputs, n_outputs, n_states):
    '''
    constructs the beginning parts of the verilog code using
    the names of the inputs and the number of states and outputs.
    each input/output gets a separate wire, and the state and its shadow
    are stored as internal variables
    '''
    input_wires = "" 
    for i in inputs:
        input_wires += f", input wire {i}"
    module_def = f"module fsm(input wire clk, input wire rst{input_wires}, output reg [{n_outputs-1}:0] out);\nreg [{n_states-1}:0] s, ns;\nreg [{n_outputs-1}:0] nout;\n\n"
    return module_def


def combinational_logic(states, onehot_states, transitions, onehot_outputs):
    '''
    constructs the combinational logic of the module using
    the states, the encodings, and the transitions. each state gets a 
    case statement and in each case statement there are several if statements
    coresponding to the transitions out of that state 
    '''
    clogic = f"always@(*) begin\nns={onehot_states[states[0]]};\nnout=out;\ncase(s)\n"
    for state in states:
        one_case = f"{onehot_states[state]}: begin\nns={onehot_states[state]};\n"
        for transition in transitions[state]:
            one_transition = f'if({transition["on"]}) begin\nns={onehot_states[transition["dst"]]};\nnout={onehot_outputs[transition["out"]]};\nend\n'
            one_case += one_transition
        clogic += one_case + "end\n"
    clogic += "endcase\nend\n\n"
    return clogic



def sequential_logic(states, onehot_states, n_outputs):
    '''
    constructs the sequential logic of the module using the states,
    the encodings and the number of outputs
    sets the value of s and out with respect to rst and their shadow values
    '''
    slogic = f"always@(posedge clk) begin\nif(rst) begin\ns<={onehot_states[states[0]]};\nout<={n_outputs}\'b{'0'*n_outputs};\nend\nelse begin\ns<=ns;\nout<=nout;\nend\nend\n\n"
    return slogic


def main():
    with open('fsm.json') as file:
        fsm = json.load(file)
    output_file = open('output.sv', 'w')
    output_file.write(module_definition(fsm["inputs"], len(fsm["outputs"]), len(fsm["states"])))
    onehot_states = encode_onehot(fsm["states"])
    onehot_outputs = encode_onehot(fsm["outputs"])
    output_file.write(combinational_logic(fsm["states"], onehot_states, fsm["transitions"], onehot_outputs))
    output_file.write(sequential_logic(fsm["states"], onehot_states, len(fsm["outputs"])))
    output_file.write("endmodule")
    output_file.close()
    print("the output encodings are:")
    print(onehot_outputs)


if __name__=="__main__":
    main()