El usuario controla una nave espacial que debe disparar y esquivar balas enemigas. El objetivo principal es destruir enemigos para ganar puntos y sobrevivir el mayor tiempo posible.

## 🎮 **Características del juego**
- Animaciones de explosiones
- Disparos del jugador y enemigos
- Sistema de puntuación
- Barra de vida dinámica
- Sonidos de disparo y explosiones
- Curación automática cada ciertos puntos
- Pantallas de inicio e instrucciones

## 👤 **Integrantes del grupo**
- Carolina Cottini
- Julio Fernández Martínez
- Lucas Rimbano
- Nahuel Galeano
- Pedro Mendy

## ⚙️ **Instrucciones de Uso**
1. Asegurate de tener *Python 3.8+* instalado.
2. Instala la librería *Pygame* si no la tenés:

   ```bash
   pip install pygame
   
## 🕹️ **Instrucciones de uso del juego**
- Mover la nave:
- Flechas ← →
- o teclas A / D (según elección inicial)
- Disparar: ESPACIO
- Reiniciar partida: R
- Salir: ESC

## ⚙️ **Funcionalidades implementadas**
- Actualización de enemigos, balas y puntuación: mediante bucles for
- Animaciones y enemigos múltiples: con ciclos range
- Posiciones y colores: definidos con tuplas
- Clases independientes para cada entidad: jugador, enemigo, balas, explosiones
- Funciones específicas para: puntuación, barra de vida, pantalla GAME OVER y menú principal
- Decorador personalizado para medir el tiempo de ejecución de funciones
- Conjuntos (set) para asegurar que solo un enemigo dispare a la vez
- Carga de archivos externos (imágenes y sonidos)
- Manejo de excepciones para errores durante la carga de archivos
