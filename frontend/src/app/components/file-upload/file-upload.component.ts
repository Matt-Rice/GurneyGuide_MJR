import { Component } from '@angular/core';
import { PathfinderService } from '../../services/pathfinder.service';

@Component({
  selector: 'app-file-upload',
  templateUrl: './file-upload.component.html',
  styleUrls: ['./file-upload.component.css']
})
export class FileUploadComponent {
  selectedFile: File | null = null;
  uploadResponse: string = '';

  constructor(private pathfinderService: PathfinderService) {}

  onFileSelected(event: Event) {
    const target = event.target as HTMLInputElement;
    if (target.files && target.files.length > 0) {
      this.selectedFile = target.files[0];
    }
  }

  onUpload() {
    if (this.selectedFile) {
      this.pathfinderService.uploadDxf(this.selectedFile).subscribe({
        next: (response) => {
          this.uploadResponse = 'File uploaded successfully!';
        },
        error: (error) => {
          this.uploadResponse = 'Error uploading file.';
          console.error(error);
        }
      });
    }
  }
}
