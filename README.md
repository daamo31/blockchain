# Basic Blockchain

Este proyecto es una implementación básica de una blockchain en Python, que incluye múltiples nodos y una wallet para gestionar transacciones. A continuación se detallan las características y la estructura del proyecto.

## Estructura del Proyecto

```
basic-blockchain
├── blockchain
│   ├── __init__.py
│   ├── blockchain.py
│   ├── block.py
│   ├── transaction.py
│   └── node.py
├── wallet
│   ├── __init__.py
│   ├── wallet.py
│   └── keys.py
├── nodes
│   ├── node1.py
│   ├── node2.py
│   └── node3.py
├── requirements.txt
└── README.md
```

## Descripción de Archivos

- **blockchain/**: Contiene la lógica principal de la blockchain.
  - `__init__.py`: Inicializa el paquete `blockchain`.
  - `blockchain.py`: Clase que gestiona la cadena de bloques.
  - `block.py`: Clase que representa un bloque en la cadena.
  - `transaction.py`: Clase que representa una transacción.
  - `node.py`: Clase que representa un nodo en la red.

- **wallet/**: Maneja las transacciones y claves del usuario.
  - `__init__.py`: Inicializa el paquete `wallet`.
  - `wallet.py`: Clase que gestiona las transacciones y saldo.
  - `keys.py`: Maneja la generación y almacenamiento de claves.

- **nodes/**: Contiene los scripts para inicializar los nodos de la red.
  - `node1.py`, `node2.py`, `node3.py`: Scripts para cada nodo, configurando conexiones y sincronización.

- **requirements.txt**: Lista las dependencias necesarias para el proyecto.

## Instalación

1. Clona el repositorio:
   ```
   git clone <URL_DEL_REPOSITORIO>
   cd basic-blockchain
   ```

2. Instala las dependencias:
   ```
   pip install -r requirements.txt
   ```

## Ejecución

Para iniciar los nodos, ejecuta los siguientes comandos en diferentes terminales:

```
python nodes/node1.py
python nodes/node2.py
python nodes/node3.py
```

## Contribuciones

Las contribuciones son bienvenidas. Si deseas mejorar este proyecto, por favor abre un issue o un pull request.

## Licencia

Este proyecto está bajo la Licencia MIT.