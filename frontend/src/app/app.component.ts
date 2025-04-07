import { Component } from '@angular/core';
// import { RouterOutlet } from '@angular/router';
import { PathfinderComponent } from './componenents/pathfinder/pathfinder.component';
import { FloorplanListComponent } from './componenents/floorplan-list/floorplan-list.component';
import { FileUploadComponent } from './componenents/file-upload/file-upload.component';
@Component({
  selector: 'app-root',
  imports: [FloorplanListComponent, PathfinderComponent, FileUploadComponent],
  templateUrl: './app.component.html',
  styleUrl: './app.component.scss'
})
export class AppComponent {
  title = 'frontend';
}