# 🧩 Proyecto PCB - Diseño y Fabricación

Este documento explica el proceso de diseño y fabricación de una **placa de circuito impreso (PCB)** realizada manualmente, desde el diseño esquemático hasta el montaje final. El objetivo fue crear una placa funcional a partir de un circuito previamente diseñado en software de simulación electrónica.

---

## 🧰 Herramientas y materiales utilizados

- Software: [KiCad](https://kicad.org/) (también se puede usar Proteus, EasyEDA, etc.)
- Impresora láser
- Papel transfer
- Placa virgen de cobre
- Alcohol isopropílico
- Plancha o laminadora
- Ácido férrico
- Micrómetro digital o manual
- Taladro para PCB
- Estaño y soldador
- Componentes electrónicos (resistencias, capacitores, Arduino, etc.)

---

## 📝 Pasos realizados

### 1. Diseño del esquema eléctrico
Se utilizó **KiCad** para crear el esquema del circuito, seleccionando y conectando los componentes electrónicos de acuerdo a la lógica del sistema a implementar.

### 2. Asignación de huellas (footprints)
A cada componente del esquema se le asignó una **huella física**, que representa su forma y tamaño en la placa.  
En caso de no conocerla, se midió con un **micrómetro** para determinar dimensiones aproximadas (ej. 4 mm).  
Para el Arduino y otros módulos comunes, se usaron las huellas disponibles por defecto.

### 3. Diseño del PCB
Con las huellas asignadas, se enrutaron las pistas para unir los componentes y se organizó el diseño del PCB, cuidando el orden y evitando cruces de pistas innecesarios.

### 4. Impresión del diseño
El diseño del PCB se imprimió en **papel transfer** utilizando una **impresora láser**, en modo espejo (espejado) para que coincida al colocarlo sobre la placa.

### 5. Preparación de la placa
Se limpió la **placa virgen de cobre** con **alcohol isopropílico** para eliminar grasa o impurezas que pudieran impedir una buena transferencia.

### 6. Transferencia del diseño a la placa
Se colocó el papel transfer (con el diseño) sobre la parte de cobre de la placa.  
Se aplicó calor con una **plancha casera durante 10 minutos** para que el tóner se adhiera al cobre.

### 7. Ataque químico con ácido férrico
Se sumergió la placa en **ácido férrico** y se removió hasta que se eliminaron las partes de cobre no protegidas por el tóner.

### 8. Perforado
Una vez revelada, se perforaron los orificios necesarios con un **taladro manual o de banco**, para permitir la inserción de los componentes.

### 9. Montaje y soldadura
Finalmente, se colocaron los componentes sobre la placa y se procedió a **soldar cada uno cuidadosamente**, verificando continuidad con multímetro.

---

## ✅ Resultado final

La PCB resultante es completamente funcional y fue construida de forma artesanal, aplicando conocimientos de diseño electrónico y técnicas de fabricación casera. Esta metodología permite crear prototipos confiables sin necesidad de mandar a fabricar placas industrialmente.

---

## 🧠 Notas finales

- Se recomienda realizar pruebas del circuito en protoboard antes de fabricar la placa.
- Utilizar guantes y protección adecuada al manipular ácido férrico.
- Para diseños más complejos, se puede optar por servicios de fabricación como JLCPCB o PCBWay.

