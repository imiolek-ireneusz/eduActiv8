# -*- coding: utf-8 -*-

# This is a list of words used by the word builder and word maze games and possibly other games built in the future
# these words are a naive translation of a part of most commonly used words in English in each sub-list in the list di
# first number is a number of words in the sub-list to avoid counting it every time the list is selected the sub-lists
# are consisting of words with len() of 3 - 10. I think the way of going about internationalization here would be to
# create a new list with words most commonly used in your language rather than translating the English version.
# I am not sure if they are appropriate for children, but if anyone is interested we can try to built something more
# suitable or if you like you can try to edit this list - remove the words that you think are either not in German or
# are not suitable for under 10 years old children and send it back to the email address shown at the start of the game.
# If you have a better list please send it to me and I will format it and add it to the game. This is a very naive
# translation from google translate - only resorted and counted.

di = [
    [27, 'así', 'con', 'del', 'dio', 'dos', 'día', 'fui', 'hoy', 'los', 'los', 'los', 'los', 'más', 'oro', 'oso', 'oír',
     'por', 'que', 'sin', 'sin', 'sur', 'una', 'uno', 'uva', 'ver', 'ver', 'vez'],
    [49, 'algo', 'aquí', 'azul', 'bajo', 'boca', 'cada', 'cama', 'cero', 'clac', 'cuna', 'cuna', 'cuya', 'dijo', 'ella',
     'flor', 'flor', 'gris', 'hace', 'lado', 'leer', 'mano', 'maíz', 'nada', 'nada', 'niño', 'ocho', 'oler', 'otro',
     'otro', 'oído', 'para', 'paño', 'peso', 'pico', 'pide', 'piel', 'piso', 'rana', 'roca', 'rojo', 'ropa', 'seis',
     'tira', 'todo', 'todo', 'tren', 'tubo', 'vete', 'vino'],
    [84, 'ahora', 'armas', 'bache', 'barco', 'bello', 'borde', 'botín', 'campo', 'carne', 'carta', 'caída', 'caída',
     'ciego', 'clara', 'coche', 'comer', 'común', 'deber', 'entre', 'espía', 'floja', 'flota', 'forma', 'frase',
     'fresa', 'fruta', 'fuego', 'garra', 'golpe', 'goteo', 'hecho', 'horas', 'igual', 'junto', 'justo', 'lavar',
     'lento', 'línea', 'marca', 'marzo', 'media', 'mejor', 'mente', 'meses', 'miedo', 'miedo', 'migas', 'miles',
     'mirar', 'mismo', 'nacer', 'norte', 'novio', 'nuevo', 'nuevo', 'nunca', 'padre', 'paseo', 'pecas', 'peces',
     'pieza', 'plana', 'plano', 'poder', 'poema', 'punto', 'punto', 'regla', 'sabía', 'saltó', 'saltó', 'siglo',
     'signo', 'sobre', 'sueño', 'tallo', 'tapar', 'temor', 'tengo', 'valor', 'veces', 'venir', 'vista', 'visto'],
    [70, 'ajuste', 'amplio', 'anillo', 'arroyo', 'azúcar', 'blanco', 'boceto', 'brocha', 'básico', 'cambio', 'cambio',
     'camino', 'camisa', 'camión', 'choque', 'crecer', 'criado', 'cuándo', 'cómodo', 'dentro', 'deriva', 'dibujo',
     'dragón', 'escasa', 'espera', 'estufa', 'figura', 'flauta', 'flores', 'fluido', 'frotar', 'fuerte', 'fuerza',
     'ganado', 'grande', 'grande', 'grillo', 'hablar', 'hablar', 'huelga', 'hélice', 'listos', 'mancha', 'mancha',
     'montón', 'método', 'número', 'pasado', 'pasado', 'patrón', 'pensar', 'prueba', 'prueba', 'pueblo', 'página',
     'quieto', 'rastro', 'rugido', 'rápida', 'sentir', 'tierra', 'trampa', 'tratar', 'triste', 'varios', 'verano',
     'verdad', 'viajes', 'vieira', 'áspero'],
    [48, 'acuerdo', 'agujero', 'alegría', 'apretar', 'armario', 'barrido', 'calamar', 'camilla', 'canción', 'cerebro',
     'ciruela', 'consejo', 'cuidado', 'derrame', 'después', 'difícil', 'ejemplo', 'embargo', 'energía', 'espacio',
     'excepto', 'hechizo', 'hombres', 'injerto', 'mezclar', 'muestra', 'nadando', 'negocio', 'nuestro', 'ocultar',
     'orgullo', 'pequeño', 'piernas', 'pizarra', 'plantas', 'pájaros', 'párrafo', 'rebuzno', 'rejilla', 'repente',
     'sangrar', 'sentido', 'sugirió', 'sílabas', 'todavía', 'trabajo', 'vestido', 'volante'],
    [46, 'adjetivo', 'cacarear', 'calabaza', 'caliente', 'comienzo', 'conjunto', 'continuo', 'cultivos', 'defender',
     'desierto', 'detalles', 'entender', 'entonces', 'escisión', 'escuchar', 'estación', 'estirada', 'fábricas',
     'garabato', 'gobierno', 'insectos', 'interior', 'ladrillo', 'largarse', 'linterna', 'mantener', 'merienda',
     'millones', 'montañas', 'palabras', 'preparar', 'problema', 'profesor', 'programa', 'proteger', 'proyecto',
     'príncipe', 'recordar', 'registro', 'retorcer', 'ronquido', 'silencio', 'soldados', 'símbolos', 'valiente',
     'voluntad'],
    [30, 'alimentos', 'alimentos', 'argumento', 'arrebatar', 'brillante', 'brillante', 'cabriolas', 'compuesto',
     'constante', 'corriente', 'cualquier', 'derribado', 'diferente', 'dirección', 'eléctrica', 'encuentra',
     'garabatos', 'generales', 'habilidad', 'industria', 'moléculas', 'pendiente', 'preguntas', 'problemas',
     'productos', 'rebajarse', 'respuesta', 'resultado', 'sentencia', 'subrayado'],
    [15, 'campesinos', 'desarrollo', 'determinar', 'diferencia', 'golondrina', 'incorrecto', 'lentamente', 'movimiento',
     'necesarias', 'presidente', 'pronunciar', 'quemaduras', 'rociadores', 'sustancias', 'zapatillas']]
