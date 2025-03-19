import { ComponentFixture, TestBed } from '@angular/core/testing';

import { FloorplanListComponent } from './floorplan-list.component';

describe('FloorplanListComponent', () => {
  let component: FloorplanListComponent;
  let fixture: ComponentFixture<FloorplanListComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [FloorplanListComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(FloorplanListComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
