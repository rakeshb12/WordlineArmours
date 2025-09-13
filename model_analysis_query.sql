SELECT *
FROM ML.PREDICT(MODEL `brand-risk-engine-471909.brand_risk_worldline.merchant_risk_model`, (
  SELECT
     merchant_id, domain_age_days, brand_similarity_score, impersonation_risk_score, domain_brand_alignment_score, related_domains, signal_new_domain, signal_impersonation_risk, signal_sanctions_match, signal_brand_match, signal_suspicious_domain, signal_domain_age_ok, kyc_verdict, onboarding_status, sanctions_flag, entity_type, country, notes, legal_name, domain, owner_email
  FROM `brand_risk_worldline.merchant_risk_features`
));