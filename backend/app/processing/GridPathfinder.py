import numpy as np
import heapq
# from DXFProcessor import DXFProcessor
from app.processing.DXFProcessor import DXFProcessor
import matplotlib.pyplot as plt
from matplotlib import colors
import io
import base64

class GridPathfinder:
    def __init__(self, walls, rooms, entrance, grid_size = (50, 50)):
        """
        :param walls: List of wall line segments from DXF
        :param rooms: List of room text positions (doorways)
        :param entrance: Entrance point
        :param grid_size: Defines the size of the grid
        """
        self.grid_size = grid_size  # Define a fixed grid resolution
        self.grid = np.zeros((int(grid_size[0]), int(grid_size[1])), dtype=int) # Fills grid with zeroes
        self.rooms = rooms
        self.entrance = entrance
        print(f"entrance: {self.entrance}")
        self.start = self.to_grid(entrance["coordinates"])
        print(f"start: {self.start}")
        self.targets = {room["text"]: self.to_grid(room["coordinates"]) for room in rooms}

        self.mark_walls(walls) # Mark walls as 1
        self.grid[self.start] = 2  # Mark entrance as 2
        for room in self.targets.values():
            self.grid[room] = 3  # Mark room doorways as 3

    def to_grid(self, point):
        """
        Convert real-world DXF coordinates to a grid cell index.
        :param point: The point to be converted to a grid
        """
        x, y = point
        grid_x = int(x)  
        grid_y = int(y)
        return min(grid_x, self.grid_size[0] - 1), min(grid_y, self.grid_size[1] - 1)

    def mark_walls(self, walls):
        """
        Mark walls as obstacles (1) on the grid.
        :param walls: Listof wall line segments from the dxf file
        """
        for wall in walls:
            start = self.to_grid(wall["start"])
            end = self.to_grid(wall["end"])
            self.bresenham_line(start, end)

    def bresenham_line(self, start, end):
        """
        Rasterize a line onto the grid using Bresenham's algorithm.
        :param start: Starting point of the wall
        :param end: Ending point of the wall
        """
        x1, y1 = start
        x2, y2 = end
        x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)

        dx, dy = abs(x2 - x1), abs(y2 - y1)
        sx, sy = (1 if x1 < x2 else -1), (1 if y1 < y2 else -1)
        err = dx - dy

        while True:
            self.grid[x1, y1] = 1  # Mark as obstacle
            if (x1, y1) == (x2, y2):
                break
            e2 = 2 * err
            if e2 > -dy:
                err -= dy
                x1 += sx
            if e2 < dx:
                err += dx
                y1 += sy

    def find_path(self, room_name):
        """
        Finds the shortest path from entrance to selected room using A*.
        :param room_name: The ID number of the goal room 
        """
        if room_name not in self.targets:
            print(f"Room '{room_name}' not found.")
            return None
        
        target = self.targets[room_name]
        return self.a_star(self.start, target)

    def a_star(self, start, end):
        """A* pathfinding algorithm for shortest path."""
        neighbors = [(0,1), (1,0), (0,-1), (-1,0)]  # 4-directional movement
        open_list = [(0, start)]  # (cost, position)
        g_score = {start: 0} # initial g score
        f_score = {start: self.heuristic(start, end)} # initial f score
        came_from = {}

        while open_list:
            _, current = heapq.heappop(open_list)

            if current == end:
                return self.reconstruct_path(came_from, current)

            for dx, dy in neighbors:
                neighbor = (current[0] + dx, current[1] + dy)

                if not (0 <= neighbor[0] < self.grid_size[0] and 0 <= neighbor[1] < self.grid_size[1]):
                    continue  # Out of bounds
                if self.grid[neighbor] == 1:
                    continue  # Wall

                tentative_g_score = g_score[current] + 1
                if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = tentative_g_score + self.heuristic(neighbor, end)
                    heapq.heappush(open_list, (f_score[neighbor], neighbor))
                    came_from[neighbor] = current

        return None  # No path found

    def heuristic(self, a, b):
        """Manhattan distance heuristic for A*."""
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    def reconstruct_path(self, came_from, current):
        """Reconstructs the path after A* finds the shortest route."""
        path = []
        while current in came_from:
            path.append(current)
            current = came_from[current]
        path.reverse()
        return path

    def display_grid(self, entrance, rooms, path = None, img = True):
        """Generate a grid image and return it as base64."""
        plt.figure(figsize=(10, 10))

        plt.imshow(self.grid, cmap="gray_r", origin="upper")

        # Add Entrance & Rooms
        ex, ey = self.start
        plt.text(ey, ex, "S", ha='center', va='center', color="blue", fontsize=12, fontweight='bold')
        for room_name, (rx, ry) in self.targets.items():
            plt.text(ry, rx, room_name, ha='center', va='center', color="green", fontsize=10, fontweight='bold')

        # Mark path in red
        if path:
            for px, py in path:
                plt.scatter(py, px, color="red", s=10)  # Scatter points in red

        plt.xticks([])
        plt.yticks([])

        if img:
            # Save to memory
            buf = io.BytesIO()
            plt.savefig(buf, format="png")
            buf.seek(0)

            # Convert image to base64
            image_base64 = base64.b64encode(buf.getvalue()).decode("utf-8")
            plt.close()
            return image_base64
        
        else:
            plt.title('Grid Representation')
            plt.show()
            return 0

        




if __name__ == "__main__":
    processor = DXFProcessor(file_path="good.dxf")
    processor.parse_dxf()

    walls = processor.get_walls()
    rooms = processor.get_rooms()
    entrance = processor.get_entrance()
    grid_size = processor.get_grid_size(walls)

    print(f"Walls: {walls}")
    print(f"Rooms: {rooms}")
    print(f"Entrance: {entrance}")
    print(f"Grid Size: {grid_size}")

    pathfinder = GridPathfinder(walls, rooms, entrance, grid_size)

    # Find shortest path to a specific room
    room_name = "102"
    path = pathfinder.find_path(room_name)
    print(f"Path to {room_name}:", path)

    pathfinder.display_grid(entrance, rooms, img=False)
    pathfinder.display_grid(entrance, rooms, path, img=False)
