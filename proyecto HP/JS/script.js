// script.js
function cambiarEstilo(opcion) {
    const root = document.documentElement.style;
    switch (opcion) {
        case 'gryffindor':
            root.setProperty('--color-fondo', '#740001');
            root.setProperty('--color-texto', '#eeba30');
            // Define otras propiedades de estilo aquí
            break;
        case 'slytherin':
            root.setProperty('--color-fondo', '#e3e3e3');
            root.setProperty('--color-texto', '#002f01');
            // Define otras propiedades de estilo aquí
            break;
        case 'hufflepuff':
            root.setProperty('--color-fondo', '#d4c20e');
            root.setProperty('--color-texto', '#000');
            // Define otras propiedades de estilo aquí
            break;
        case 'ravenclaw':
            root.setProperty('--color-fondo', '#0e1a40');
            root.setProperty('--color-texto', '#aaa');
            // Define otras propiedades de estilo aquí
            break;
    }
}

// Captura el formulario de la carta
const cartaFormulario = document.getElementById('carta-form');

// Captura la imagen de la carta
const cartaImagen = document.getElementById('carta-imagen');

// Agrega un evento al formulario para manejar su envío
cartaFormulario.addEventListener('submit', function(event) {
  event.preventDefault(); // Evita que el formulario se envíe normalmente

  // Captura los valores de los campos del formulario
  const title = cartaFormulario.elements['title'].value;
  const name = cartaFormulario.elements['name'].value;
  const surname = cartaFormulario.elements['surname'].value;
  const address1 = cartaFormulario.elements['address'].value;
  const address2 = cartaFormulario.elements['address2'].value;
  const email = cartaFormulario.elements['email'].value;
  const papertex = cartaFormulario.elements['papertex'].checked;

  // Construye el texto de la carta con los valores del formulario
  const cartaTexto = `
  <div class="carta">
      <div class="membrete">
          ${title} ${name} ${surname}<br>
          ${address1}<br>
          ${address2}<br>
          ${email}<br><br>
      </div>
      <div class="cuerpo">
          <p>Estimado/a ${title} ${surname},</p>
          <p>Nos complace informarte que usted has sido aceptado en el Colegio Hogwarts de Magia y Hechicería.</p> 
          <p>Las clases comienzan el 1° de septiembre. </p>
          <p>Te esperamos en la plataforma 9 y 3/4 en la estación de tren de King's Cross</p>
      </div>

      <div class="firma">
          Atentamente,<br>
          El Director del Colegio Hogwarts de Magia y Hechicería
      </div>
  </div>
`;

  // Muestra la imagen de la carta
  cartaImagen.style.display = 'block';

  // Captura el contenedor donde se mostrará el texto de la carta
  const cartaContenedor = document.querySelector('#carta-texto');

  // Limpia cualquier contenido previo en el contenedor
  cartaContenedor.innerHTML = '';

  // Crea un nuevo elemento de párrafo para mostrar el texto de la carta
  const cartaParrafo = document.createElement('p');
  cartaParrafo.innerHTML = cartaTexto; // Usa innerHTML para renderizar saltos de línea (<br>)

  // Aplica la textura de papel si está marcada en el formulario
  if (papertex) {
    cartaParrafo.classList.add('textura-papel');
  }

  // Agrega el párrafo de la carta al contenedor
  cartaContenedor.appendChild(cartaParrafo);

  // Actualiza el membrete
  const membrete = document.querySelector('#membrete');
  membrete.innerHTML = `${title} ${name} ${surname}<br>${address1}<br>${address2}`;
   membrete.style.display = 'block';
});

// hasta acá gus