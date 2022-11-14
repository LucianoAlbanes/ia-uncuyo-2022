# Implementaciones
## Función `create_folds()`
```R:
create_folds <- function(df, k) {
  # Info: Will not shuffle df, do it before.
  
  # Prepare
  indexes <- df$id
  fold_size <- ceiling(length(indexes)/k)
  folds_n <- ceiling(length(indexes)/fold_size)
  folds <- list()
  
  # Make folds
  for (i in seq(folds_n)) {
    name <- paste0('Fold', i) 
    folds[name] <- list(indexes[(1 + fold_size * (i-1)) : (fold_size*i)])
  }
  
  # Return folds
  folds
}
```

## Función `cross_validation()`
```R:
cross_validation <- function(df, k_folds) {
  # Prepare
  folds <- create_folds(df, k_folds)
  train_formula <- formula(inclinacion_peligrosa~altura+
                                                 circ_tronco_cm+
                                                 lat+
                                                 long+
                                                 seccion+
                                                 especie)
  # Results
  results <- tibble(
              accuracy = double(),
              precision = double(),
              sensitivity = double(),
              specificity = double())
  
  # Make RPart with each fold and save results
  for (i in seq(length(folds))) {
    # Get dataframes
    fold <- folds[[i]]
    validation <- subset(df, id %in% fold)
    train <- subset(df, !(id %in% fold))
    
    # Train model
    model <- rpart(train_formula, train)
    
    # Get predictions
    predicted <- predict(model, validation, type='class')
    
    # Calc confusion matrix and save required values
    cMatrix <- confusionMatrix(data=predicted,
                               reference=validation$inclinacion_peligrosa,
                               positive = '1')
    # Save results
    results <- results |> add_row(
      accuracy = cMatrix$overall[["Accuracy"]],
      precision = cMatrix$byClass[["Precision"]],
      sensitivity = cMatrix$byClass[["Sensitivity"]],
      specificity = cMatrix$byClass[["Specificity"]])
  }
  
  # Return averages and deviations
  t(sapply(split.default(results, names(results)), function(x)  {
    x1 <- unlist(x)
    data.frame(mean = mean(x1, na.rm = TRUE), sd = sd(x1, na.rm = TRUE))}))
}
```

# Tabla de resultados estadísticos

| Metric      | Mean      | Std         |
|-------------|-----------|-------------|
| Accuracy    | 0.692443  | 0.004852079 |
| Precision   | 0.7175119 | 0.01072502  |
| Sensitivity | 0.6422259 | 0.006676295 |
| Specificity | 0.7434172 | 0.01255439  |
