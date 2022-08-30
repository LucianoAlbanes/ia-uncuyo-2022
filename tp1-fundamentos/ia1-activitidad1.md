IA1 - Fundamentos
===
## 1. Buscar 2 ejemplos de aplicaciones de inteligencia artificial.
### Detección de ataques DOS / DDOS 
El objetivo principal de los ataques de Denegación de Servicio (DOS) es crear un tráfico maligno mediante el uso de distintos tipos de paquetes de red que logran privar del acceso a usuarios legítimos de un servicio/servidor web. 

Este tipo de ataques se puede llevar a cabo de forma distribuida (DDOS), de forma que múltiples dispositivos bajo el control del atacante generan el tráfico malicioso.
Los paquetes enviados en un ataque DDOS, por su naturaleza, no son fáciles de distinguir respecto al tráfico legítimo. Por lo tanto, es necesario desarrollar software capaz de distinguir entre el trafico legítimo y malicioso, de forma rápida y efectiva.

![DDOS Diagram](https://blog.cloudflare.com/content/images/2022/04/unnamed1.png)

Para este problema, se utilizan actualmente algoritmos de inteligencia artificial, que son desarrollados y entrenados mediante muestras de ataques previos, en donde se extraen los patrones significativos de paquetes maliciosos para luego ser contrastados en un trafico real y detectar posibles ataques.

El verdadero reto a día de hoy son los ataques zero-day, que no son detectados por los algoritmos tradicionales que se basan en ataques ya conocidos. En estos casos resultan muy efectivos los algoritmos de deep learning usando ANNs (redes neuronales artificiales).

> Veranyurt, Ozan. (2019). Usage of Artificial Intelligence in DOS/DDOS Attack Detection. 8(1):. 23-36. 

### Separación de pistas de audio
En el mundo de la música, existen escenarios donde es útil tener los distintos elementos de una canción (voces, instrumentos, guitarra, batería, etc) de forma separada. Esto le puede servir, por ejemplo, a un DJ para lograr mejores mezclas, mejorar softwares de transcripción, o a un grupo de amigos en una noche de Karaoke.

El problema, es que los archivos de música contienen todos los elementos en una sola pista de audio y es necesario realizar la separación de las mismas.

![Spleeter](https://miro.medium.com/max/700/1*j1WakLQXuQkJCXlRk0xt5g.jpeg)

Si bien ya se encontraban disponibles algunas soluciones para esta problemática hace varios años, el resultado no era el mejor. Tras realizar la separación, se podían oír ruidos y distorsiones (artefactos) causadas por los limitados algoritmos para realizar la tarea.

![Realtek Karaoke](./images/realtekKaraoke.png)

Recientemente, ~~como a todo en este mundo~~, se comenzaron a desarrollar algoritmos basados en inteligencia artificial (machine learning) para poder llevar a cabo esta tarea obteniendo mejores resultados.

Si bien existen en el mercado muchas ofertas para realizar esta tarea, también hay disponibles de código abierto, como por ejemplo [Spleeter](https://github.com/deezer/spleeter), desarrollada por el servicio de streaming de música [Deezer](https://www.deezer.com/). Este software tiene disponible modelos para separar archivos de música en 2, 4 y 5 pistas, realiza la tarea en muy buenos tiempos (con posibilidad de ser acelerado en GPU), y se puede utilizar de formas muy sencillas (como una biblioteca de python, o desde un comando en docker).

## 2. ¿Qué se entiende por inteligencia artificial?
Inteligencia artificial (IA) se refiere a sistemas o máquinas que imitan (o intentan imitar) la inteligencia humana para realizar tareas y pueden mejorar iterativamente a partir de la información que recopilan.

Esta sintetiza y automatiza tareas que en principio son intelectuales y es, por lo tanto, potencialmente relevante para cualquier ámbito de la actividad intelectual humana (Lingüística computacional, Minería de datos (Data Mining), Medicina, Procesamiento de lenguaje natural, Robótica, Simulación de multitudes, Sistemas Operativos, Automoción, etc)

## 3. ¿Qué se entiende por inteligencia?
La inteligencia se ha definido de muchas maneras, incluyendo: la capacidad de lógica, comprensión, autoconciencia, aprendizaje, conocimiento emocional, razonamiento, planificación, creatividad, pensamiento crítico y resolución de problemas. 

En términos más generales, se puede describir como la **capacidad de percibir o inferir información, y retenerla como conocimiento** para aplicarlo a comportamientos adaptativos dentro de un entorno o contexto.

La inteligencia se estudia más a menudo en los seres humanos, pero también se ha observado en animales no humanos, en plantas (_controversial_), y a la inteligencia en los ordenadores u otras máquinas se denomina **inteligencia artificial.**

## 4. ¿Qué se entiende por artificial?
La artificialidad (el estado de ser artificial o hecho por el hombre) es el estado de ser el **producto de la fabricación humana intencional**, en lugar de ocurrir naturalmente a través de procesos que no implican o requieren la actividad humana.
