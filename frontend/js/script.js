document.getElementById('heartForm').addEventListener('submit', function(e) {
    e.preventDefault();

    const form = e.target;
    const formData = new FormData(form);
    const data = {};

    formData.forEach((val, key) => {
        // Convertir solo si es un número válido
        if (!isNaN(val) && val.trim() !== "" && key !== "name") {
            data[key] = parseFloat(val);
        } else {
            data[key] = val;
        }
    });

    fetch('http://localhost:5000/predict', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(result => {
        document.getElementById('result').textContent = result.message;
        form.reset();
    })
    .catch(error => {
        console.error('Error:', error);
    });
});
    
function mostrarHistorial(index) {
    const paciente = window.pacientes[index];
    const historialDiv = document.getElementById('historial-container');
    const tabla = document.getElementById('tabla-pacientes');
    
    // Animación de salida para la tabla
    tabla.classList.remove("fade-slide-in");
    tabla.classList.add("fade-slide-out");
    
    setTimeout(() => {
        tabla.classList.add('no-mostrar');
        tabla.classList.remove("fade-slide-out");
    
        historialDiv.innerHTML = `
            <div class="historial fade-slide-in">
                <div class="historial-header">
                    <h3>Historiales Clínicos</h3>
                    <button class="botonCerrar" onclick="cerrarHistorial()">X</button>
                </div>
                <div class="historiales">
                    ${paciente.history.map((entry, i) => `
                    <div class="historial-item">
                        <h3>HISTORIAL ${i + 1}</h3>
                        <div class="historial-body">
                            <div class="datosPaciente">
                                <p>Nombre: ${paciente.name}</p>
                                <p>Edad: ${entry.age}</p>
                            </div>
                            <div class="datosPaciente">
                                <p>Frecuencia máxima: ${entry.thalach}</p>
                                <p>Resultado: ${entry.prediction === 1 ? 'Posible arritmia' : 'Normal'}</p>
                            </div>
                        </div>
                    </div>
                `).join('')}
                </div>
            </div>`;}, 500); // Esperamos a que termine la animación
        }
    
function cerrarHistorial() {
    const historialDiv = document.getElementById('historial-container');
    const tabla = document.getElementById('tabla-pacientes');
    
    // Animación de salida para historial
    const historial = historialDiv.querySelector('.historial');
    if (historial) {
        historial.classList.remove("fade-slide-in");
        historial.classList.add("fade-slide-out");
    
        setTimeout(() => {
            historialDiv.innerHTML = '';
    
            // Mostrar la tabla con animación
            tabla.classList.remove('no-mostrar');
            tabla.classList.add("fade-slide-in");
        }, 
    500);
    } else {
        // Si no hay historial (por seguridad)
        tabla.classList.remove('no-mostrar');
        tabla.classList.add("fade-slide-in");
    }
}

function mostrarFormularioDiagnostico(index) {
    const paciente = window.pacientes[index];
    const contenedor = document.getElementById("historial-container");
    const tabla = document.getElementById('tabla-pacientes');

    tabla.classList.add('no-mostrar');

    contenedor.innerHTML = `
        <div class="form-container fade-slide-in">
            <div class="form-header">
                <h2>Nuevo Diagnóstico para ${paciente.name}</h2>
                <button class="botonHistorial" onclick="cerrarFormularioDiagnostico()">X</button>
            </div>

            <form id="heartForm">
                <fieldset class="paciente-DatosMedicos">
                    <legend>Antecedentes médicos</legend>
                    <div class="container-datos">
                        <label for="cp">Chest Pain</label>
                        <select id="cp" name="cp">
                            <option value="0">0</option>
                            <option value="1">1</option>
                            <option value="2">2</option>
                            <option value="3">3</option>
                        </select>

                        <label for="trestbps">Resting BP</label>
                        <input type="number" id="trestbps" name="trestbps" required />

                        <label for="chol">Colesterol sérico (mg/dl):</label>
                        <input type="number" id="chol" name="chol" required />
                    </div>

                    <div class="container-datos">
                        <label for="fbs">Azúcar en sangre en ayunas</label>
                        <input type="number" id="fbs" min="0" max="1" name="fbs" required />

                        <label for="restecg">Resultados del ECG</label>
                        <input type="number" id="restecg" name="restecg" required />

                        <label for="thalach">Frecuencia cardíaca máxima</label>
                        <input type="number" id="thalach" name="thalach" required />
                    </div>

                    <div class="container-datos">
                        <label for="exang">Angina inducida por ejercicio</label>
                        <input type="number" id="exang" min="0" max="1" name="exang" required />

                        <label for="oldpeak">Oldpeak</label>
                        <input type="number" step="0.1" id="oldpeak" name="oldpeak" required />

                        <label for="slope">Pendiente del segmento ST</label>
                        <input type="number" id="slope" name="slope" required />
                    </div>

                    <div class="container-datos">
                        <label for="ca">Vasos principales por fluoroscopía:</label>
                        <input type="number" id="ca" min="0" max="3" name="ca" required />

                        <label for="thal">Talasemia</label>
                        <input type="number" id="thal" min="0" max="2" name="thal" required />

                        <input type="submit" value="ANALIZAR DATOS"  />
                    </div>
                </fieldset><br>

            </form>
            <div id="result-container">
                <p id="result"></p>
            </div>
        </div>
    `;

    // Evento submit
    document.getElementById("heartForm").addEventListener("submit", async (e) => {
    e.preventDefault();
        const form = e.target;

        const datosMedicos = {
            name: paciente.name,
            age: paciente.age,
            sex: paciente.history[0].sex,
            cp: +form.cp.value,
            trestbps: +form.trestbps.value,
            chol: +form.chol.value,
            fbs: +form.fbs.value,
            restecg: +form.restecg.value,
            thalach: +form.thalach.value,
            exang: +form.exang.value,
            oldpeak: +form.oldpeak.value,
            slope: +form.slope.value,
            ca: +form.ca.value,
            thal: +form.thal.value,
        };

        const response = await fetch("http://localhost:5000/predict", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(datosMedicos),
        });

        const result = await response.json();
        alert(result.message);
        location.reload(); // recarga todo el documento
    });
}

function cerrarFormularioDiagnostico() {
    const contenedor = document.getElementById("historial-container");
    const tabla = document.getElementById('tabla-pacientes');
    const formContainer = contenedor.querySelector('.form-container');

    if (formContainer) {
        // Aplicamos la animación de salida para cerrar el formulario
        formContainer.classList.remove("fade-slide-in");
        formContainer.classList.add("fade-slide-out");

        // Esperamos el tiempo de la animación
        setTimeout(() => {
            contenedor.removeChild(formContainer);  // Elimina el formulario del DOM
            tabla.classList.remove('no-mostrar');
            tabla.classList.add("fade-slide-in");
        }, 500); // Asegúrate de que este tiempo coincida con la duración de la animación
    } else {
        // Si no hay formulario, solo mostramos la tabla
        tabla.classList.remove('no-mostrar');
        tabla.classList.add("fade-slide-in");
    }
}


