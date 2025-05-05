from typing import Any, List, Optional

from langchain_core.callbacks.manager import CallbackManagerForLLMRun
from langchain_core.language_models.llms import LLM
import os
import requests
import subprocess
import pickle

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
            cluster=str(subprocess.run(['/sw/local/bin/clustername'], stdout=subprocess.PIPE).stdout.decode('utf-8').lower()).strip()
            if(cluster == "aces"):
                with open("/sw/hprc/sw/dor-hprc-venv-manager/codeai/ip.pkl", "rb") as my_file:
                    ip = pickle.load(my_file)
                    url = f"http://{ip}:5000/infer"
            headers = {"Content-Type": "application/json"}
            data = {
                "input": prompt,
                "length": 512,
                "model": "llama_8B"
            }
            print("sending to url: ", url)
            response = requests.post(url, headers=headers, json=data)
            return response.json()["response"]
        return send_question(prompt)
