package ca.keenan.beans;

import com.fasterxml.jackson.annotation.JsonProperty;
import lombok.Data;

@Data
public class RiskResponse {
    // Maps "risk_level" from Python JSON to this Java field
    @JsonProperty("risk_level")
    private String riskLevel;
}