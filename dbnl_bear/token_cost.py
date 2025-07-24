class TokenCostTracker:
    """Track token usage and estimated cost for OpenAI models."""

    # Estimated costs per 1K tokens for known models
    MODEL_PRICING = {
        "gpt-4-turbo": {"prompt": 0.01, "completion": 0.03},
        "gpt-4-turbo-mini": {"prompt": 0.01, "completion": 0.03},
        "gpt-4-turbo-mini-2024-07-18": {"prompt": 0.01, "completion": 0.03},
        "gpt-3.5-turbo": {"prompt": 0.0005, "completion": 0.0015},
    }

    def __init__(self, model: str):
        self.model = model
        self.prompt_tokens = 0
        self.completion_tokens = 0
        pricing = self.MODEL_PRICING.get(model, {"prompt": 0.0, "completion": 0.0})
        self.prompt_cost = pricing["prompt"]
        self.completion_cost = pricing["completion"]

    def count_tokens(self, text: str) -> int:
        """Rudimentary token counting by whitespace separation."""
        return len(text.split())

    def update_usage(self, prompt_tokens: int, completion_tokens: int) -> None:
        self.prompt_tokens += prompt_tokens
        self.completion_tokens += completion_tokens

    def get_usage_report(self) -> dict:
        total_tokens = self.prompt_tokens + self.completion_tokens
        estimated_cost = (
            (self.prompt_tokens / 1000) * self.prompt_cost +
            (self.completion_tokens / 1000) * self.completion_cost
        )
        return {
            "model": self.model,
            "prompt_tokens": self.prompt_tokens,
            "completion_tokens": self.completion_tokens,
            "total_tokens": total_tokens,
            "estimated_cost_usd": estimated_cost,
        }

