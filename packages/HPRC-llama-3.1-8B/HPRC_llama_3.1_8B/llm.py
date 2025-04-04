from typing import Any, List, Optional

from langchain_core.callbacks.manager import CallbackManagerForLLMRun
from langchain_core.language_models.llms import LLM
import requests

class TestLLM(LLM):
    model_id: str

    @property
    def _llm_type(self) -> str:
        return "custom"

    def _call(
        self,
        prompt: str,
        stop: Optional[List[str]] = None,
        run_manager: Optional[CallbackManagerForLLMRun] = None,
        **kwargs: Any,
    ) -> str:
        def send_question(prompt):
            url = "http://10.72.10.12:5000/infer"
            headers = {"Content-Type": "application/json"}
            data = {
                "input": prompt,
                "length": 512
            }
            response = requests.post(url, headers=headers, json=data)
            return response.json()["response"]
        return send_question(prompt)
