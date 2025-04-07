from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from app.services.FloorplanService import FloorplanService
import shutil
import os
import uuid

# Initialize FastAPI app
app = FastAPI(
    title="Gurney Guide API", 
    description="API documentation",
    version="1.0",
    docs_url="/docs",  # Ensure Swagger UI is enabled
    redoc_url="/redoc"
    )

# Initialize Services
floorplan_service = FloorplanService()

# Allow CORS for frontend communication (adjust origins accordingly)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],  # Adjust for Angular frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Temporary storage for uploaded files
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.get("/")
def root():
    return {"message": "Welcome to the Gurney Guide API!"}


# 📌 **1. Upload and Process DXF File**
@app.post("/upload-dxf/")
async def upload_dxf(file: UploadFile = File(...)):
    """
    Uploads and processes a DXF file, storing its walls, rooms, and entrance in the database.
    """
    try:
        file_ext = file.filename.split(".")[-1]
        if file_ext.lower() != "dxf":
            raise HTTPException(status_code=400, detail="Only DXF files are allowed.")

        file_path = os.path.join(UPLOAD_DIR, f"{uuid.uuid4()}.dxf")

        # Save file temporarily
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Process file
        dxf_id = floorplan_service.parse_dxf(file_path)

        if not dxf_id:
            raise HTTPException(status_code=500, detail="Failed to process DXF file.")

        return {"message": "File uploaded successfully!", "dxf_id": dxf_id}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing DXF: {str(e)}")


# 📌 **2. Retrieve All Floorplans**
@app.get("/floorplans/")
def get_all_floorplans():
    """
    Fetches all stored DXF floorplans.
    """
    try:
        floorplans = floorplan_service.get_all_floorplans()
        return {"floorplans": floorplans}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# 📌 **3. Get a Specific Floorplan**
@app.get("/floorplan/{dxf_id}")
def get_floorplan(dxf_id: int):
    """
    Fetches a specific floorplan's details.
    """
    dxf_data = floorplan_service.get_floorplan_by_id(dxf_id)
    if not dxf_data:
        raise HTTPException(status_code=404, detail="DXF File not found.")
    return dxf_data


# 📌 **4. Find Path to a Room**
@app.get("/floorplan/{dxf_id}/path/{room_name}")
def get_path(dxf_id: int, room_name: str):
    """
    Finds and returns the shortest path from entrance to the specified room.
    """
    response = floorplan_service.find_path(dxf_id, room_name)
    if not response:
        raise HTTPException(status_code=404, detail=f"No path found to room {room_name}.")
    return response


# 📌 **5. Delete a Floorplan**
@app.delete("/floorplan/{dxf_id}")
def delete_floorplan(dxf_id: int):
    """
    Deletes a DXF floorplan from the database.
    """
    success = floorplan_service.delete_floorplan(dxf_id)
    if not success:
        raise HTTPException(status_code=404, detail="DXF File not found.")
    return {"message": "Floorplan deleted successfully!"}


# Start the FastAPI application
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
