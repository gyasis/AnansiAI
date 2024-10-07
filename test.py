import logging
from agent_system.agents.overseer_agent import OverseerAgent
from agent_system.models.model_pool import ModelPool
from agent_system.utils.message_pool import MessagePool

# Mock Agent class for testing
class MockAgent:
    def __init__(self, agent_id, description):
        self.id = agent_id
        self.description = description

def test_nominate():
    logging.basicConfig(level=logging.INFO)
    
    # Setup
    available_agents = []
    message_pool = MessagePool()
    model_pool = ModelPool()
    model_pool.add_model("default", "chatgpt", "gpt-4o-mini")
    
    overseer = OverseerAgent("I manage the agents.", available_agents, message_pool, model_pool)
    
    # Create mock agents
    mock_agent1 = MockAgent(1, "Task Agent 1")
    mock_agent2 = MockAgent(2, "Task Agent 2")
    
    # Add mock agents to available agents
    available_agents.append(mock_agent1)
    available_agents.append(mock_agent2)
    
    # Simulate response and options
    response = "I need help with a task."
    
    # Call nominate
    try:
        overseer.nominate(available_agents, response)
    except Exception as e:
        logging.error(f"Test failed: {str(e)}")

if __name__ == "__main__":
    test_nominate()