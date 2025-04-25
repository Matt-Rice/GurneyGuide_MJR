import { Component } from '@angular/core';
import { NgIf} from '@angular/common';
import { RouterLink } from '@angular/router';

@Component({
  imports: [NgIf, RouterLink],
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.scss']
})
export class HomeComponent {
  openSections: { [key: string]: boolean } = {};

  toggleSection(section: string): void {
    this.openSections[section] = !this.openSections[section];
  }

  isSectionOpen(section: string): boolean {
    return !!this.openSections[section];
  }
}
