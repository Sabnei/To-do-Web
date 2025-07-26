// JavaScript personalizado para el Gestor de Tareas

document.addEventListener("DOMContentLoaded", function () {
  // Inicializar tooltips de Bootstrap
  var tooltipTriggerList = [].slice.call(
    document.querySelectorAll('[data-bs-toggle="tooltip"]')
  );
  var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
    return new bootstrap.Tooltip(tooltipTriggerEl);
  });

  // Efectos de animación para las cards
  const cards = document.querySelectorAll(".card");
  cards.forEach((card, index) => {
    card.style.animationDelay = `${index * 0.1}s`;
    card.classList.add("fade-in-up");
  });

  // Confirmación mejorada para eliminar tareas
  const deleteButtons = document.querySelectorAll('a[href*="eliminar"]');
  deleteButtons.forEach((button) => {
    button.addEventListener("click", function (e) {
      if (
        !confirm(
          "¿Estás seguro de que quieres eliminar esta tarea? Esta acción no se puede deshacer."
        )
      ) {
        e.preventDefault();
      }
    });
  });

  // Efectos de hover para las tareas
  const taskCards = document.querySelectorAll(".task-card");
  taskCards.forEach((card) => {
    card.addEventListener("mouseenter", function () {
      this.style.transform = "translateY(-5px)";
    });

    card.addEventListener("mouseleave", function () {
      this.style.transform = "translateY(0)";
    });
  });

  // Auto-completar para el campo de etiquetas
  const tagsInput = document.querySelector('input[name="tags"]');
  if (tagsInput) {
    const commonTags = [
      "trabajo",
      "personal",
      "urgente",
      "proyecto",
      "reunión",
      "estudio",
      "ejercicio",
      "compras",
    ];

    tagsInput.addEventListener("input", function () {
      const value = this.value.toLowerCase();
      const lastTag = value.split(",").pop().trim();

      if (lastTag.length > 0) {
        const suggestions = commonTags.filter(
          (tag) => tag.startsWith(lastTag) && !value.includes(tag)
        );

        // Aquí podrías mostrar sugerencias en un dropdown
        if (suggestions.length > 0) {
          console.log("Sugerencias:", suggestions);
        }
      }
    });
  }

  // Validación de formularios en tiempo real
  const forms = document.querySelectorAll("form");
  forms.forEach((form) => {
    const inputs = form.querySelectorAll("input, select, textarea");
    inputs.forEach((input) => {
      input.addEventListener("blur", function () {
        validateField(this);
      });

      input.addEventListener("input", function () {
        if (this.classList.contains("is-invalid")) {
          validateField(this);
        }
      });
    });
  });

  // Función de validación
  function validateField(field) {
    const value = field.value.trim();

    // Remover clases de validación previas
    field.classList.remove("is-valid", "is-invalid");

    // Validaciones específicas
    if (field.name === "descripcion") {
      if (value.length < 3) {
        field.classList.add("is-invalid");
        showFieldError(
          field,
          "La descripción debe tener al menos 3 caracteres"
        );
      } else {
        field.classList.add("is-valid");
        hideFieldError(field);
      }
    }

    if (field.name === "fecha_limite") {
      if (value) {
        const selectedDate = new Date(value);
        const today = new Date();
        today.setHours(0, 0, 0, 0);

        if (selectedDate < today) {
          field.classList.add("is-invalid");
          showFieldError(field, "La fecha límite no puede ser anterior a hoy");
        } else {
          field.classList.add("is-valid");
          hideFieldError(field);
        }
      }
    }
  }

  // Mostrar errores de campo
  function showFieldError(field, message) {
    let errorDiv = field.parentNode.querySelector(".invalid-feedback");
    if (!errorDiv) {
      errorDiv = document.createElement("div");
      errorDiv.className = "invalid-feedback d-block";
      field.parentNode.appendChild(errorDiv);
    }
    errorDiv.textContent = message;
  }

  // Ocultar errores de campo
  function hideFieldError(field) {
    const errorDiv = field.parentNode.querySelector(".invalid-feedback");
    if (errorDiv) {
      errorDiv.remove();
    }
  }

  // Efectos de carga para botones
  const submitButtons = document.querySelectorAll('button[type="submit"]');
  submitButtons.forEach((button) => {
    button.addEventListener("click", function () {
      this.classList.add("loading");
      this.innerHTML =
        '<i class="fas fa-spinner fa-spin me-2"></i>Procesando...';
    });
  });

  // Notificaciones toast (si Bootstrap está disponible)
  function showToast(message, type = "info") {
    const toastContainer = document.getElementById("toast-container");
    if (!toastContainer) {
      const container = document.createElement("div");
      container.id = "toast-container";
      container.className = "position-fixed top-0 end-0 p-3";
      container.style.zIndex = "1055";
      document.body.appendChild(container);
    }

    const toastHtml = `
            <div class="toast align-items-center text-white bg-${type} border-0" role="alert">
                <div class="d-flex">
                    <div class="toast-body">
                        ${message}
                    </div>
                    <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button>
                </div>
            </div>
        `;

    toastContainer.insertAdjacentHTML("beforeend", toastHtml);
    const toastElement = toastContainer.lastElementChild;
    const toast = new bootstrap.Toast(toastElement);
    toast.show();

    // Remover el toast después de que se oculte
    toastElement.addEventListener("hidden.bs.toast", function () {
      this.remove();
    });
  }

  // Contador de caracteres para descripción
  const descripcionInput = document.querySelector('input[name="descripcion"]');
  if (descripcionInput) {
    const counter = document.createElement("small");
    counter.className = "form-text text-muted";
    counter.textContent = "0/255 caracteres";
    descripcionInput.parentNode.appendChild(counter);

    descripcionInput.addEventListener("input", function () {
      const length = this.value.length;
      counter.textContent = `${length}/255 caracteres`;

      if (length > 200) {
        counter.className = "form-text text-warning";
      } else {
        counter.className = "form-text text-muted";
      }
    });
  }

  // Filtros dinámicos
  const filterForm = document.querySelector('form[action*="lista_tareas"]');
  if (filterForm) {
    const filterInputs = filterForm.querySelectorAll("input, select");
    filterInputs.forEach((input) => {
      input.addEventListener("change", function () {
        // Auto-submit del formulario cuando cambian los filtros
        setTimeout(() => {
          filterForm.submit();
        }, 500);
      });
    });
  }

  // Efectos de scroll suave
  const smoothScrollLinks = document.querySelectorAll('a[href^="#"]');
  smoothScrollLinks.forEach((link) => {
    link.addEventListener("click", function (e) {
      e.preventDefault();
      const targetId = this.getAttribute("href");
      const targetElement = document.querySelector(targetId);

      if (targetElement) {
        targetElement.scrollIntoView({
          behavior: "smooth",
          block: "start",
        });
      }
    });
  });

  // Modo oscuro toggle (opcional)
  const darkModeToggle = document.getElementById("dark-mode-toggle");
  if (darkModeToggle) {
    darkModeToggle.addEventListener("click", function () {
      document.body.classList.toggle("dark-mode");
      const isDark = document.body.classList.contains("dark-mode");
      localStorage.setItem("darkMode", isDark);
    });

    // Cargar preferencia guardada
    const savedDarkMode = localStorage.getItem("darkMode");
    if (savedDarkMode === "true") {
      document.body.classList.add("dark-mode");
    }
  }

  // Estadísticas animadas
  const statsNumbers = document.querySelectorAll(".stats-card h3");
  statsNumbers.forEach((number) => {
    const finalValue = parseInt(number.textContent);
    animateNumber(number, 0, finalValue, 1000);
  });

  function animateNumber(element, start, end, duration) {
    const startTime = performance.now();

    function updateNumber(currentTime) {
      const elapsed = currentTime - startTime;
      const progress = Math.min(elapsed / duration, 1);

      const current = Math.floor(start + (end - start) * progress);
      element.textContent = current;

      if (progress < 1) {
        requestAnimationFrame(updateNumber);
      }
    }

    requestAnimationFrame(updateNumber);
  }

  // Efectos de parallax para el hero section
  const heroSection = document.querySelector(".hero-section");
  if (heroSection) {
    window.addEventListener("scroll", function () {
      const scrolled = window.pageYOffset;
      const rate = scrolled * -0.5;
      heroSection.style.transform = `translateY(${rate}px)`;
    });
  }

  console.log("Gestor de Tareas inicializado correctamente");
});
