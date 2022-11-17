# Árboles de decisión

## 1\. Implementar un árbol de decisión y comprobar su funcionamiento

Se implementó el algoritmo pedido en Python, de acuerdo al pseudo-código provisto. Se ajustó en base al dataset `tennis.csv` y posteriormente se le solicitó que predijera la clase para los mismos datos.

El árbol de decisión obtenido es el siguiente:

<img src="./attachments/tree.svg">

La matriz de confusión fue la siguiente:

```
Confusion Matrix and Statistics

          Reference
Prediction FALSE TRUE
     FALSE     5    0
     TRUE      0    9
                                     
               Accuracy : 1          
                 95% CI : (0.7684, 1)
    No Information Rate : 0.6429     
    P-Value [Acc > NIR] : 0.002059   
                                     
                  Kappa : 1          
                                     
 Mcnemar's Test P-Value : NA         
                                     
            Sensitivity : 1.0000     
            Specificity : 1.0000     
         Pos Pred Value : 1.0000     
         Neg Pred Value : 1.0000     
             Prevalence : 0.6429     
         Detection Rate : 0.6429     
   Detection Prevalence : 0.6429     
      Balanced Accuracy : 1.0000     
                                     
       'Positive' Class : TRUE
```

## 2\. Estrategias de los árboles de decisión para datos de tipo real

To be continued...