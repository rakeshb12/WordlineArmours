--Check data distribution: 
SELECT
  is_legit,
  COUNT(*) as count,
  COUNT(*) * 100.0 / SUM(COUNT(*)) OVER() as percentage
FROM
  `your-project-id.your_dataset_id.merchant_risk_data`
GROUP BY
  is_legit;

-- Example: Domain age for legit vs. fake
SELECT
  is_legit,
  AVG(domain_age_days) as avg_domain_age,
  STDDEV(domain_age_days) as stddev_domain_age,
  MIN(domain_age_days) as min_domain_age,
  MAX(domain_age_days) as max_domain_age
FROM
  `your-project-id.your_dataset_id.merchant_risk_data`
GROUP BY
  is_legit;

-- Example: Impersonation risk score
SELECT
  is_legit,
  AVG(impersonation_risk_score) as avg_impersonation_risk,
  MIN(impersonation_risk_score) as min_impersonation_risk,
  MAX(impersonation_risk_score) as max_impersonation_risk
FROM
  `your-project-id.your_dataset_id.merchant_risk_data`
GROUP BY
  is_legit;

-- Example: Signal counts
SELECT
  is_legit,
  COUNTIF(signals LIKE '%new_domain%') as new_domain_signals,
  COUNTIF(signals LIKE '%impersonation_risk%') as impersonation_risk_signals,
  COUNTIF(signals LIKE '%sanctions_match%') as sanctions_match_signals,
  COUNTIF(signals LIKE '%brand_match%') as brand_match_signals,
  COUNTIF(signals LIKE '%suspicious_domain%') as suspicious_domain_signals
FROM
  `your-project-id.your_dataset_id.merchant_risk_data`
GROUP BY
  is_legit;