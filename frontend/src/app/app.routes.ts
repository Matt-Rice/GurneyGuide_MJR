import { Routes } from '@angular/router';
import { HomeComponent } from './componenents/home/home.component';
import { FloorplanListComponent } from './componenents/floorplan-list/floorplan-list.component';
import { PathfinderComponent } from './componenents/pathfinder/pathfinder.component';

export const routes: Routes = [
    {
        path: '',
        component: HomeComponent
    },

    {
        path: 'upload',
        component: FloorplanListComponent
    },
    
    {
        path: 'pathfind',
        component: PathfinderComponent
    },

];
