from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import shutil
import os
from pathlib import Path
from dotenv import load_dotenv
from converter import convert_musicxml_to_abc
from agent import create_clef_agent
from rag_indexer import get_index, add_document_to_index

# Load environment variables (override existing ones)
load_dotenv(override=True)

app = FastAPI(title="Clef.ai Backend")

# CORS setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all for dev
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = "data/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Initialize Agent and Index
# We initialize the index here to ensure it's ready
rag_index = get_index(data_dir="data/Catholic", persist_dir="data/chromadb")
agent_executor = create_clef_agent()

class ChatRequest(BaseModel):
    message: str

@app.get("/")
async def root():
    return {"message": "Clef.ai Backend is running with LangChain + LlamaIndex"}

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    try:
        file_path = os.path.join(UPLOAD_DIR, file.filename)
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
            
        # Process file if it's MusicXML
        if file.filename.endswith(".xml") or file.filename.endswith(".mxl"):
            # Convert to ABC (Optional now, but good for display/legacy)
            abc_content = convert_musicxml_to_abc(file_path)
            
            # Add to RAG Index using Custom Reader
            if rag_index:
                add_document_to_index(Path(file_path), rag_index)
            
            return {
                "filename": file.filename,
                "message": "File uploaded, converted, and indexed successfully",
                "abc_content": abc_content[:200] + "..." if abc_content else "Conversion failed"
            }
            
        return {"filename": file.filename, "message": "File uploaded successfully"}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/chat")
async def chat(request: ChatRequest):
    try:
        # Use LangChain Agent
        response = agent_executor.invoke({"input": request.message})
        
        return {
            "response": response["output"],
            "source": "LangChain Agent",
            # "steps": response["intermediate_steps"] # Optional: return steps if needed
        }
    except Exception as e:
        print(f"Error in chat: {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
