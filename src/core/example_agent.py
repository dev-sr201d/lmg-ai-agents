from agent_framework import ChatAgent, AgentThread
from agent_framework.azure import AzureOpenAIChatClient
from azure.identity import DefaultAzureCredential
import json
from pydantic import Field
from typing import Annotated

from core.configuration import Configuration

class ExampleAgent1():
    def __init__(self, configuration: Configuration):
        self._foundry_endpoint = configuration.foundry_endpoint
        self._deployment_name = configuration.deployment_name
        self._api_key = configuration.api_key

    def create_agent(self) -> ChatAgent:
        credential = DefaultAzureCredential() if self._api_key is None else None
        return AzureOpenAIChatClient(
            endpoint=self._foundry_endpoint,
            deployment_name=self._deployment_name,
            api_key=self._api_key,
            credential=credential
        ).create_agent(
            instructions="""
            You are an assistant ...
            """,
            name="OKR Creation Assistant",
            tools=[self._tool_one]
        )
    
    async def get_agent_thread(self, serialized_thread: str | None) -> AgentThread:
        if serialized_thread is None:
            return self._agent.get_new_thread()

        thread_data = json.loads(serialized_thread)
        return await AgentThread.deserialize(thread_data)

    async def serialize_agent_thread(self, thread: AgentThread) -> str:
        thread_data = await thread.serialize()
        return json.dumps(thread_data)

    def _tool_one(self,
        param1: Annotated[str, Field(description="Description of what param 1 does.")]
    ) -> str:
        """Description of what the tool does."""
        return "something"
