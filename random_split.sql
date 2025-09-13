-- Create a table with a random split indicator
CREATE OR REPLACE TABLE `brand-risk-engine-471909.brand_risk_worldline.merchant_risk_split` AS
SELECT
  *,
  RAND() AS split_rand
FROM
  `brand-risk-engine-471909.brand_risk_worldline.merchant_risk_features`;

-- Define training and testing datasets (e.g., 80% train, 20% test)
-- (We'll use this split logic when creating the model for evaluation)