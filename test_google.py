from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options as ChromeOptions
import os
import time

# Configuración de BrowserStack
USERNAME = os.environ.get("BROWSERSTACK_USERNAME")
ACCESS_KEY = os.environ.get("BROWSERSTACK_ACCESS_KEY")
URL = f"https://hub-cloud.browserstack.com/wd/hub"

# Configuración del navegador (compatible con Selenium 4.10+)
options = ChromeOptions()
options.set_capability("browserName", "Chrome")
options.set_capability("browserVersion", "latest")
options.set_capability("platformName", "Windows")
options.set_capability("sessionName", "Prueba en Google Search")

# Opciones específicas de BrowserStack
options.set_capability("bstack:options", {
    "osVersion": "10",
    "debug": "true",
    "consoleLogs": "verbose",
    "userName": USERNAME,
    "accessKey": ACCESS_KEY
})

def test_google_search():
    driver = webdriver.Remote(
        command_executor=URL,
        options=options
    )
    
    try:
        # 1. Navegar a Google
        driver.get("https://www.google.com")
        assert "Google" in driver.title

        # 2. Buscar "BrowserStack"
        search_box = driver.find_element(By.NAME, "q")
        search_box.send_keys("BrowserStack")
        search_box.send_keys(Keys.RETURN)
        time.sleep(2)

        # 3. Verificar resultados
        assert "BrowserStack" in driver.title
        print("✅ Prueba exitosa!")
        driver.execute_script(
            'browserstack_executor: {"action": "setSessionStatus", "arguments": {"status":"passed", "reason": "Prueba exitosa"}}'
        )

    except Exception as e:
        print(f"❌ Error: {e}")
        driver.save_screenshot("error.png")
        driver.execute_script(
            'browserstack_executor: {"action": "setSessionStatus", "arguments": {"status":"failed", "reason": "Error en la prueba"}}'
        )
        raise e
    finally:
        driver.quit()

if __name__ == "__main__":
    test_google_search()
