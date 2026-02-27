def simple_answer(state):
    ctx = state["context"]
    if ctx:
        answer = f"I found this: '{ctx[0][:100]}...'"
    else:
        answer = "Sorry, I don't know."
    state["answer"] = answer
    return state