from langgraph.graph import StateGraph, END

class RagWorkflow:
    def __init__(self, retrieve_node, answer_node):
        self.retrieve_node = retrieve_node
        self.answer_node = answer_node

        workflow = StateGraph(dict)
        workflow.add_node("retrieve", self.retrieve_node.run)
        workflow.add_node("answer", self.answer_node.run)
        workflow.set_entry_point("retrieve")
        workflow.add_edge("retrieve", "answer")
        workflow.add_edge("answer", END)
        self.chain = workflow.compile()
    
    def run(self, question):
        return self.chain.invoke({"question": question})