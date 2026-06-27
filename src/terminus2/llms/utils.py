from model_library.base import LLM


async def get_model_context_limit(llm: LLM) -> int:
    """
    Using the model registry, we fetch the context window for the given model.
    NOTE: Do not override this information. Instead update the model library if its missing.
    """

    await llm.ensure_metadata_loaded()
    context_window = llm.input_context_window
    assert context_window is not None, "no context window found for " + llm.model_name
    return context_window
