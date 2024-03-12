# FSM to Verilog
Small Python project that converts a mealy FSM description into synthesizable Verilog code. \
The created module will have an input wire for each input in the FSM and it is up to the user to make sure multiple inputs are not active simultaneously. \
Also, the output will be in one-hot form and the encoding will be shown after the Verilog code is created.
## FSM description
The description of your FSM should be in JSON format. The JSON file should include a list of inputs, outputs, and states, as well as a list of outgoing edges for each state.
For example, the description of the FSM drawn below would look like [this](https://github.com/NegarAskari/fsm-to-verilog/blob/main/fsm.json).
<p align="center" width="100%">
    <img src="https://github.com/NegarAskari/fsm-to-verilog/blob/main/fsm.png?raw=true"> 
</p>

## How to use
Write your FSM description in the "fsm.json" file and run "fsm_to_verilog.py". The output will be written to "output.sv" in the same directory.
