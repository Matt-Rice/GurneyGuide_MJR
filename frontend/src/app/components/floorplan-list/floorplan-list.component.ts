import { Component, OnInit } from '@angular/core';
import { PathfinderService } from '../../services/pathfinder.service';

@Component({
  selector: 'app-floorplan-list',
  templateUrl: './floorplan-list.component.html',
  styleUrls: ['./floorplan-list.component.css']
})
export class FloorplanListComponent implements OnInit {
  floorplans: any[] = [];

  constructor(private pathfinderService: PathfinderService) {}

  ngOnInit() {
    this.loadFloorplans();
  }

  loadFloorplans() {
    this.pathfinderService.getAllFloorplans().subscribe({
      next: (data) => {
        this.floorplans = data;
      },
      error: (error) => {
        console.error('Error fetching floorplans:', error);
      }
    });
  }

  deleteFloorplan(id: number) {
    this.pathfinderService.delete(id).subscribe({
      next: () => {
        this.floorplans = this.floorplans.filter(fp => fp.id !== id);
      },
      error: (error) => {
        console.error('Error deleting floorplan:', error);
      }
    });
  }

  selectFloorplan(id: number) {
    console.log('Selected floorplan:', id);
    // Navigate to a new component or update UI accordingly
  }
}
