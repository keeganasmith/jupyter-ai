from typing import Any, List, Optional

from langchain_core.callbacks.manager import CallbackManagerForLLMRun
from langchain_core.language_models.llms import LLM

import requests

class Llama_8B_LLM(LLM):
    model_id: str = "HPRC_llama_8B"

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
            url = "http://10.72.10.19:5000/infer"
            headers = {"Content-Type": "application/json"}
            data = {
                "input": prompt,
                "length": 512,
                "model": "llama_8B"
            }
            response = requests.post(url, headers=headers, json=data)
            return response.json()["response"]
        return send_question(prompt)
