from agent_framework import ChatAgent
from agent_framework.azure import AzureOpenAIChatClient
from azure.identity import InteractiveBrowserCredential
import dotenv
from os import getenv
from typing import Annotated
from pydantic import Field

class AgentFactory():
    def __init__(self):
        dotenv.load_dotenv()
        dotenv.load_dotenv("./.env.local")
        self._foundry_endpoint = self._require_env("FOUNDRY_ENDPOINT")
        self._deployment_name = self._require_env("DEPLOYMENT_NAME")
        self._tenant_id=self._require_env("AZURE_TENANT_ID")
        self._api_key: str | None = getenv("API_KEY")

    def create_agent(self) -> ChatAgent:
        credential = InteractiveBrowserCredential(tenant_id=self._tenant_id) if self._api_key is None else None
        return AzureOpenAIChatClient(
            endpoint=self._foundry_endpoint,
            deployment_name=self._deployment_name,
            api_key=self._api_key,
            credential=credential
        ).create_agent(
            instructions="""
            You are an AI assistant that helps people find information.
            """,
            name="Test Assistant",
            tools=[self._tool_one]
        )
    
    def _require_env(self, var_name: str) -> str:
        value = getenv(var_name)
        if value is None:
            raise ValueError(f"Environment variable {var_name} is required but not set.")
        return value

    def _tool_one(self,
        param1: Annotated[str, Field(description="Description of what param 1 does.")]
    ) -> str:
        """Description of what the tool does."""
        return "something"

# Further tool options see: https://github.com/microsoft/Agent-Framework-Samples/tree/main/04.Tools
