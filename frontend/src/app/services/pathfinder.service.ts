import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class PathfinderService {
  private baseUrl = 'http://localhost:8000';

  constructor(private http: HttpClient) {}

  get(): Observable<any> {
    return this.http.get(`${this.baseUrl}/`);
  }

  uploadDxf(file: File): Observable<any> {
    const formData = new FormData();
    formData.append('file', file);
    return this.http.post(`${this.baseUrl}/upload-dxf`, formData);
  }

  getAllFloorplans(): Observable<any> {
    return this.http.get(`${this.baseUrl}/floorplans`);
  }

  getFloorplanById(id: number): Observable<any> {
    return this.http.get(`${this.baseUrl}/floorplan/${id}`);
  }

  findPath(id: number, roomNum: number): Observable<any> {
    return this.http.get(`${this.baseUrl}/floorplan/${id}/path/${roomNum}`);
  }

  delete(id: number): Observable<any> {
    return this.http.delete(`${this.baseUrl}/floorplan/${id}`);
  }
}
