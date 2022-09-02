Respuestas a las preguntas 2.10 y 2.11 (AIMA)
===

## 2.10:
**Considere una versión modificada del Ejercicio 2.8 en la que el agente aspiradora es penalizado con un punto por cada movimiento.**

a. **¿Puede un agente de reflejo simple ser perfectamente racional para este entorno? Justifique**. No, porque podría tomar la decisión de volver a un slot previamente visitado, lo que implica que se encuentra limpio, siendo penalizado.

b. **¿Qué tal un agente de reflejo con estado?** Si, porque de esta forma, el agente evitaría explorar los slots ya visitados, y por ende, limpios.

c. **¿Cómo cambiarían las respuestas anteriores si las percepciones del agente le dan el estado de limpieza/suciedad de cada slot del entorno?** En este caso, ambos agentes buscarían el camino con mayor cantidad de suciedad por slots recorridos ( $\frac{dirtySlots}{pathLength}$ ), maximizando así la medida de performance. Como ambos tienen acceso al estado del entorno en todo momento, los estados que genera el agente con estados pierden valor.

## 2.11
**Considere una versión modificada del Ejercicio 2.8, en la que la
geografía del entorno -su extensión, límites y obstáculos- es desconocida, al igual que la configuración inicial de la suciedad.**

a. **¿Puede un agente de reflejo simple ser perfectamente racional para este entorno? Explique** Si, como no es penalizado por volver a slots ya visitados, esto no alteraría su medida de performance. Claro está que no seria tan eficiente como un agente con estados.

b. **¿Puede un agente de reflejo simple con una función de agente aleatoria superar a un agente de reflejo simple?** No, ya que este agente aspiraría en slots donde no es necesario, obteniendo así al final de su vida una menor medida de performance que el agente no aleatorio, ya que disminuyó su eficiencia.

c. **¿Puede diseñar un entorno en el que su agente aleatorio tenga un mal rendimiento?** Se puede observar que la medida de rendimiento del agente aleatorio se ve perjudicada a medida que el tamaño del entorno crece, respecto del agente de reflejo simple. (lineplot @ tp2-results.md)

d. **¿Puede un agente de reflejo con estado superar a un agente reflejo simple?** Si. Un agente con estados guardaría información sobre los slots ya visitados y los obstáculos del entorno. Con esta información, evitaría tales slots y obtendría una mayor medida de performance.
