from azure.ai.vision.imageanalysis import ImageAnalysisClient
from azure.ai.vision.imageanalysis.models import VisualFeatures
from azure.core.credentials import AzureKeyCredential
from core.config import settings


client = ImageAnalysisClient(
    endpoint=settings.VISION_ENDPOINT,
    credential=AzureKeyCredential(settings.VISION_KEY)
)

def get_image_analysis(image_url: str) -> dict:
    # Get a caption for the image. This will be a synchronously (blocking) call.
    result = client.analyze_from_url(
        image_url=image_url,
        visual_features=[VisualFeatures.CAPTION, VisualFeatures.READ],
        gender_neutral_caption=True,  # Optional (default is False)
    )

    return {
        "caption": result.caption.text if result.caption is not None else None,
        "read": [
            {
                "line": line.text
            }
            for block in result.read.blocks
            for line in block.lines
        ]
    }