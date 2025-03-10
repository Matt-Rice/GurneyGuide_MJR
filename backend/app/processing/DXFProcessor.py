import ezdxf
import math

class DXFProcessor:
    def __init__(self, file_path: str, walls_layer: str = "Walls", rooms_layer: str = "Rooms", entrance_layer: str = "Entrance"):
        self.file_path = file_path
        self.walls_layer = walls_layer
        self.rooms_layer = rooms_layer
        self.entrance_layer = entrance_layer
        self.doc = None
        self.msp = None
        self.origin_shift = (0, 0)

    def parse_dxf(self):
        """
        Reads the DXF file and shifts coordinates to start at (0,0).
        """
        try:
            self.doc = ezdxf.readfile(self.file_path)
            self.msp = self.doc.modelspace()
            self.calculate_origin_shift()
        except IOError as e:
            print(f"Could not open file: {self.file_path} -> {e}")
        except ezdxf.DXFStructureError as e:
            print(f"Invalid or corrupted DXF file: {self.file_path} -> {e}")

    def calculate_origin_shift(self):
        """Finds the minimum X and Y values to shift the entire floorplan."""
        min_x, min_y = float("inf"), float("inf")
        
        for entity in self.msp.query("*"):
            if hasattr(entity.dxf, "start"):
                min_x = min(min_x, entity.dxf.start[0])
                min_y = min(min_y, entity.dxf.start[1])
            if hasattr(entity.dxf, "insert"):
                min_x = min(min_x, entity.dxf.insert[0])
                min_y = min(min_y, entity.dxf.insert[1])

        self.origin_shift = (min_x, min_y)

    def shift_point(self, point):
        """Applies the origin shift to a point."""
        return (point[0] - self.origin_shift[0], point[1] - self.origin_shift[1])

    def get_walls(self):
        """Gets walls and shifts coordinates to a new origin."""
        walls = []
        for entity in self.msp.query("*"):
            if entity.dxf.layer == self.walls_layer:
                if entity.dxftype() == "LINE":
                    start = self.shift_point((entity.dxf.start[0], entity.dxf.start[1]))
                    end = self.shift_point((entity.dxf.end[0], entity.dxf.end[1]))
                    walls.append({"type": "LINE", "start": start, "end": end})

                if entity.dxftype() == "LWPOLYLINE":
                    points = [self.shift_point((p[0], p[1])) for p in entity.get_points()]
                    walls.append({"type": "LWPOLYLINE", "points": points})

        return walls

    def get_grid_size(self, walls):
        """Returns the total size of the grid assuming walls are the boundaries"""
        x_coords = []
        y_coords = []

        # Get all coordinates from each wall
        for wall in walls:
            x_coords.extend([wall["start"][0], wall["end"][0]])
            y_coords.extend([wall["start"][1], wall["end"][1]])

        # Get grid size
        min_x, max_x, min_y, max_y = min(x_coords), max(x_coords), min(y_coords), max(y_coords)

        width = math.ceil(max_x - min_x)
        height = math.ceil(max_y - min_y)

        return width, height
    
    def get_rooms(self):
        """Gets rooms and shifts text positions."""
        rooms = []
        for entity in self.msp.query("TEXT MTEXT"):
            if entity.dxf.layer == self.rooms_layer:
                insert = self.shift_point((entity.dxf.insert[0], entity.dxf.insert[1]))
                text_value = entity.dxf.text if entity.dxftype() == 'TEXT' else entity.text
                rooms.append({"text": text_value, "coordinates": insert})

        return rooms

    def get_entrance(self):
        """Gets the entrance and shifts its coordinates."""
        entrance = []
        for entity in self.msp.query("*"):
            if entity.dxf.layer == self.entrance_layer:
                if entity.dxftype() in ['POINT', 'TEXT', 'MTEXT']:
                    insert = self.shift_point((entity.dxf.insert[0], entity.dxf.insert[1]))
                    entrance.append({"coordinates": insert})

        return entrance
    


