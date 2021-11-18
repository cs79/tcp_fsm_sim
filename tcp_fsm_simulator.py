from transitions import Machine

class TCP_FSM(object):
    # set defaults for counters
    sdata_count = 0
    rdata_count = 0

    # helper function(s)
    def incr_sdata(self): self.sdata_count += 1
    def incr_rdata(self): self.rdata_count += 1

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
        { "trigger": "RDATA",       "source": "ESTABLISHED",    "dest": "ESTABLISHED",  "before": "incr_rdata" },
        { "trigger": "SDATA",       "source": "ESTABLISHED",    "dest": "ESTABLISHED",  "before": "incr_sdata" },
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

# utilize the class defined above to implement the simulation
fsm = TCP_FSM("sim", "CLOSED")

# get user input, handle -> flag warning and continue, or perform state transition using transition method
# need some way to exit, I guess

# can do a def main() etc. etc. here probably
