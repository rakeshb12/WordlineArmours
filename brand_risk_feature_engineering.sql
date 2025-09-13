CREATE OR REPLACE TABLE `brand-risk-engine-471909.brand_risk_worldline.merchant_risk_features`  AS
SELECT
  merchant_id,
  is_legit, -- Target variable

  -- Numeric features
  domain_age_days,
  brand_similarity_score,
  impersonation_risk_score,
  domain_brand_alignment_score,
  related_domains,
  CASE WHEN REGEXP_CONTAINS(signals, r'\bnew_domain\b') THEN 1 ELSE 0 END AS signal_new_domain,
  CASE WHEN REGEXP_CONTAINS(signals, r'\bimpersonation_risk\b') THEN 1 ELSE 0 END AS signal_impersonation_risk,
  CASE WHEN REGEXP_CONTAINS(signals, r'\bsanctions_match\b') THEN 1 ELSE 0 END AS signal_sanctions_match,
  CASE WHEN REGEXP_CONTAINS(signals, r'\bbrand_match\b') THEN 1 ELSE 0 END AS signal_brand_match,
  CASE WHEN REGEXP_CONTAINS(signals, r'\bsuspicious_domain\b') THEN 1 ELSE 0 END AS signal_suspicious_domain,
  CASE WHEN REGEXP_CONTAINS(signals, r'\bdomain_age_ok\b') THEN 1 ELSE 0 END AS signal_domain_age_ok,

  -- Categorical features (can be one-hot encoded later or handled by BQML model)
  kyc_verdict,
  onboarding_status,
  sanctions_flag,
  entity_type,
  country,

  -- Financial institution features (optional, might be noisy)
  -- financial_institution_name, -- May need one-hot encoding
  -- financial_institution_account_number, -- Probably too noisy or complex to use directly

  -- Text features (can be embedded by BQML or processed separately)
  notes, -- Could be used with text embedding models or for TF-IDF
  legal_name, -- Similar to notes

  -- Other potentially useful fields
  domain,
  owner_email

FROM
  `brand-risk-engine-471909.brand_risk_worldline.brand_risk_customer`
WHERE
  -- Optional: Filter out any rows with critical missing values if needed
  -- For example: AND NOT REGEXP_CONTAINS(domain, r'\.biz$') -- Exclude obvious scam domains if you want cleaner legit data
  TRUE -- Placeholder for future WHERE clauses
;