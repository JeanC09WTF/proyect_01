from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import os
import time

# Configuración de BrowserStack
USERNAME = os.environ.get("BROWSERSTACK_USERNAME")
ACCESS_KEY = os.environ.get("BROWSERSTACK_ACCESS_KEY")
URL = f"https://{USERNAME}:{ACCESS_KEY}@hub-cloud.browserstack.com/wd/hub"

# Configuración del navegador (actualizado para Selenium 4+)
capabilities = {
    "os": "Windows",
    "os_version": "10",
    "browserName": "Chrome",
    "browser_version": "latest",
    "name": "Prueba en Google Search",
    "bstack:options": {
        "debug": "true",
        "consoleLogs": "verbose"
    }
}

def test_google_search():
    driver = webdriver.Remote(
        command_executor=URL,
        options=webdriver.ChromeOptions().add_capabilities(capabilities)
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
        driver.execute_script(
            'browserstack_executor: {"action": "setSessionStatus", "arguments": {"status":"failed", "reason": "Error en la prueba"}}'
        )
        raise e
    finally:
        driver.quit()

if __name__ == "__main__":
    test_google_search()
