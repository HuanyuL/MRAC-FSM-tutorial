class FSM:
    def __init__(self):
        self.state = "start"

    def transition(self, event):
        if self.state == "start" and event == "game_start":
            self.state = "challenge1"
        elif self.state == "challenge1" and event == "hand_over_bubble":
            self.state = "win"
        elif self.state == "challenge1" and event == "fail":
            self.state = "retry"
        elif self.state == "retry" and event == "retry_challenge1":
            self.state = "challenge1"
        elif event == "reset":
            self.state = "start"

    def get_state(self):
        return self.state
