"""Small wrapper over the Anthropic Messages API."""

from __future__ import annotations

import anthropic


class LLMClient:
    def __init__(self, api_key: str, model: str = "claude-opus-5") -> None:
        # An empty api_key lets the SDK fall back to ANTHROPIC_API_KEY / a profile.
        self._client = anthropic.Anthropic(api_key=api_key or None)
        self.model = model

    def complete(self, system: str, prompt: str, max_tokens: int = 16000) -> str:
        response = self._client.messages.create(
            model=self.model,
            max_tokens=max_tokens,
            thinking={"type": "adaptive"},
            system=system,
            messages=[{"role": "user", "content": prompt}],
        )
        return "".join(b.text for b in response.content if b.type == "text")
