import os
import asyncio
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from pydantic import BaseModel  # <--- ADD THIS LINE RIGHT HERE
from dotenv import load_dotenv
import httpx


# Load variables from the .env file automatically
load_dotenv()

app = FastAPI(title="Open-Eye Spatial VLA Engine")

# This securely grabs the key you just generated
API_KEY = os.getenv("GROQ_API_KEY")
INFERENCE_URL = "https://groq.com"


class SpatialResponse(BaseModel):
    object_detected: str
    spatial_coordinate_xyz: list[float]
    action_instruction: str

@app.get("/")
async def root():
    return {"status": "Open-Eye Protocol Active"}

@app.websocket("/v1/spatial-stream")
async def spatial_stream(websocket: WebSocket):
    await websocket.accept()
    print("🚀 Hardware device connected to Open-Eye Stream")
    
    try:
        while True:
            # Receive raw image data/bytes from the smart glasses or camera
            frame_bytes = await websocket.receive_bytes()
            
            # Fire-and-forget processing loop to maintain 60fps throughput
            asyncio.create_task(process_frame_and_respond(websocket, frame_bytes))
            
    except WebSocketDisconnect:
        print("🛑 Hardware device disconnected safely")

async def process_frame_and_respond(websocket: WebSocket, frame_bytes: bytes):
    """
    Sends frame bytes to the high-speed vision model and returns 
    spatial action vectors back to the hardware device.
    """
    # In production, you convert frame_bytes to base64 and send to Llama-3-Vision
    # For tonight's test, we simulate an ultra-low latency spatial calculation
    try:
        spatial_data = {
            "object_detected": "Mechanical Component A",
            "spatial_coordinate_xyz": [0.45, -1.2, 0.88],
            "action_instruction": "ROTATE_COUNTER_CLOCKWISE_10MM"
        }
        
        # Stream the spatial coordination vector back down the pipe instantly
        await websocket.send_json(spatial_data)
        
    except Exception as e:
        print(f"Error processing frame: {e}")
