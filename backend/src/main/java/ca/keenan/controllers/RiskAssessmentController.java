package ca.keenan.controllers;

import java.util.List;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.CrossOrigin;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.client.RestTemplate;

import ca.keenan.beans.FullAssessment;
import ca.keenan.beans.RiskResponse;
import ca.keenan.beans.UserHealthData;
import ca.keenan.model.HealthTip;
import ca.keenan.repositories.HealthTipRepository;

import java.util.List;

@RestController
@RequestMapping("/api/scan")
@CrossOrigin(origins = "http://localhost:4200") // Allow Angular to access this
public class RiskAssessmentController {

    @Autowired
    private RestTemplate restTemplate;

    @Autowired
    private HealthTipRepository tipRepository;

    @PostMapping("/assess")
    public ResponseEntity<FullAssessment> assessRisk(@RequestBody UserHealthData healthData) {
        
        // 1. Send data to Python ML Service
        // Ensure your Python app is running on port 5000
        String pythonServiceUrl = "http://localhost:5000/predict";
        
        RiskResponse aiResponse;
        try {
            aiResponse = restTemplate.postForObject(pythonServiceUrl, healthData, RiskResponse.class);
        } catch (Exception e) {
            // Fallback if Python is down (Good for Hackathon stability)
            aiResponse = new RiskResponse();
            aiResponse.setRiskLevel("Medium"); 
            System.err.println("AI Service Error: " + e.getMessage());
        }

        // 2. Fetch relevant tips from MySQL
        List<HealthTip> tips = tipRepository.findByRiskLevel(aiResponse.getRiskLevel());

        // 3. Combine and return
        FullAssessment response = new FullAssessment(aiResponse.getRiskLevel(), tips);
        return ResponseEntity.ok(response);
    }
}
