import { Component, ChangeDetectorRef } from '@angular/core'; 
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { ApiService } from '../../services/api'; 

@Component({
  selector: 'app-survey',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './survey.html', 
  styleUrls: ['./survey.css']
})
export class SurveyComponent {
  formData = {
    age: null,
    weight: null,
    height: null,
    sleep: null,
    exercise: 'medium',    
    sugarIntake: 'medium', 
    smoking: 'no',
    alcohol: 'no',
    married: 'no',
    profession: 'student'
  };

  // Stores the result from Spring Boot
  result: any = null;
  isLoading = false;

  // 2. Inject ChangeDetectorRef in the constructor
  constructor(private apiService: ApiService, private cdr: ChangeDetectorRef) {
    this.result = { riskLevel: 'TEST', tips: [] };
  }

  onSubmit() {
    this.isLoading = true;
    this.result = null;

    console.log('Sending survey data:', this.formData); 

    this.apiService.submitSurvey(this.formData).subscribe({
      next: (response) => {
        console.log('Backend Response Received:', response); 
        
        this.result = response; 
        this.isLoading = false;
      
        this.cdr.detectChanges(); 
      },
      error: (error) => {
        console.error('Error submitting survey:', error);
        alert('Could not connect to the backend. Check console for details.');
        
        this.isLoading = false;
        this.cdr.detectChanges(); // Force update even on error
      }
    });
  }

  // Helper to change color based on risk
  getRiskColor(level: string): string {
    if (level === 'High') return '#ef4444'; // Red
    if (level === 'Medium') return '#f59e0b'; // Orange
    return '#10b981'; // Green
  }
}