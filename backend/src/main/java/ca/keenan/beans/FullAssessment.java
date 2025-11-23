package ca.keenan.beans;


import ca.keenan.model.HealthTip;
import lombok.AllArgsConstructor;
import lombok.Data;
import java.util.List;

@Data
@AllArgsConstructor
public class FullAssessment {
    private String riskLevel;
    private List<HealthTip> tips;
}