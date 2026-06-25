from model_library.base import LLM 
from model_library.register_models import ModelConfig
from model_library.registry_utils import get_registry_config


def get_model_context_limit(llm: LLM) -> int:
    """
    Using the model registry, we fetch the context window for the given model.
    NOTE: Do not override this information. Instead update the model library if its missing.
    """

    # fetches model config
    config: ModelConfig | None = get_registry_config(llm._registry_key)
    assert config is not None, "no model config found for " + llm.model_name

    # returns the context window
    return config.properties.context_window