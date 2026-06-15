from langgraph.graph import StateGraph, END
from agents.triage_agent import TriageAgent
from agents.retrieval_agent import RetrievalAgent
from agents.action_reasoning_agent import ActionReasoningAgent
from agents.formatting_agent import FormattingAgent

class AgentState:
    def __init__(self, network_log=None, triage_output=None, retrieved_docs=None, final_plan=None):
        self.network_log = network_log
        self.triage_output = triage_output
        self.retrieved_docs = retrieved_docs
        self.final_plan = final_plan

def create_langgraph_workflow():
    workflow = StateGraph(AgentState)

    triage_agent = TriageAgent()
    retrieval_agent = RetrievalAgent()
    action_reasoning_agent = ActionReasoningAgent()
    formatting_agent = FormattingAgent()

    workflow.add_node("triage", lambda state: AgentState(triage_output=triage_agent.process_log(state.network_log), **state.__dict__))
    workflow.add_node("retrieve", lambda state: AgentState(retrieved_docs=retrieval_agent.retrieve_info(state.triage_output["issue_type"]), **state.__dict__))
    workflow.add_node("reason", lambda state: AgentState(final_plan=action_reasoning_agent.formulate_plan(state.triage_output, state.retrieved_docs), **state.__dict__))
    workflow.add_node("format", lambda state: AgentState(final_plan=formatting_agent.format_response(state.final_plan), **state.__dict__))

    workflow.set_entry_point("triage")
    workflow.add_edge("triage", "retrieve")
    workflow.add_edge("retrieve", "reason")
    workflow.add_edge("reason", "format")
    workflow.add_edge("format", END)

    return workflow.compile()

if __name__ == "__main__":
    # Example usage:
    # This will fail if the faiss_index is not built.
    # Run scripts/knowledge_base.py first.
    workflow = create_langgraph_workflow()
    initial_state = AgentState(network_log={"timestamp": "...", "device_id": "...", "error_code": "...", "description": "BGP flapping detected on interface Gi0/1"})
    result = workflow.invoke(initial_state)
    print("Workflow finished with result:")
    print(result.final_plan)
