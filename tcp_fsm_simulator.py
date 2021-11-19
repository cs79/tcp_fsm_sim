from transitions import Machine, MachineError
import sys

class TCP_FSM(object):
    # define TCP states
    states = [
        "CLOSED",
        "LISTEN",
        "SYN_RCVD",
        "SYN_SENT",
        "ESTABLISHED",
        "FIN_WAIT_1",
        "FIN_WAIT_2",
        "CLOSING",
        "TIME_WAIT",
        "CLOSE_WAIT",
        "LAST_ACK"
    ]

    # define valid commands
    commands = [
        "PASSIVE",
        "ACTIVE",
        "SYN",
        "SYNACK",
        "ACK",
        "RDATA",
        "SDATA",
        "FIN",
        "CLOSE",
        "TIMEOUT"
    ]

    # define state transitions
    transitions = [
        { "trigger": "PASSIVE",     "source": "CLOSED",         "dest": "LISTEN" },
        { "trigger": "ACTIVE",      "source": "CLOSED",         "dest": "SYN_SENT" },
        { "trigger": "CLOSE",       "source": "LISTEN",         "dest": "CLOSED" },
        { "trigger": "SYN",         "source": "LISTEN",         "dest": "SYN_RCVD" },
        { "trigger": "CLOSE",       "source": "SYN_SENT",       "dest": "CLOSED" },
        { "trigger": "SYN",         "source": "SYN_SENT",       "dest": "SYN_RCVD" },
        { "trigger": "SYNACK",      "source": "SYN_SENT",       "dest": "ESTABLISHED" },
        { "trigger": "ACK",         "source": "SYN_RCVD",       "dest": "ESTABLISHED" },
        { "trigger": "CLOSE",       "source": "SYN_RCVD",       "dest": "FIN_WAIT_1" },
        { "trigger": "ACK",         "source": "FIN_WAIT_1",     "dest": "FIN_WAIT_2" },
        { "trigger": "FIN",         "source": "FIN_WAIT_1",     "dest": "CLOSING" },
        { "trigger": "FIN",         "source": "FIN_WAIT_2",     "dest": "TIME_WAIT" },
        { "trigger": "ACK",         "source": "CLOSING",        "dest": "TIME_WAIT" },
        { "trigger": "TIMEOUT",     "source": "TIME_WAIT",      "dest": "CLOSED" },
        { "trigger": "RDATA",       "source": "ESTABLISHED",    "dest": "ESTABLISHED" },
        { "trigger": "SDATA",       "source": "ESTABLISHED",    "dest": "ESTABLISHED" },
        { "trigger": "CLOSE",       "source": "ESTABLISHED",    "dest": "FIN_WAIT_1" },
        { "trigger": "FIN",         "source": "ESTABLISHED",    "dest": "CLOSE_WAIT" },
        { "trigger": "CLOSE",       "source": "CLOSE_WAIT",     "dest": "LAST_ACK" },
        { "trigger": "ACK",         "source": "LAST_ACK",       "dest": "CLOSED" }
    ]

    # initializer for TCP FSM
    def __init__(self, name, state):
        # set passed variables
        self.name = name
        if (state in TCP_FSM.states):
            self.state = state
        else:
            raise "Invalid state"
        # initialize the Machine
        self.machine = Machine(model=self,
                               states=TCP_FSM.states,
                               transitions=TCP_FSM.transitions,
                               initial="CLOSED",
                               auto_transitions=False)

# global program variables
input_data = None
rdata_count = 0
sdata_count = 0

# main function - either process passed input file, or start user command REPL
def main():
    # utilize the class defined above to implement the simulation
    fsm = TCP_FSM("sim", "CLOSED")

    # define inner helper function to process commands either from input file or user
    def proc_cmd(cmd):
        if cmd == "PASSIVE":
            try:
                fsm.PASSIVE()
                print("Event {} received, current State is {}".format(cmd, fsm.state))
            except MachineError as e:
                print(e)
        elif cmd == "ACTIVE":
            try:
                fsm.ACTIVE()
                print("Event {} received, current State is {}".format(cmd, fsm.state))
            except MachineError as e:
                print(e)
        elif cmd == "SYN":
            try:
                fsm.SYN()
                print("Event {} received, current State is {}".format(cmd, fsm.state))
            except MachineError as e:
                print(e)
        elif cmd == "SYNACK":
            try:
                fsm.SYNACK()
                print("Event {} received, current State is {}".format(cmd, fsm.state))
            except MachineError as e:
                print(e)
        elif cmd == "ACK":
            try:
                fsm.ACK()
                print("Event {} received, current State is {}".format(cmd, fsm.state))
            except MachineError as e:
                print(e)
        elif cmd == "RDATA":
            try:
                fsm.RDATA()
                global rdata_count
                rdata_count += 1
                print("DATA received {}".format(rdata_count))
            except MachineError as e:
                print(e)
        elif cmd == "SDATA":
            try:
                fsm.SDATA()
                global sdata_count
                sdata_count += 1
                print("DATA sent {}".format(sdata_count))
            except MachineError as e:
                print(e)
        elif cmd == "FIN":
            try:
                fsm.FIN()
                print("Event {} received, current State is {}".format(cmd, fsm.state))
            except MachineError as e:
                print(e)
        elif cmd == "CLOSE":
            try:
                fsm.CLOSE()
                # should we be resetting SDATA / RDATA counters here ?
                print("Event {} received, current State is {}".format(cmd, fsm.state))
            except MachineError as e:
                print(e)
        elif cmd == "TIMEOUT":
            try:
                fsm.TIMEOUT()
                print("Event {} received, current State is {}".format(cmd, fsm.state))
            except MachineError as e:
                print(e)
        elif cmd == "QUIT":
            print("QUIT command received - exiting")
            exit(0)
        else:
            print("Error: Unexpected Event: {}".format(cmd))

    # check if we got command line arguments
    if (len(sys.argv) > 1):
        input_file = sys.argv[1]
        # check to make sure we can open the data file, etc.
        try:
            with open(input_file, "r") as f:
                for line in f:
                    proc_cmd(line.rstrip())
                else:
                    print("Reached end of input file - exiting")
        # throw error if bad
        except:
            print("Bad input file! Enter a file of TCP commands, or use no args to start user REPL")
            exit(1)

    else:
        # start user-command REPL session
        print("Initiliazed TCP FSM - current State is {}".format(fsm.state))
        while True:
            command = input("Enter FSM command (or QUIT to exit): ")
            proc_cmd(command)

if __name__ == "__main__":
    main()
