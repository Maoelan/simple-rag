class AnswerNode:
    def __init__(self) :
        pass
    
    def run(self, state):
        ctx = state["context"]
        if ctx:
            answer = f"I found this : '{ctx[0][:100]}...'"
        else:
            answer = "Sorry, I don't know."
        state["answer"] = answer
        return state