# TCP Finite State Machine simulator
A simple TCP FSM implemented in Python.

## Dependencies
* `transitions` library: install using `pip install transitions`

## Quick Start
The FSM simulator can be started in user-facing REPL mode, or can be run at the command line by passing a file of commands.

To start the REPL: simply run the `tcp_fsm_simulator.py` file with no arguments.

To process a command file: run `tcp_fsm_simulator.py command_file_name`

Additional arguments beyond the first will be ignored.

## Commands
The following commands are valid for the FSM, depending on state:
* `PASSIVE`: performs a passive open
* `ACTIVE`: performs an active open
* `SYN`: sends SYN
* `SYNACK`: sends SYNACK
* `ACK`: sends ACK
* `RDATA`: simulates a data receive operation
* `SDATA`: simulats a data send operation
* `FIN`: sends FIN
* `CLOSE`: sends CLOSE
* `TIMEOUT`: simulates timeout

In addition, the user may pass the special command `QUIT` to exit the REPL.

## Notes
Faulty commands not in the list above, and commands which are in the list above but invalid for the current TCP connection state, will be ignored with a warning to the user.

**N.B. If a set of commands closes a simulated TCP session without exiting this program, the tracked count of data receives and sends will be reset (simulating a new connection).**
