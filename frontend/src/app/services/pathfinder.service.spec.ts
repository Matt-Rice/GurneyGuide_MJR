import { TestBed } from '@angular/core/testing';

import { PathfinderService } from './pathfinder.service';

describe('PathfinderService', () => {
  let service: PathfinderService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(PathfinderService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
