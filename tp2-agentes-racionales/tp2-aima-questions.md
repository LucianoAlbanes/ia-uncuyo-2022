Respuestas a las preguntas 2.10 y 2.11
===

## 2.10
a. No, porque podría tomar la decisión de volver a un slot previamente visitado, lo que implica que se encuentra limpio, siendo penalizado.

b. Si, porque de esta forma, el agente evitaría explorar los slots ya visitados, y por ende, limpios.

c. En este caso, ambos agentes buscarían el camino con mayor cantidad de suciedad por slots recorridos ( $\frac{dirtySlots}{pathLength}$ ), maximizando así la medida de performance. Como ambos tienen acceso al estado del entorno en todo momento, los estados que genera el agente con estados pierden valor.

## 2.11
a. Si, como no es penalizado por volver a slots ya visitados, esto no alteraría su medida de performance. Claro está que no seria tan eficiente como un agente con estados.

b. No, ya que este agente aspiraría en slots donde no es necesario, obteniendo así al final de su vida una menor medida de performance que el agente no aleatorio, ya que disminuyó su eficiencia.

c. Se puede observar que la medida de rendimiento del agente aleatorio se ve perjudicada a medida que el tamaño del entorno crece. (lineplot @ tp2-results.md)

d. Si, un agente con estados guardaría información sobre los slots ya visitados y los obstáculos del entorno. Con esta información, evitaría tales slots y obtendría una mayor medida de performance.
