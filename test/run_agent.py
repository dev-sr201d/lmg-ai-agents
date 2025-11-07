from core.configuration import Configuration
from core.example_agent import ExampleAgent1

from agent_framework.devui import serve

configuration = Configuration()
example_agent = ExampleAgent1(configuration=configuration)

# Launch debug UI - that's it!
serve(entities=[example_agent.create_agent()], auto_open=True)
# → Opens browser to http://localhost:8080
