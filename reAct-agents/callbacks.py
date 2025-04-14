from typing import Any, Dict, List
from langchain.callbacks.base import BaseCallbackHandler
from langchain.schema import LLMResult


class AgentCallbackHandler(BaseCallbackHandler):
    def on_llm_start(self, serialized: Dict[str, Any], prompts: List[str], *, run_id, parent_run_id=None, tags=None, metadata=None, **kwargs: Any) -> Any:
        """Run when LLM starts running"""
        print(f"***Prompt to LLM was:***\n{prompts[0]}")
        print("***********")

    def on_llm_end(self, response: LLMResult, *, run_id, parent_run_id=None, **kwargs: Any) -> Any:
        """Run when LLM ends running"""
        print(f"***LLM Response:***\n{response.generations[0][0].text}")
        print("***********")
