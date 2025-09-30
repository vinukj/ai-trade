import config
from openai import OpenAI  # noqa: E0401  # type: ignore
import logging
import time


def call_llm(prompt: str) -> str:
    """
    Call Azure OpenAI (Grok) deployment with retries and return the response content.
    """
    logger = logging.getLogger(__name__)
    for attempt in range(3):
        try:
            client = OpenAI(
                base_url=config.AZURE_OPENAI_ENDPOINT,
                api_key=config.AZURE_OPENAI_API_KEY,
            )
            response = client.chat.completions.create(
                model=config.AZURE_OPENAI_DEPLOYMENT,
                messages=[{"role": "user", "content": prompt}],
            )
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"LLM request failed on attempt {attempt+1}: %s", e)
            if attempt < 2:
                time.sleep(2 ** attempt)
            else:
                raise
