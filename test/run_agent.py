from core.example_agent import ExampleAgent1

from agent_framework.devui import serve

agent = ExampleAgent1()

# Launch debug UI - that's it!
serve(entities=[agent._agent], auto_open=True)
# → Opens browser to http://localhost:8080
