from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

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
    def __init__(self, db_url="postgresql://user:password@localhost:5432/dxf_db"):
        self.engine = create_engine(db_url)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()
        Base.metadata.create_all(self.engine)  # Create tables if they don't exist

    def add_dxf_file(self, file_name, walls, rooms, entrance, grid_size):
        """
        Inserts a DXF file entry and its associated walls, rooms, and entrance.
        """
        try:
            new_dxf = DXFFile(file_name=file_name, uploaded_at="NOW()", grid_x=grid_size[0], grid_y=grid_size[1])

            self.session.add(new_dxf)
            self.session.commit()  # Commit to generate DXF file ID

            # Insert walls
            for wall in walls:
                wall_entry = Wall(
                    dxf_file_id=new_dxf.id,
                    start_x=wall["start"][0], start_y=wall["start"][1],
                    end_x=wall["end"][0], end_y=wall["end"][1]
                )
                self.session.add(wall_entry)

            # Insert rooms
            for room in rooms:
                room_entry = Room(
                    dxf_file_id=new_dxf.id,
                    name=room["text"],
                    x=room["coordinates"][0], y=room["coordinates"][1]
                )
                self.session.add(room_entry)

            # Insert entrance
            if entrance:
                entrance_entry = Entrance(
                    dxf_file_id=new_dxf.id,
                    x=entrance["coordinates"][0], y=entrance["coordinates"][1]
                )
                self.session.add(entrance_entry)

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

    def close(self):
        """
        Closes the database session.
        """
        self.session.close()
