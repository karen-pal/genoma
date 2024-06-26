Genoma, por Karen Palacio.

# Descripción
Primero leo el contenido de la muestra más actualizada de genoma humano hasta la fecha (Homo_sapiens.GRCh38.85).

Extraigo de toda esa información los genes clasificados/nombrados.

Con eso creo un dataset de esta pinta:
```python
              seqid          source  type  start    end score strand phase   gene_name          gene_id                                               desc
2512305  KI270721.1         ensembl  gene   2585  11802     .      +     .  AC004556.1  ENSG00000276345                                                   
2511636  KI270711.1         ensembl  gene   4612  29626     .      -     .  AC240274.1  ENSG00000271254                                                   
2513047  KI270731.1         ensembl  gene  10598  13001     .      -     .  AC023491.2  ENSG00000278633                                                   
865056           16          havana  gene  11555  14090     .      +     .    DDX11L10  ENSG00000233614  DEAD/H-box helicase 11 like 10 [Source:HGNC Sy...
16                1          havana  gene  11869  14409     .      +     .     DDX11L1  ENSG00000223972  DEAD/H-box helicase 11 like 1 [Source:HGNC Sym...
2416567           9          havana  gene  12134  13783     .      +     .     DDX11L5  ENSG00000236875  DEAD/H-box helicase 11 like 5 [Source:HGNC Sym...
483390           12          havana  gene  12310  13501     .      +     .     DDX11L8  ENSG00000256263  DEAD/H-box helicase 11 like 8 [Source:HGNC Sym...
865067           16          havana  gene  14381  18068     .      -     .      WASH4P  ENSG00000234769  WAS protein family homolog 4 pseudogene [Sourc...
28                1          havana  gene  14404  29570     .      -     .      WASH7P  ENSG00000227232  WAS protein family homolog 7 pseudogene [Sourc...
2416575           9  ensembl_havana  gene  14521  29739     .      -     .       WASH1  ENSG00000181404  WAS protein family homolog 1 [Source:HGNC Symb...

```

De estos datos me interesó el start y end de cada gen. Hay un mar de información a adquirir si une quiere empezar a sacar hipótesis semánticas sobre el contenido del genoma - pero una hipótesis interesante es que la locación de un gen contiene información localizada , codificando geométricamente información de relación entre genes y funciones de genes.

> Genomic Location: Genes located close to each other on the same chromosome (syntenic genes) may be functionally related or co-regulated. Analyzing genomic coordinates (start and end positions) can reveal clustering or co-localization of genes.

Me interesó encontrar o ver sobreposiciones en estas localizaciones 

> Genomic Context: Plot the genomic locations of the genes to identify clusters or overlaps.

Para esto representé el contenido del dataset en un árbol de intervalos - debido a que una implementación naive sería no-apta para algo que suceda en el marco de tiempo de la muestra para la cual fue construido este sistema.

> A menudo se utiliza para las consultas de ventanas, por ejemplo, para encontrar todos los caminos en un mapa computarizado dentro de una ventana rectangular, o para encontrar todos los elementos visibles dentro de una escena tridimensional.

<img src="./Figure_first_100.png"/>

Luego usando python se grafica en tiempo real recorriendo los datos del genoma ordenados por localización con una velocidad parametrizada y controlable.

Además en una ventana se van imprimiendo las descripciones de estos genes.

Este sistema busca reemplazar un algoritmo de randomización de un sistema más grande que implementa cadenas de markov para controlar luces y sonido. Por lo tanto finalmente lo que se manda es el último dígito del dato end actual usando OSC, para que sea interpretado por ese otro sistema que está implementado en Pure Data por Valentin 

# Contexto de construcción
Instalación multimedia

Quimera. Pensar con luz, sonido y algoritmos

28 de junio | 18:30 a 21 h.
Sala Jorge Díaz · CePIA

En la mitología griega, una Quimera [Χίμαιρα] es una criatura viviente híbrida, un ser compuesto de varios seres. Recuperamos esta alegoría para explorar el esfuerzo y la riqueza que implican congeniar historias y personalidades distintas en un mismo proceso creativo. 

Esta instalación multimedial teje un tapiz sensorial que se despliega como una especie de Quimera: un sistema autónomo que cobra vida en espacios escénicos mediante diversos procesos lumínicos, visuales y sonoros manipulados a través de código generativo de programación basado en modelos matemáticos de Márkov.

Cada luz, cada sonido y cada imagen se entrelazan como partes de un todo orgánico, reflejando la armonía y el caos del azar y de la creación colectiva. La Quimera se vuelve una metáfora del mismo proceso: una entidad que nace de la fusión de diferentes elementos, rica en diversidad y complejidad. Una experiencia híbrida a la cual te invitamos a sumergirte.

+info >> https://cepia.artes.unc.edu.ar/2024/06/06/instalacion-multimedia-quimera-pensar-con-luz-sonido-y-algoritmos/

# Running

## Preprocess
### Get original dataset

`wget ftp://ftp.ensembl.org/pub/release-85/gff3/homo_sapiens/Homo_sapiens.GRCh38.85.gff3.gz`

Read more about it here: https://www.toptal.com/python/comprehensive-introduction-your-genome-scipy

### Get intermediate files
`python3 build_datasets.py`

> This generates the dataset gene_data.pkl

`python3 get_nodes_edges_of_genes.py`

> this generates node_data.json and edge_data.json. They are not ultimetaly used since I haven't still found a way to render them properly using react flow.

## run simulation
`python3 gen.py`



# Mandar OSC
- Conectar mi compu al router.
- deshabilitar la seguridad en http://tplinklogin.net/
- Conectar la compu de Laura por wifi al router.
- preguntar por el IP de laura,en una terminal con ifconfig | grep inet (debería empezar en 192)
- mandar a ese IP.

