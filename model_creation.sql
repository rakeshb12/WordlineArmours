-- Create the model
CREATE OR REPLACE MODEL `brand-risk-engine-471909.brand_risk_worldline.merchant_risk_model`
OPTIONS(
  MODEL_TYPE='BOOSTED_TREE_CLASSIFIER', -- Use BOOSTED_TREE_REGRESSOR for regression tasks
  INPUT_LABEL_COLS=['is_legit']      -- Your target variable
  -- AUTO_CLASS = TRUE                  -- Automatically determine if classes are balanced enough
  -- Optional: Adjust these parameters for performance/accuracy
  -- MAX_TREE_DEPTH = 8,
  -- MIN_TREE_DEPTH = 3,
  -- NUM_PARALLEL_TREE = 2,
  -- SUBSAMPLE = 0.8,
  -- LEARNING_RATE = 0.1,
  -- NUM_TREES = 100,
  -- EARLY_STOP = TRUE,
  -- EARLY_STOP_MONITOR = 'roc_auc', -- Or 'accuracy', 'precision', 'recall'
  -- EARLY_STOP_PATIENCE = 10,
  -- Enable this for data splitting directly in training if you haven't done it manually
  -- TEST_SIZE = 0.2, -- For 20% test set
  -- DATA_SPLIT_METHOD = 'AUTO_SPLIT' -- Or 'RANDOM'
) AS
SELECT
  -- Select all features EXCEPT the split indicator and original target if splitting manually
  -- If using AUTO_SPLIT, you'd select all features including the target.
  -- For this example, we assume we'll manually select train data below.
  * EXCEPT (split_rand) -- Exclude original target and split indicator for training features
FROM
  `brand-risk-engine-471909.brand_risk_worldline.merchant_risk_split`
WHERE
  split_rand < 0.8; -- Select 80% for training

-- Note: If you used AUTO_SPLIT, you'd use the entire table here.
-- The query above assumes manual splitting where we select training data.
-- We'll need to adjust the model training if we want to use AUTO_SPLIT.