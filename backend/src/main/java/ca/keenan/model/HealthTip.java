package ca.keenan.model;

import jakarta.persistence.*;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@Entity
@Table(name = "health_tips")
@Data // Generates Getters, Setters, toString, etc.
@NoArgsConstructor
@AllArgsConstructor
public class HealthTip {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(name = "risk_level")
    private String riskLevel; // 'Low', 'Medium', 'High'

    @Column(name = "advice_text", columnDefinition = "TEXT")
    private String adviceText;

    @Column(name = "resource_link")
    private String resourceLink;
}