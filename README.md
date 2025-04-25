## Abstract
Efficient navigation in healthcare facilities is crucial for transporting patients and for responding to emergencies. However, hospitals generally have complex layouts that can be difficult to understand, which makes it difficult for people unfamiliar with the layout to navigate to certain areas. Gurney Guide is an application that is designed to process 2D floorplans, convert them into a computer-navigable environment, and use a path-planning algorithm, determining optimal routes from a starting point to a target room or area so that a user can take the shortest path to the target area. The system works by processing a DXF file, a file commonly used in designing floorplans, by gathering the coordinates of all the walls, the entrance/starting point, and the rooms. Once it has this information, it adds this information to a Postgres database so that it can be used later by the user. Then, the backend converts this information into a grid and after a user selects a room number, using the A* algorithm, an optimal path to that room from their location will be generated and displayed to them. After preliminary testing, Gurney Guide is able to recognize walls, rooms, and entrances, generate the optimal paths from the entrance to a room, and display those paths. The only downside is that the files must be formatted in a very specific way with the walls, rooms, and entrance each being on separate layers. Gurney Guide has the potential to enhance hospital navigation by providing automated navigational assistance to users so that they could transport patients more efficiently and respond more quickly to emergencies.

## How to run

### 1. First clone the repository 
```bash git clone https://github.com/Matt-Rice/GurneyGuide_MJR.git```

### 2. Download Docker Desktop and run it: https://www.docker.com/products/docker-desktop/
   
### 3. Using the terminal, navigate to the directory in which you cloned the repository into and run the following command:
   ```cmd docker-compose up --build```
   
## 5. Navigate to http://localhost:4200 to view the frontend
