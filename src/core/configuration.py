from azure.keyvault.secrets import SecretClient
from azure.identity import DefaultAzureCredential
from azure.identity import AzureCliCredential

class Configuration:
    def __init__(self):
        self._foundry_endpoint = "https://aif-lmg-ai-agents.cognitiveservices.azure.com"
        self._key_vault_name = "kv-lmg-ai-agents"
        self._deployment_name = "gpt-5-chat"
        self._api_key_secret_name = "foundry-api-key"
        self._api_key: str | None = None

    @property
    def foundry_endpoint(self) -> str:
        return self._foundry_endpoint
    
    @property
    def deployment_name(self) -> str:
        return self._deployment_name

    @property
    def key_vault_name(self) -> str:
        return self._key_vault_name
    
    @property
    def api_key_secret_name(self) -> str:
        return self._api_key_secret_name

    @property
    def api_key(self) -> str:
        if self._api_key is None:
            key_vault_client = SecretClient(
                vault_url=f"https://{self._key_vault_name}.vault.azure.net/",
                credential=AzureCliCredential()
            )
            self._api_key = key_vault_client.get_secret(self._api_key_secret_name).value
        return self._api_key
