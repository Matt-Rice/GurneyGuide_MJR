import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { NgFor } from '@angular/common';
import { NgIf } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { ChangeDetectorRef } from '@angular/core';
import { PathfinderService } from '../../services/pathfinder.service';

@Component({
  selector: 'app-pathfinder',
  templateUrl: './pathfinder.component.html',
  styleUrls: ['./pathfinder.component.scss'],
  imports: [FormsModule, CommonModule, NgFor, NgIf]
})
export class PathfinderComponent {
  floorplanId: number = 1;
  roomNum: string = "1";
  path: [number, number][] = [];
  walls: { start: [number, number]; end: [number, number] }[] = [];
  rooms: { text: string; coordinates: [number, number] }[] = [];
  entrance: { coordinates: [number, number] } | null = null;

  cellSize = 1;

  constructor(private pathfinderService: PathfinderService, private cdr: ChangeDetectorRef) {}

  findPath() {
    this.pathfinderService.findPath(this.floorplanId, this.roomNum).subscribe({
      next: (data) => {
        console.log('PATH RESPONSE:', data);
        this.path = data.path;
        this.walls = data.walls;
        console.log('walls:', this.walls)
        this.rooms = data.rooms;
        this.entrance = data.entrance;
        this.cdr.detectChanges();
      },
      error: (error) => {
        console.error('Error fetching path:', error);
      }
    });
  }
}