from django.contrib.auth.models import User
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

class MySeleniumTests(StaticLiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        """ Configuración inicial: crea el usuario admin y abre el navegador. """
        super().setUpClass()
        opts = Options()
        cls.selenium = WebDriver(options=opts)
        cls.selenium.implicitly_wait(5)

        # Crear un superusuario para el test
        User.objects.create_superuser(username="admin", password="admin123", email="admin@example.com")

    @classmethod
    def tearDownClass(cls):
        """ Cierra el navegador al finalizar los tests. """
        cls.selenium.quit()
        super().tearDownClass()

    def test_create_questions_and_choices(self):
        """ Prueba la creación de 2 Questions y 2 Choices por cada Question. """
        self.selenium.get(f"{self.live_server_url}/admin/login/")

        # Iniciar sesión en el admin
        username_input = self.selenium.find_element(By.NAME, "username")
        password_input = self.selenium.find_element(By.NAME, "password")
        username_input.send_keys("admin")
        password_input.send_keys("admin123")
        self.selenium.find_element(By.XPATH, '//input[@value="Log in"]').click()


        # Crear 2 Choices para cada Question
        for i in range(1, 3):  # Para cada pregunta
            

            # Seleccionar la pregunta correspondiente en el dropdown
            question_dropdown = self.selenium.find_element(By.XPATH, "//a[@href='/admin/myapp/question/add/']")
            question_dropdown.click()

            # Rellenar el texto de la choice
            question_input = self.selenium.find_element(By.NAME, "question_text")
            question_input.send_keys(f"Pregunta {i}")
            question_date = self.selenium.find_element(By.NAME, "pub_date_0")
            question_date.send_keys(f"2025-02-06")
            question_time = self.selenium.find_element(By.NAME, "pub_date_1")
            question_time.send_keys(f"18:58:28")

            choice_1 = self.selenium.find_element(By.NAME, "choice_set-0-choice_text")
            choice_1.send_keys(f"Me quiero")
            choice_2 = self.selenium.find_element(By.NAME, "choice_set-1-choice_text")
            choice_2.send_keys(f"Morir")
               
                # Guardar el choice
            self.selenium.find_element(By.NAME, "_save").click()
            time.sleep(5)  # Esperar a que se guarde antes de continuar
        #entra en la pagina
        CC = self.selenium.find_element(By.XPATH, "//a[@href='/admin/myapp/question/2/change/']")
        CC.click()
        # encuentra las choices y se guarda
        H = self.selenium.find_element(By.ID, "id_choice_set-0-choice_text")
        B = self.selenium.find_element(By.ID, "id_choice_set-1-choice_text")
        # se guarda el texto de los campos
        text = H.get_attribute("value")
        text2 = B.get_attribute("value")
        # se define el texto esperado
        et1 = "Me quiero"
        et2 = "Morir"
        # viva el chat(gpt) hacemos la comprobacion
        self.assertEqual(text, et1, f"El texto esperado era '{et1}', pero se obtuvo '{text}'") 
        self.assertEqual(text2, et2, f"El texto esperado era '{et1}', pero se obtuvo '{text2}'") 
        
        
        
        

