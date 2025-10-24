// player.js

// Declara swup en el ámbito global o accesible para otros scripts si es necesario
let swup;

document.addEventListener('DOMContentLoaded', () => {
    const radioPlayer = document.getElementById('radio-player');
    const playPauseButton = document.getElementById('play-pause-button');
    const playIcon = document.getElementById('play-icon');
    const pauseIcon = document.getElementById('pause-icon');

    // Inicializar Swup aquí, después de que swup.min.js se haya cargado
    // Y hacer que la instancia sea global para que otros scripts (como este) puedan usarla.
    if (typeof Swup !== 'undefined' && !window.swup) {
        window.swup = new Swup(); // Asigna la instancia a window.swup
        swup = window.swup; // También a la variable local para facilidad
    } else if (typeof Swup !== 'undefined' && window.swup) {
        swup = window.swup; // Si ya está inicializado globalmente, usa esa instancia
    }


    // Función para manejar el estado del reproductor
    function togglePlayPause() {
        if (radioPlayer.paused) {
            radioPlayer.play().catch(error => {
                console.error("Error al intentar reproducir el audio:", error);
                // Aquí podrías mostrar un mensaje al usuario si la reproducción falla (e.g., autoplay block)
            });
            playIcon.classList.add('hidden');
            pauseIcon.classList.remove('hidden');
        } else {
            radioPlayer.pause();
            playIcon.classList.remove('hidden');
            pauseIcon.classList.add('hidden');
        }
    }

    // Escuchar clics en el botón de play/pause
    if (playPauseButton) {
        playPauseButton.addEventListener('click', togglePlayPause);
    }

    // Manejar el estado del reproductor después de transiciones de Swup.js
    // Asegúrate de que swup esté disponible globalmente
    if (window.swup) {
        window.swup.on('contentReplaced', () => {
            // El header con el reproductor no se reemplaza, por lo que los listeners permanecen.
            // Esta parte es más para otros scripts que sí interactúen con el contenido dinámico.
        });
    }

    // Mantener el estado de play/pause en el almacenamiento local para persistencia
    radioPlayer.addEventListener('play', () => {
        localStorage.setItem('radioPlayerState', 'playing');
    });

    radioPlayer.addEventListener('pause', () => {
        localStorage.setItem('radioPlayerState', 'paused');
    });

    // Restaurar el estado al cargar la página
    const savedState = localStorage.getItem('radioPlayerState');
    if (savedState === 'playing') {
        radioPlayer.muted = true; // Intentar mutear para evitar bloqueos de autoplay, luego desmutear si el usuario interactúa
        radioPlayer.play().then(() => {
            radioPlayer.muted = false;
            playIcon.classList.add('hidden');
            pauseIcon.classList.remove('hidden');
        }).catch(error => {
            console.warn("Autoplay bloqueado o error al reanudar la reproducción:", error);
            playIcon.classList.remove('hidden');
            pauseIcon.classList.add('hidden');
        });
    } else {
        playIcon.classList.remove('hidden');
        pauseIcon.classList.add('hidden');
    }
});
