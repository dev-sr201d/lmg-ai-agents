from core.agent_factory import AgentFactory

from agent_framework.devui import serve

agent_factory = AgentFactory()

# Launch debug UI - that's it!
serve(entities=[agent_factory.create_agent()], auto_open=True)
# → Opens browser to http://localhost:8080
