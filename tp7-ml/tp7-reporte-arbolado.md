## Preprocesamiento
Para el preprocesamiento del dataset se utilizaron 3 estrategias:

- Oversampling y undersampling.
- Eliminar especies de árboles con pocas apariciones.
- Agregar la elevación de cada árbol.

Tras realizar múltiples envíos a la competencia en Kaggle, en base a la puntaje AUC ROC obtenido se concluye lo siguiente:

- Es necesario realizar un balanceo en el dataset, donde la combinación de oversampling y undersampling da los mejores resultados.
- Algunas especies tienen muy pocas apariciones (p. ej. algarrobo, árbol del cielo, maitén, arabia), por lo que se definió un umbral de apariciones mínimas. Si una especie aparecía menos de $n$ veces resultaría eliminada del dataset. Los valores de $n$ más efectivos fueron $3, 4, 10$.
- Se añadió un nueva columna que contenía la elevación sobre el nivel del mar de cada árbol, con la esperanza de así obtener mas información sobre la inclinación de los mismos. Esto no resultó en una mejora significativa en los puntajes obtenidos.

## Resultados (Validación)
Este fue el conjunto de datos que se utilizó para ajustar el modelo, con el objetivo de obtener el mayor valor del AUC ROC.

A continuación se muestra la matriz de confusión con las diversas métricas obtenidas en base a una ejecución de la solución planteada. En la misma se utilizó una combinación de oversampling y undersampling para el balanceo, umbral de especies con pocas apariciones igual a $3$, y la elevación de cada árbol.

```txt:
Confusion Matrix and Statistics

          Reference
Prediction    0    1
         0 4457  300
         1 1175  451
                                          
               Accuracy : 0.7689          
                 95% CI : (0.7584, 0.7792)
    No Information Rate : 0.8823          
    P-Value [Acc > NIR] : 1               
                                          
                  Kappa : 0.2604          
                                          
 Mcnemar's Test P-Value : <2e-16          
                                          
            Sensitivity : 0.60053         
            Specificity : 0.79137         
         Pos Pred Value : 0.27737         
         Neg Pred Value : 0.93694         
             Prevalence : 0.11766         
         Detection Rate : 0.07066         
   Detection Prevalence : 0.25474         
      Balanced Accuracy : 0.69595         
                                          
       'Positive' Class : 1 
```

## Resultados (Kaggle)
A continuación se muestra una tabla con distintos envíos realizados, donde se muestra que criterios de preprocesamiento se utilizaron y que puntaje recibió:

| Umbral rareza | Método balance | Con elevación | AUC ROC |
|---------------|----------------|---------------|---------|
| 3             | Ninguno        | No            | 0.52195 |
| 3             | Combinado      | No            | 0.70766 |
| 3             | Combinado      | Si            | 0.70612 |
| 4             | Combinado      | Si            | 0.70586 |
| 10            | Combinado      | Si            | 0.70344 |
| 10            | Oversampling   | No            | 0.69545 |

## Detalles del algoritmo

- Ingresar los datasets de entrenamiento y prueba a utilizar, y el umbral de rareza.
- Asignar `inclinacion_peligrosa` como factor.
- Definir la formula de entrenamiento.
- Realizar el balanceo del dataset de entrenamiento acorde a la formula de entrenamiento si fuese necesario.
- Remover las especies que caigan dentro del umbral de rareza.
- Entrenar un modelo utilizando `randomForest`, en base al dataset de entrenamiento y la formula.
- Obtener las predicciones utilizando el modelo sobre el dataset de prueba.
- Si en dataset de prueba estaban disponibles los valores de referencia, llamar a `confusionMatrix` para evaluar las predicciones.
- Guardar conforme al formato de Kaggle la lista de predicciones.

