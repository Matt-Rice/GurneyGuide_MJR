from backend.app.processing.GridPathfinder import GridPathfinder
from backend.app.processing.DXFProcessor import DXFProcessor
from backend.app.DbContext import DBContext

class FloorplanService():
    
    def __init__(self):
        self.db_context = DBContext()

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

        return path
    
    def get_floorplan_by_id(self, dxf_id):
        """Returns specific floorplan's details by ID"""
        dxf_data = self.db_context.get_dxf_file(dxf_id)
        walls = dxf_data["walls"]
        rooms = dxf_data["rooms"]
        entrance = dxf_data["entrance"]
        grid_size = dxf_data["grid_size"]

        return walls, rooms, entrance, grid_size

