<!DOCTYPE html>
<html>
<head>
    <title>Resultado del Test de Casa de Hogwarts</title>
</head>
<body>
    <?php
    if ($_SERVER["REQUEST_METHOD"] == "POST") {
        // Recuperar las respuestas del formulario
        $respuesta1 = $_POST["pregunta1"];
        $respuesta2 = $_POST["pregunta2"];
        $respuesta3 = $_POST["pregunta3"];
        
        // Calcular el resultado basado en las respuestas (ejemplo ficticio)
        $resultado = "";

        if ($respuesta1 == "a" && $respuesta2 == "b" && $respuesta3 == "c") {
            $resultado = "Gryffindor";
        } elseif ($respuesta1 == "b" && $respuesta2 == "a" && $respuesta3 == "d") {
            $resultado = "Slytherin";
        } elseif ($respuesta1 == "c" && $respuesta2 == "c" && $respuesta3 == "a") {
            $resultado = "Hufflepuff";
        } elseif ($respuesta1 == "d" && $respuesta2 == "d" && $respuesta3 == "b") {
            $resultado = "Ravenclaw";
        } else {
            $resultado = "No se pudo determinar la casa";
        }
        
        // Mostrar el resultado
        echo "<h1>¡Felicidades!</h1>";
        echo "<p>Según tus respuestas, perteneces a la casa de $resultado.</p>";
    } else {
        // Si no se han enviado datos del formulario, puedes redirigir al usuario a la página del formulario o mostrar un mensaje de error.
        echo "<p>No se han enviado datos del formulario.</p>";
    }
    ?>
</body>
</html>

 
