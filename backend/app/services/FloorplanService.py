from app.processing.GridPathfinder import GridPathfinder
from app.processing.DXFProcessor import DXFProcessor
from app.DbContext import DBContext
import os

class FloorplanService():
    
    def __init__(self):
        self.db_context = DBContext(os.getenv("DATABASE_URL"))

    def parse_dxf(self, file_path, wall_layer="Walls", room_layer="Rooms", entrance_layer="Entrance"):
        """
        Parses a DXF file and adds it to the database along with its walls, rooms, and entrance values.
        """
        
        try:
            
            # Get and process the dxf
            processor = DXFProcessor(file_path, wall_layer, room_layer, entrance_layer) 
            processor.parse_dxf()
            
            # Get properties of dxf
            walls = processor.get_walls()
            rooms = processor.get_rooms()
            entrance = processor.get_entrance()
            grid_size = processor.get_grid_size(walls)

            # Add dxf to database
            id = self.db_context.add_dxf_file(file_path, walls, rooms, entrance, grid_size)

            return id
            
        
        except Exception as e:
            print(f"Unexpected error {e}")    

    def find_path(self, dxf_id, room_name):
        """Finds and returns the path for a given room"""
        # Get properties
        walls, rooms, entrance, grid_size = self.get_floorplan_by_id(dxf_id)

        # Get Pth
        self.pathfinder = GridPathfinder(walls, rooms, entrance, grid_size)
        path = self.pathfinder.find_path(room_name)

        return self.pathfinder.display_grid(entrance, rooms, path)
    
    def get_floorplan_by_id(self, dxf_id):
        """Returns specific floorplan's details by ID"""
        dxf_data = self.db_context.get_dxf_file(dxf_id)
        walls = dxf_data["walls"]
        rooms = dxf_data["rooms"]
        entrance = dxf_data["entrance"]
        grid_size = dxf_data["grid_size"]

        return walls, rooms, entrance, grid_size
    
    def get_all_floorplans(self):
        """Returns all floorplans that are currently in the database"""
        return self.db_context.get_all_floorplans()
    
    def delete_floorplan(self, dxf_id):
        """Deletes a floorplan with the specified id"""
        success = self.db_context.delete_floorplan(dxf_id)

if __name__ == '__main__':
    file_path = 'cool.dxf'
    service = FloorplanService()
    id = service.parse_dxf(file_path)
    floorplan = service.get_floorplan_by_id(id)
    image = service.find_path(id, 101)

