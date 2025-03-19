import { Component } from '@angular/core';
// import { RouterOutlet } from '@angular/router';
import { FloorplanListComponent } from './components/floorplan-list/floorplan-list.component';
import { PathfinderComponent } from './components/pathfinder/pathfinder.component';
import { FileUploadComponent } from './components/file-upload/file-upload.component';

@Component({
  selector: 'app-root',
  imports: [FloorplanListComponent, PathfinderComponent, FileUploadComponent],
  templateUrl: './app.component.html',
  styleUrl: './app.component.css'
})
export class AppComponent {
  title = 'frontend';
}
