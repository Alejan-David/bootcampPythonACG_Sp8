import unittest
from modelos.dueno import Dueno
from modelos.mascota import Mascota
from modelos.consulta import Consulta

class TestMascota(unittest.TestCase):
    def setUp(self):
         # Objeto con los datos quemados para las pruebas
        self.dueno = Dueno("Ana López", "323456789", "Av. Siempre Viva")
        self.mascota = Mascota("Luna", "Perro", "Labrador", 3, self.dueno)
        self.consulta = Consulta("2025-06-03", "Dolor de oído", "Otitis", self.mascota)

    #Verifica que el nombre de la mascota sea un string y no este vacio    
    def test_nombre_mascota_no_vacio(self):
        self.assertIsInstance(self.mascota.nombre, str)
        self.assertTrue(self.mascota.nombre.strip() != "")

    #Verifica que el especie de la mascota sea un string y no este vacio    
    def test_especie_no_vacio(self):
        self.assertIsInstance(self.mascota.especie, str)
        self.assertTrue(self.mascota.especie.strip() != "")   

    #Verifica que el raza de la mascota sea un string y no este vacio   
    def test_raza_no_vacio(self):
        self.assertIsInstance(self.mascota.raza, str)
        self.assertTrue(self.mascota.raza.strip() != "")    

    #Verifica que la edad de la mascota sea un int y mayor que cero 
    def test_edad_positiva(self):
        self.assertIsInstance(self.mascota.edad, int)
        self.assertGreaterEqual(self.mascota.edad, 0)

    #Vertifica que el nombre del dueño este asociado con la mascota
    def test_dueno_asocidado(self):
        self.assertEqual(self.mascota.dueno.nombre, self.dueno.nombre )

    #Verifica que el nombre del dueño sea un string y no este vacio    
    def test_dueno_no_vacio(self):
        self.assertIsInstance(self.dueno.nombre, str)
        self.assertTrue(self.dueno.nombre.strip() != "")

    #Verifica que el numero de telefono sea digitos del 0 al 9    
    def test_telefono_numero(self):
        self.assertTrue(self.dueno.telefono.isdigit())

    #Verifica que la dirección no sea string y no este vacia 
    def test_direccion_no_vacia(self):
        self.assertIsInstance(self.dueno.direccion,str)
        self.assertTrue(self.dueno.direccion.strip() != "")

    #Verfica que los datos del dueño sean correctos a los ingresados 
    def test_dueno_correctos(self):
        self.assertEqual(self.dueno.nombre, "Ana López")
        self.assertEqual(self.dueno.telefono, "323456789")
        self.assertEqual(self.dueno.direccion, "Av. Siempre Viva")

    #Verifica que los datos de la moscatoa sean correctos a los ingresados 
    def test_mascota_correctos(self):
        self.assertEqual(self.mascota.nombre, "Luna")
        self.assertEqual(self.mascota.especie, "Perro")
        self.assertEqual(self.mascota.raza, "Labrador")
        self.assertEqual(self.mascota.edad, 3)
        self.assertEqual(self.mascota.dueno, self.dueno)

    #Verifica que los datos de la consulta sean correctos a los ingresados 
    def test_atributos_consulta(self):
        self.assertEqual(self.consulta.fecha, "2025-06-03")
        self.assertEqual(self.consulta.motivo, "Dolor de oído")
        self.assertEqual(self.consulta.diagnostico, "Otitis")

    #Verifica que el nombre de la mascota sea correcto al ingresado 
    def test_mascota_asociada(self):
        self.assertIsInstance(self.consulta.mascota, Mascota)
        self.assertEqual(self.consulta.mascota.nombre, "Luna")

if __name__ == '__main__':
    unittest.main()