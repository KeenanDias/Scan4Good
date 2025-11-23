package ca.keenan.repositories;



import ca.keenan.model.HealthTip;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface HealthTipRepository extends JpaRepository<HealthTip, Long> {
    // Custom query method to find tips by risk level
    List<HealthTip> findByRiskLevel(String riskLevel);
}