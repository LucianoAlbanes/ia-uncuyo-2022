HAILML: Predicción de tormentas de granizo utilizando machine learning
===

# Descripción
Este proyecto busca poder predecir que tan probable es que ocurra una tormenta con precipitación de granizo en una determinada zona geográfica utilizando aprendizaje de máquinas (machine learning).

El tiempo meteorológico tiene un comportamiento caótico, por lo que las predicciones del mismo no gozan de gran precisión en el mediano y largo plazo. Por ello, el desarrollo de la solución se concentrará en el pronóstico intradiario, con posibilidad de extenderse hasta una semana por delante con la condición de que las predicciones sean útiles.

Será necesario realizar un estudio de las variables relevantes que influyen en la formación de granizo y como representarlas en el dataset. Además, habrá que recopilar los mismos de múltiples fuentes (con la esperanza de que estén disponibles).

La zona geográfica con la que se comenzará a trabajar es el Oasis Norte de la Provincia de Mendoza, Argentina; pero como aún no se sabe con certeza las variables y disponibilidad de las mismas, podría llegar a analizarse otra zona geográfica donde también ocurra este fenómeno meteorológico.

Las predicciones del modelo se evaluarán como si se tratase de un problema de clasificación (si ocurrió una tormenta con caída de granizo o no), se generarán dos dataset: uno de entrenamiento y otro de verificación, con los cuales se podrán obtener diversas métricas para evaluar los modelos.

Para implementar el modelo se utilizará el algoritmo de clasificación random forest, y de forma tentativa una implementación mediante deep learning.

# Justificación
Si bien existen y se utilizan actualmente los modelos numéricos de predicción meteorológica, estos son muy complejos y costosos computacionalmente, por lo que lograr una buena estimación mediante técnicas de machine learning sería positivo. Además, existe una esperanza de que utilizando técnicas de aprendizaje profundo (deep learning) se pueda "hallar" patrones no considerados anteriormente que permitan mejoren las predicciones.

