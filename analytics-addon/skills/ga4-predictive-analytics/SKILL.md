---
name: ga4-predictive-analytics
description: "Use when leveraging GA4 predictive metrics — purchase probability, churn prediction, revenue prediction. Requires 1000+ users."
category: analyst
tags: [ga4, predictive, ml, prediction, analytics, audience]
---

# GA4 Predictive Analytics (Research-Based)

## Requirements
- **Minimum**: 1000 positive samples in 7 days
- **Recommended**: 1000+ monthly users per metric
- **Timeframe**: GA4 needs 28 days of data

## Predictive Metrics

### Purchase Probability
**Definition**: Likelihood user will purchase in next 7 days
**Use Case**: Target high-probability users with offers
**Minimum**: 1000 purchases in 7 days

### Churn Probability
**Definition**: Likelihood user will not return in 7 days
**Use Case**: Re-engage at-risk users with content
**Minimum**: 1000 users who haven't churned

### Revenue Prediction
**Definition**: Expected revenue in next 28 days
**Use Case**: Forecast revenue, prioritize high-value users
**Minimum**: 1000 purchases in 7 days

## Implementation

### Step 1: Verify Eligibility
1. GA4 > Admin > Predictive Audiences
2. Check: "Eligible" status for each metric
3. If not eligible: need more user data

### Step 2: Create Predictive Audiences
1. GA4 > Audiences > New Audience
2. Select predictive metric
3. Set threshold (e.g., "Purchase probability > 70%")
4. Save and publish

### Step 3: Use Predictions
- **High purchase probability**: targeted offers
- **High churn probability**: re-engagement campaigns
- **High revenue forecast**: prioritize support

## Use Cases for Blogs

### Content Optimization
- **High churn users**: send newsletter with best content
- **High engagement**: offer premium content
- **New users with high probability**: welcome sequence

### Monetization
- **High purchase probability**: show relevant ads
- **High revenue users**: priority support
- **Low engagement**: content improvement signals

## Limitations
- Requires 1000+ users (not suitable for small blogs)
- Predictions are probabilistic, not certain
- Privacy restrictions may limit accuracy
- Only for web + app properties

## Pitfalls
1. Don't use predictions without validation
2. Don't treat predictions as guarantees
3. Don't ignore privacy regulations
4. Don't create audiences without enough data
5. Don't forget to retrain models periodically

## Verification
- Predictive audiences eligible
- Audiences created and published
- Predictions used in content strategy
- Results tracked and validated
