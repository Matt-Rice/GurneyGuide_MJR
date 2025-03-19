import { Component } from '@angular/core';
import { JsonPipe } from '@angular/common';
import { PathfinderService } from '../../services/pathfinder.service';

@Component({
  selector: 'app-pathfinder',
  templateUrl: './pathfinder.component.html',
  styleUrls: ['./pathfinder.component.css'],
  imports: [JsonPipe]
})
export class PathfinderComponent {
  floorplanId: number = 1;
  roomNum: number = 1;
  path: any = null;

  constructor(private pathfinderService: PathfinderService) {}

  findPath() {
    this.pathfinderService.findPath(this.floorplanId, this.roomNum).subscribe({
      next: (data) => {
        this.path = data;
      },
      error: (error) => {
        console.error('Error fetching path:', error);
      }
    });
  }
}
