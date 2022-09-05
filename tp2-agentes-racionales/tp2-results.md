Resultados Agente de Reflejo Simple vs Agente Totalmente aleatorio
===
Se realizaron simulaciones con Agentes de Reflejo Simple (_SimpleReflexAgent_) y Agentes totalmente aleatorios (_DumbAgent_). Las configuraciones utilizadas son las siguientes:
- _tamaño_: 2x2, 4x4, 8x8, 16x16, 32x32, 64x64, 128x128
- _ratio de suciedad_: 0.1, 0,2 0,4, 0.8
- _movimientos disponibles:_ 1000
- _iteraciones por configuración_: 30

La medida de rendimiento es la cantidad de slots limpiados.

> Los archivos *.csv* correspondientes a las tablas se encuentran en la carpeta *attachments*. Además, en la carpeta *code*, se encuentra un Jupyter Notebook para llevar a cabo esta misma simulación, con la posibilidad de alterar la configuración anterior.

# Análisis por categoría
|agent_type       |size|dirt_rate|cleaned_slots_avg|cleaned_slots_std|remaining_life_avg|remaining_life_std|
|-----------------|----|---------|-----------------|-----------------|------------------|------------------|
|SimpleReflexAgent|2   |0,1      |0,63             |0,85             |997,80            |3,62              |
|SimpleReflexAgent|2   |0,2      |0,73             |0,78             |997,53            |3,42              |
|SimpleReflexAgent|2   |0,4      |1,70             |0,79             |992,60            |4,90              |
|SimpleReflexAgent|2   |0,8      |3,03             |0,89             |991,03            |5,08              |
|SimpleReflexAgent|4   |0,1      |1,70             |1,24             |959,57            |47,96             |
|SimpleReflexAgent|4   |0,2      |2,90             |1,60             |952,37            |30,14             |
|SimpleReflexAgent|4   |0,4      |6,33             |1,92             |916,10            |49,76             |
|SimpleReflexAgent|4   |0,8      |12,80            |1,27             |895,10            |43,00             |
|SimpleReflexAgent|8   |0,1      |7,37             |2,71             |616,23            |217,69            |
|SimpleReflexAgent|8   |0,2      |12,23            |2,80             |450,33            |270,01            |
|SimpleReflexAgent|8   |0,4      |25,37            |4,21             |338,90            |249,25            |
|SimpleReflexAgent|8   |0,8      |51,23            |3,67             |265,30            |256,61            |
|SimpleReflexAgent|16  |0,1      |19,00            |4,66             |1,60              |8,76              |
|SimpleReflexAgent|16  |0,2      |37,70            |6,25             |0,00              |0,00              |
|SimpleReflexAgent|16  |0,4      |75,17            |9,81             |0,00              |0,00              |
|SimpleReflexAgent|16  |0,8      |142,67           |21,74            |0,00              |0,00              |
|SimpleReflexAgent|32  |0,1      |29,80            |6,62             |0,00              |0,00              |
|SimpleReflexAgent|32  |0,2      |58,63            |11,89            |0,00              |0,00              |
|SimpleReflexAgent|32  |0,4      |109,07           |19,85            |0,00              |0,00              |
|SimpleReflexAgent|32  |0,8      |193,93           |29,79            |0,00              |0,00              |
|SimpleReflexAgent|64  |0,1      |32,90            |8,61             |0,00              |0,00              |
|SimpleReflexAgent|64  |0,2      |63,37            |10,86            |0,00              |0,00              |
|SimpleReflexAgent|64  |0,4      |115,93           |21,84            |0,00              |0,00              |
|SimpleReflexAgent|64  |0,8      |214,73           |25,07            |0,00              |0,00              |
|SimpleReflexAgent|128 |0,1      |33,93            |6,67             |0,00              |0,00              |
|SimpleReflexAgent|128 |0,2      |67,20            |13,02            |0,00              |0,00              |
|SimpleReflexAgent|128 |0,4      |126,87           |18,14            |0,00              |0,00              |
|SimpleReflexAgent|128 |0,8      |218,43           |28,88            |0,00              |0,00              |
|DumbAgent        |2   |0,1      |0,40             |0,50             |994,97            |10,52             |
|DumbAgent        |2   |0,2      |0,63             |0,61             |982,07            |27,56             |
|DumbAgent        |2   |0,4      |1,43             |0,97             |970,60            |43,29             |
|DumbAgent        |2   |0,8      |3,07             |0,98             |948,07            |44,02             |
|DumbAgent        |4   |0,1      |1,57             |0,94             |798,47            |231,63            |
|DumbAgent        |4   |0,2      |2,90             |1,42             |769,90            |219,83            |
|DumbAgent        |4   |0,4      |6,90             |1,71             |690,57            |213,58            |
|DumbAgent        |4   |0,8      |12,53            |1,41             |560,70            |203,12            |
|DumbAgent        |8   |0,1      |5,70             |2,12             |28,40             |116,44            |
|DumbAgent        |8   |0,2      |10,50            |2,61             |14,27             |53,69             |
|DumbAgent        |8   |0,4      |23,00            |3,91             |0,00              |0,00              |
|DumbAgent        |8   |0,8      |42,63            |3,55             |0,00              |0,00              |
|DumbAgent        |16  |0,1      |10,23            |3,81             |0,00              |0,00              |
|DumbAgent        |16  |0,2      |17,37            |3,94             |0,00              |0,00              |
|DumbAgent        |16  |0,4      |38,57            |5,23             |0,00              |0,00              |
|DumbAgent        |16  |0,8      |74,20            |8,88             |0,00              |0,00              |
|DumbAgent        |32  |0,1      |11,27            |3,60             |0,00              |0,00              |
|DumbAgent        |32  |0,2      |22,00            |4,09             |0,00              |0,00              |
|DumbAgent        |32  |0,4      |46,00            |6,57             |0,00              |0,00              |
|DumbAgent        |32  |0,8      |88,00            |9,54             |0,00              |0,00              |
|DumbAgent        |64  |0,1      |11,30            |2,69             |0,00              |0,00              |
|DumbAgent        |64  |0,2      |23,10            |4,87             |0,00              |0,00              |
|DumbAgent        |64  |0,4      |45,37            |5,79             |0,00              |0,00              |
|DumbAgent        |64  |0,8      |94,00            |11,94            |0,00              |0,00              |
|DumbAgent        |128 |0,1      |12,77            |3,34             |0,00              |0,00              |
|DumbAgent        |128 |0,2      |23,07            |4,41             |0,00              |0,00              |
|DumbAgent        |128 |0,4      |46,80            |6,06             |0,00              |0,00              |
|DumbAgent        |128 |0,8      |93,63            |8,94             |0,00              |0,00              |


# Gráficos
## Boxplot
En el siguiente gráfico se observa el comportamiento de cada agente para cada una de las posibles combinaciones de *tamaño* y *ratio de suciedad*. La variable evaluada es la medida de rendimiento (*cleaned_slots)*.
<img src="./attachments/boxplot.svg">

# Lineplot
En este gráfico, se analiza como evoluciona para cada agente el *cleaned_slots* a medida que aumenta el tamaño de la grilla. Un gráfico por *ratio de suciedad*.
<img src="./attachments/lineplot.svg">
