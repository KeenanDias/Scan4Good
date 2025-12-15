import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class ApiService {
  // Matches your Spring Boot Controller URL
  private apiUrl = 'http://localhost:8080/api/scan/assess';

  constructor(private http: HttpClient) {}

  // Send the user data to the backend
  submitSurvey(data: any): Observable<any> {
    return this.http.post(this.apiUrl, data);
  }
}