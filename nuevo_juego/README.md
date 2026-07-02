El usuario controla una nave espacial que debe disparar y esquivar balas enemigas. El objetivo principal es destruir enemigos para ganar puntos y sobrevivir el mayor tiempo posible.

## 🎮 **Características del juego**
- Animaciones de explosiones
- Disparos del jugador y enemigos
- Sistema de puntuación
- Barra de vida dinámica
- Sonidos de disparo y explosiones
- Curación automática cada ciertos puntos
- Pantallas de inicio e instrucciones

[![Ver video](https://img.youtube.com/vi/SF5AseoXdS8/hqdefault.jpg)](https://youtu.be/SF5AseoXdS8)


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
   ```

## 🌐 **Version web**
Este juego tambien se puede empaquetar como pagina web usando `pygbag`.

Desde la raiz del proyecto:

```bash
source .venv/bin/activate
python -m pygbag --build --disable-sound-format-error nuevo_juego
```

La carpeta que se sube a internet es:

```text
nuevo_juego/build/web/
```

Para probar la pagina final:

```bash
python -m http.server 8000 --directory nuevo_juego/build/web
```

Despues abri `http://localhost:8000`.
   
## 🕹️ **Instrucciones de uso del juego**
- Mover la nave:
- Flechas ← →
- o teclas A / D (según elección inicial)
- Disparar: ESPACIO
- Reiniciar partida: R
- Terminar partida: ESC
- La vida se restaura al llegar a 1000 puntos, y luego cada 1000 puntos más.
- Al perder o terminar con ESC, la version web pide un nombre y guarda los 5 mejores puntajes en ese navegador.

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
