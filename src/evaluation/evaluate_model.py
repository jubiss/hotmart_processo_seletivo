# Calculate permutation importance

result = permutation_importance(model, X_val, y_val, n_repeats=10, random_state=42, n_jobs=-1)

# Get feature importance scores and their corresponding indices
importance_scores = result.importances_mean
indices = np.argsort(importance_scores)

# Plot feature importance
plt.figure(figsize=(10, 6))
plt.barh(range(len(indices)), importance_scores[indices], align='center')
plt.yticks(range(len(indices)), [feature_names[i] for i in indices])
plt.xlabel('Permutation Importance')
plt.title('Feature Importance - Permutation Importance')
plt.tight_layout()
plt.show()