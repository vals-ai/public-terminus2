from pathlib import Path
from typing import Any, override

from valkyrie.contract import BaseAgentContract

_LOGS_DIR = Path("/logs/terminus2")


class Terminus2Contract(BaseAgentContract):
    """Terminus 2 Agent Contract"""

    @property
    def name(self) -> str:
        return "terminus_2"

    @property
    def install_cmd(self) -> str:
        return "bash setup.sh"

    @property
    def secrets(self) -> dict[str, str]:
        model_keys = [
            "OPENAI_API_KEY",
            "GOOGLE_API_KEY",
            "COHERE_API_KEY",
            "ANTHROPIC_API_KEY",
            "MISTRAL_API_KEY",
            "XAI_API_KEY",
            "AI21LABS_API_KEY",
            "FIREWORKS_API_KEY",
            "DEEPSEEK_KEY",
            "AZURE_API_KEY",
            "DASHSCOPE_API_KEY",
            "PERPLEXITY_KEY",
            "ZAI_API_KEY",
            "KIMI_API_KEY",
            "MERCURY_KEY",
            "MINIMAX_API_KEY",
            "DEEPSEEK_API_KEY",
            "ARCEE_API_KEY",
            "META_API_KEY",
            "POOLSIDE_API_KEY",
        ]
        return {
            **{key: "prodBenchmarksInfraApiKeys" for key in model_keys},
            "MODEL_PROXY_SSH_KEY": "model_proxy_ssh",
        }

    @property
    def final_output(self) -> Path | None:
        return _LOGS_DIR

    @property
    def ingest_lambda(self) -> str | None:
        return "analysis-terminus2"

    @override
    def run_cmd(self, problem_statement_path: str, task_id: str, kwargs: dict[str, Any]) -> str:
        model = self._agent_config.model
        if not model:
            raise ValueError("Model is required. Use --model to specify one.")

        parts = [
            "terminus2 run",
            f"--problem-path {problem_statement_path}",
            f"-m {model}",
            f"--logs-dir {_LOGS_DIR}",
        ]

        temperature = kwargs.get("temperature")
        if temperature:
            parts.append(f"--temperature {temperature}")

        max_turns = kwargs.get("max_turns")
        if max_turns:
            parts.append(f"--max-turns {max_turns}")

        parser = kwargs.get("parser")
        if parser:
            parts.append(f"--parser {parser}")

        reasoning = kwargs.get("reasoning")
        if reasoning is not None:
            parts.append("--reasoning" if str(reasoning).lower() == "true" else "--no-reasoning")

        reasoning_effort = kwargs.get("reasoning_effort")
        if reasoning_effort:
            parts.append(f"--reasoning-effort {reasoning_effort}")

        return " ".join(parts)


contract = Terminus2Contract
