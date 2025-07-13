from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import os

# Configuración de BrowserStack (usa variables de entorno)
USERNAME = os.environ.get("cuentarecuperaci_XCNBUK")
ACCESS_KEY = os.environ.get("pNFGbk5NPRQNazx9d4Nn")
URL = f"https://{USERNAME}:{ACCESS_KEY}@hub-cloud.browserstack.com/wd/hub"

# Configuración del navegador (Chrome en Windows 10)
desired_cap = {
    "os": "Windows",
    "os_version": "10",
    "browser": "Chrome",
    "browser_version": "latest",
    "name": "Prueba en Google Search",
    "browserstack.debug": "true",
    "browserstack.console": "verbose"
}

def test_google_search():
    driver = webdriver.Remote(
        command_executor=URL,
        desired_capabilities=desired_cap
    )
    try:
        # 1. Navegar a Google
        driver.get("https://www.google.com")
        assert "Google" in driver.title

        # 2. Buscar "BrowserStack"
        search_box = driver.find_element("name", "q")
        search_box.send_keys("BrowserStack")
        search_box.send_keys(Keys.RETURN)
        time.sleep(2)

        # 3. Verificar resultados
        assert "BrowserStack" in driver.title
        print("✅ Prueba exitosa!")

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
