# from fastapi import APIRouter, UploadFile, File, HTTPException
# from backend.app.services.FloorplanService import FloorplanService
# import shutil
# import os

# router = APIRouter()
# service = FloorplanService()

# UPLOAD_DIR = "uploads"

# @router.post("/upload/")
# async def upload_dxf(file: UploadFile = File(...)):
#     file_path = os.path.join(UPLOAD_DIR, file.filename)
    
#     # Save file to server
#     with open(file_path, "wb") as buffer:
#         shutil.copyfileobj(file.file, buffer)
    
#     # Parse DXF and save to DB
#     dxf_id = service.parse_dxf(file_path)
#     return {"message": "DXF file processed", "dxf_id": dxf_id}

# @router.get("/floorplans/")
# async def get_all_floorplans():
#     return service.get_all_floorplans()

# @router.get("/floorplans/{dxf_id}/path/{room_name}")
# async def get_path(dxf_id: int, room_name: str):
#     path = service.find_path(dxf_id, room_name)
#     if not path:
#         raise HTTPException(status_code=404, detail="Path not found")
#     return {"path": path}