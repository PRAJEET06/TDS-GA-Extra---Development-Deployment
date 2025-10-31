from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# 1. Define Pydantic Models for Input Validation
# This model ensures the JSON input has a nested "url" string
class AttachmentURL(BaseModel):
    url: str

# This model ensures the main JSON object has an "attachments" key
# which contains an object matching the AttachmentURL model
class FileRequest(BaseModel):
    attachments: AttachmentURL

# 2. Create the FastAPI app instance
app = FastAPI()

# 3. Define the POST endpoint at /file
@app.post("/file")
async def detect_mime_type(request: FileRequest):
    # Access the URL from the validated request object
    data_uri = request.attachments.url
    
    # 4. The Core Logic: Parse the Data URI
    try:
        # A data URI looks like: "data:<mime_type>;base64,<data>"
        
        # Check if it's a data URI
        if not data_uri.startswith("data:"):
            raise ValueError("Not a valid data URI")

        # Get the header part (e.g., "data:image/png;base64")
        header = data_uri.split(',')[0]
        
        # Get the mime part (e.g., "image/png;base64")
        mime_part = header.split(':')[1]
        
        # Get the actual mime type (e.g., "image/png")
        mime_type = mime_part.split(';')[0]
        
        # Get the main type (e.g., "image")
        main_type = mime_type.split('/')[0]
        
        # 5. Classify the main type based on requirements
        supported_types = ["image", "text", "application"]
        if main_type in supported_types:
            return {"type": main_type}
        else:
            # For other valid types like "audio", "video", etc.
            return {"type": "unknown"}
    
    except (IndexError, AttributeError, ValueError):
        # This catches any errors during splitting if the format is wrong
        return {"type": "unknown"}