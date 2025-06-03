from core.logger import logger
from core.config import settings

from openai import AzureOpenAI

client = AzureOpenAI(
    api_version=settings.AZURE_OPENAI_API_VERSION,
    azure_endpoint=settings.AZURE_OPENAI_ENDPOINT,
    api_key=settings.AZURE_OPENAI_KEY
)

model = "gpt-4o-mini"

def get_azure_openai_response(message):
    """
    Get a response from Azure OpenAI.

    Args:
        message: message to send to the model.

    Returns:
        The response from the model.
    """
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[{
                "role": "user",
                "content": message,
            }],
            max_tokens=10000,
            temperature=0.7,
        )
        return response.choices[0].message.content
    except Exception as e:
        logger.error(f"Failed to get Azure OpenAI response: {e}")
        return None