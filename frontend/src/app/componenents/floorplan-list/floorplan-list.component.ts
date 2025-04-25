import { Component, OnInit } from '@angular/core';
import { PathfinderService } from '../../services/pathfinder.service';
import { ChangeDetectorRef } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';
import { FileUploadComponent } from '../file-upload/file-upload.component';
import { NgFor } from '@angular/common';
import { NgIf } from '@angular/common';

@Component({
  selector: 'app-floorplan-list',
  templateUrl: './floorplan-list.component.html',
  styleUrls: ['./floorplan-list.component.scss'],
  imports: [FormsModule, NgFor, NgIf, FileUploadComponent]
})
export class FloorplanListComponent implements OnInit {
  floorplans: any[] = [];
  selectedFloorplan: number = 0;
  path: [number, number][] = [];
  walls: { start: [number, number]; end: [number, number] }[] = [];
  rooms: { text: string; coordinates: [number, number] }[] = [];
  entrance: { coordinates: [number, number] } | null = null;

  cellSize = 1;

  constructor(private pathfinderService: PathfinderService, private cdr: ChangeDetectorRef) {}

  ngOnInit() {
    this.loadFloorplans();
  }

  loadFloorplans() {
    this.pathfinderService.getAllFloorplans().subscribe({
      next: (data) => {
        this.floorplans = data.floorplans;
        console.log("floorplan: ", this.floorplans)
        this.cdr.detectChanges();
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
    this.selectedFloorplan = id;
    this.pathfinderService.getFloorplanById(id).subscribe({
      next: (data) => {
        console.log('RESPONSE:', data);
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