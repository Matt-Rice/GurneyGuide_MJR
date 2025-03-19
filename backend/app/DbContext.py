from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
import os

Base = declarative_base()

class DXFFile(Base):
    __tablename__ = "dxf_files"

    id = Column(Integer, primary_key=True, autoincrement=True)
    file_name = Column(String, nullable=False)
    uploaded_at = Column(String, nullable=False)
    grid_x = Column(Float, nullable=False)
    grid_y = Column(Float, nullable=False)

    walls = relationship("Wall", back_populates="dxf_file", cascade="all, delete-orphan")
    rooms = relationship("Room", back_populates="dxf_file", cascade="all, delete-orphan")
    entrance = relationship("Entrance", uselist=False, back_populates="dxf_file", cascade="all, delete-orphan")


class Wall(Base):
    __tablename__ = "walls"

    id = Column(Integer, primary_key=True, autoincrement=True)
    dxf_file_id = Column(Integer, ForeignKey("dxf_files.id"), nullable=False)
    start_x = Column(Float, nullable=False)
    start_y = Column(Float, nullable=False)
    end_x = Column(Float, nullable=False)
    end_y = Column(Float, nullable=False)

    dxf_file = relationship("DXFFile", back_populates="walls")

class Room(Base):
    __tablename__ = "rooms"

    id = Column(Integer, primary_key=True, autoincrement=True)
    dxf_file_id = Column(Integer, ForeignKey("dxf_files.id"), nullable=False)
    name = Column(String, nullable=False)
    x = Column(Float, nullable=False)
    y = Column(Float, nullable=False)

    dxf_file = relationship("DXFFile", back_populates="rooms")

class Entrance(Base):
    __tablename__ = "entrance"

    id = Column(Integer, primary_key=True, autoincrement=True)
    dxf_file_id = Column(Integer, ForeignKey("dxf_files.id"), nullable=False)
    x = Column(Float, nullable=False)
    y = Column(Float, nullable=False)

    dxf_file = relationship("DXFFile", back_populates="entrance")

class DBContext:
    def __init__(self, db_url=os.getenv("DATABASE_URL")):
        self.engine = create_engine(db_url)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()
        Base.metadata.create_all(self.engine, checkfirst=True)  # Create tables if they don't exist

    def add_dxf_file(self, file_name, walls, rooms, entrance, grid_size):
        """
        Inserts a DXF file entry and its associated walls, rooms, and entrance.
        """
        try:
            #print("Debug Walls:", walls)  # Debug print
            print (f"Debug Entrance, type: {type(entrance)} val: {entrance}")

            new_dxf = DXFFile(file_name=file_name, uploaded_at="NOW()", grid_x=grid_size[0], grid_y=grid_size[1])
            self.session.add(new_dxf)
            self.session.commit()  # Commit to generate DXF file ID

            for wall in walls:
                if not isinstance(wall, dict):
                    print(f"Skipping invalid wall: {wall}")
                    continue  # Skip invalid items

                # Ensure the required keys exist
                if "start" not in wall or "end" not in wall:
                    print(f"Skipping wall with missing keys: {wall}")
                    continue

                # Explicitly extract values
                start_x, start_y = wall["start"]
                end_x, end_y = wall["end"]

                wall_entry = Wall(
                    dxf_file_id=new_dxf.id,
                    start_x=start_x,
                    start_y=start_y,
                    end_x=end_x,
                    end_y=end_y
                )
                self.session.add(wall_entry)

            # Insert rooms
            for room in rooms:
                if not isinstance(room, dict) or "text" not in room or "coordinates" not in room:
                    print(f"Skipping invalid room: {room}")
                    continue  # Skip invalid items
                
                room_entry = Room(
                    dxf_file_id=new_dxf.id,
                    name=room["text"],
                    x=room["coordinates"][0], 
                    y=room["coordinates"][1]
                )
                self.session.add(room_entry)

            print("Entrance")
            # Ensure entrance is a list and contains at least one dictionary
            if isinstance(entrance, list) and len(entrance) > 0:
                entrance = entrance[0]  # Take the first entrance

            # Ensure entrance is now a dictionary before inserting
            if isinstance(entrance, dict) and "coordinates" in entrance:
                x, y = entrance["coordinates"]  # Extract values
                print(f"Adding entrance at ({x}, {y})")  # Debugging print

                entrance_entry = Entrance(
                    dxf_file_id=new_dxf.id,
                    x=x,
                    y=y
                )
                self.session.add(entrance_entry)
            else:
                print("Warning: Entrance format is incorrect or missing coordinates.")

            self.session.commit()
            print(f"DXF file '{file_name}' added successfully!")
            return new_dxf.id

        except Exception as e:
            self.session.rollback()
            print(f"Error adding DXF file: {e}")

    def get_dxf_file(self, file_id):
        """
        Fetch a DXF file with its walls, rooms, and entrance.
        """
        try:
            dxf_file = self.session.query(DXFFile).filter_by(id=file_id).first()
            if not dxf_file:
                return None

            walls = [{"start": (w.start_x, w.start_y), "end": (w.end_x, w.end_y)} for w in dxf_file.walls]
            rooms = [{"text": r.name, "coordinates": (r.x, r.y)} for r in dxf_file.rooms]
            entrance = {"coordinates": (dxf_file.entrance.x, dxf_file.entrance.y)} if dxf_file.entrance else None
            grid_size = (dxf_file.grid_x, dxf_file.grid_y)

            return {
                "file_name": dxf_file.file_name,
                "uploaded_at": dxf_file.uploaded_at,
                "walls": walls,
                "rooms": rooms,
                "entrance": entrance,
                "grid_size" : grid_size
            }
        except Exception as e:
            print(f"Error fetching DXF file: {e}")
            return None

    def get_all_floorplans(self):
        """
        Retrieves all DXF files along with their walls, rooms, and entrances.
        """
        try:
            dxf_files = self.session.query(DXFFile).all()
            floorplans = []

            for dxf in dxf_files:
                walls = [{"start": (w.start_x, w.start_y), "end": (w.end_x, w.end_y)} for w in dxf.walls]
                rooms = [{"text": r.name, "coordinates": (r.x, r.y)} for r in dxf.rooms]
                entrance = {"coordinates": (dxf.entrance.x, dxf.entrance.y)} if dxf.entrance else None
                grid_size = (dxf.grid_x, dxf.grid_y)

                floorplans.append({  
                    "id": dxf.id,
                    "file_name": dxf.file_name,
                    "uploaded_at": dxf.uploaded_at,
                    "walls": walls,
                    "rooms": rooms,
                    "entrance": entrance,
                    "grid_size": grid_size
                })

            return floorplans 

        except Exception as e:
            print(f"Error fetching all floorplans: {e}")
            return []
    
    def delete_floorplan(self, dxf_id):
        """
        Deletes a floorplan (DXF file) and all its associated data from the database.
        
        :param dxf_id: The ID of the DXF file to delete.
        """
        try:
            # Fetch the DXF file
            dxf_file = self.session.query(DXFFile).filter_by(id=dxf_id).first()

            if not dxf_file:
                print(f"DXF file with ID {dxf_id} not found.")
                return False
            
            # Delete the DXF file (this will cascade to delete walls, rooms, and entrance)
            self.session.delete(dxf_file)
            self.session.commit()
            print(f"DXF file with ID {dxf_id} deleted successfully!")
            return True

        except Exception as e:
            self.session.rollback()
            print(f"Error deleting DXF file: {e}")
            return False
    
    def close(self):
        """
        Closes the database session.
        """
        self.session.close()
