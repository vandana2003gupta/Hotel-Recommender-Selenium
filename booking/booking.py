import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# use webdriver-manager to auto-download chromedriver
try:
    from webdriver_manager.chrome import ChromeDriverManager
    _WM_AVAILABLE = True
except Exception:
    _WM_AVAILABLE = False

from booking.constants import BASE_URL

class Booking:

    def __init__(self, driver_path: str = None, teardown: bool = False, headless: bool = False):
        self.driver_path = driver_path
        self.teardown = teardown
        self.headless = headless

        options = webdriver.ChromeOptions()
        options.add_experimental_option("excludeSwitches", ["enable-logging"])
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        # only enable headless if requested
        if headless:
            options.add_argument("--headless=new")

        if _WM_AVAILABLE:
            service = Service(ChromeDriverManager().install())
        else:
            # if user provides driver_path add to PATH, else rely on PATH
            if driver_path:
                os.environ["PATH"] += os.pathsep + driver_path
            service = Service()

        self.driver = webdriver.Chrome(service=service, options=options)
        self.driver.implicitly_wait(10)

    # context manager
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, exc_tb):
        if self.teardown:
            try:
                self.driver.quit()
            except Exception:
                pass

    def get_driver(self):
        return self.driver

    def land_first_page(self):
        """Open Booking.com home"""
        self.driver.get(BASE_URL)

    def change_currency(self, currency: str = "USD"):
        driver = self.driver
        try:
            # Common 2024/2025 button
            btn = driver.find_element(By.CSS_SELECTOR, 'button[data-testid="header-currency-picker-trigger"]')
            btn.click()
            # wait for currency options to appear
            WebDriverWait(driver, 6).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'button[data-testid="selection-item"], a[data-currency]'))
            )
            # attempt data-value/data-currency matches, then text match
            try:
                cand = driver.find_element(By.CSS_SELECTOR, f'button[data-testid="selection-item"][data-value="{currency}"],'
                                                         f'button[data-testid="selection-item"][data-currency="{currency}"],'
                                                         f'a[data-currency="{currency}"]')
                cand.click()
                return
            except Exception:
                # fallback: find visible link/button containing currency code text
                items = driver.find_elements(By.CSS_SELECTOR, 'button, a')
                for it in items:
                    try:
                        if currency.upper() in it.text.upper():
                            it.click()
                            return
                    except Exception:
                        pass
        except Exception:
            # legacy selectors fallback
            try:
                btn = driver.find_element(By.CSS_SELECTOR, 'button[data-tooltip-text="Choose your currency"]')
                btn.click()
                opt = WebDriverWait(driver, 6).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, f'a[data-modal-header-async-url-param*="selected_currency={currency}"]'))
                )
                opt.click()
                return
            except Exception:
                pass

        # final fallback: ignore and continue, but inform user
        print("Continuing...")

    def select_place_to_go(self, place_to_go: str):
        """Type destination and click first suggestion when available."""
        driver = self.driver
        try:
            el = driver.find_element(By.ID, "ss")
            el.clear()
            el.send_keys(place_to_go)
            try:
                first = WebDriverWait(driver, 6).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, "li[data-i='0'], li[data-i=\"0\"]"))
                )
                first.click()
                return
            except Exception:
                # if suggestion not clickable, continue
                return
        except Exception:
            # alternative: header search input (sometimes different markup)
            try:
                el = driver.find_element(By.CSS_SELECTOR, "input[placeholder*='Where'], input[placeholder*='Where are you going']")
                el.clear()
                el.send_keys(place_to_go)
                time.sleep(1)
                try:
                    first = driver.find_element(By.CSS_SELECTOR, "li[data-i='0'], li[data-i=\"0\"]")
                    first.click()
                except Exception:
                    pass
            except Exception:
                raise

    def select_dates(self, check_in: str, check_out: str):
        driver = self.driver
        try:
            driver.find_element(By.CSS_SELECTOR, f'td[data-date="{check_in}"]').click()
            driver.find_element(By.CSS_SELECTOR, f'td[data-date="{check_out}"]').click()
        except Exception:
            # fallback: try name-based fields
            try:
                in_el = driver.find_element(By.NAME, "checkin")
                out_el = driver.find_element(By.NAME, "checkout")
                in_el.clear(); in_el.send_keys(check_in)
                out_el.clear(); out_el.send_keys(check_out)
            except Exception:
                # if both fail, just continue and let site default behavior handle
                pass

    def select_adults(self, count: int = 1):
        """Set number of adults using guest toggle controls."""
        driver = self.driver
        try:
            toggle = driver.find_element(By.ID, "xp__guests__toggle")
            toggle.click()
            # decrease loop to 1
            while True:
                try:
                    dec = driver.find_element(By.CSS_SELECTOR, 'button[aria-label="Decrease number of Adults"]')
                    dec.click()
                    cur = int(driver.find_element(By.ID, "group_adults").get_attribute("value"))
                    if cur == 1:
                        break
                except Exception:
                    break
            # increase to desired value
            try:
                inc = driver.find_element(By.CSS_SELECTOR, 'button[aria-label="Increase number of Adults"]')
                for _ in range(max(0, count - 1)):
                    inc.click()
            except Exception:
                pass
        except Exception:
            # if not found, ignore
            pass

    def click_search(self):
        """Click the primary search button or submit the form."""
        driver = self.driver
        try:
            btn = driver.find_element(By.CSS_SELECTOR, 'button[type="submit"], button[aria-label="Search"]')
            btn.click()
        except Exception:
            try:
                form = driver.find_element(By.TAG_NAME, "form")
                form.submit()
            except Exception:
                raise

    def apply_filters(self):
        """Apply basic filters: 4 & 5 stars and sort by price — robust to multiple UIs."""
        driver = self.driver
        # star filters
        try:
            for sv in ("4 stars", "5 stars"):
                try:
                    el = driver.find_element(By.XPATH, f"//div[@data-filters-group='class']//a[contains(., '{sv}')]")
                    driver.execute_script("arguments[0].click();", el)
                except Exception:
                    pass
        except Exception:
            pass

        # sort by price (try multiple variants)
        try:
            try:
                # new dropdown
                sort_btn = driver.find_element(By.CSS_SELECTOR, 'button[data-testid="sorters-dropdown-trigger"]')
                sort_btn.click()
                time.sleep(0.2)
                price_opt = driver.find_element(By.CSS_SELECTOR, 'button[data-id="price"], li[data-id="price"]')
                price_opt.click()
            except Exception:
                # older variant
                el = driver.find_element(By.CSS_SELECTOR, 'li[data-id="price"]')
                el.click()
        except Exception:
            pass

    def extract_results(self, max_results: int = 40):
        driver = self.driver
        results = []

        # wait for either modern or legacy card
        try:
            WebDriverWait(driver, 15).until(
                EC.any_of(
                    EC.presence_of_element_located((By.CSS_SELECTOR, 'div[data-testid="property-card"]')),
                    EC.presence_of_element_located((By.CSS_SELECTOR, '.sr_property_block'))
                )
            )
        except Exception:
            pass

        # prefer modern cards
        cards = driver.find_elements(By.CSS_SELECTOR, 'div[data-testid="property-card"]')
        if not cards:
            cards = driver.find_elements(By.CSS_SELECTOR, '.sr_property_block')

        for card in cards[:max_results]:
            name = "N/A"
            price = "N/A"
            score = "N/A"
            try:
                # modern title or legacy
                el = card.find_element(By.CSS_SELECTOR, 'div[data-testid="title"], .sr-hotel__name')
                name = el.text.strip()
            except Exception:
                pass
            try:
                el = card.find_element(By.CSS_SELECTOR, 'span[data-testid="price-and-discounted-price"], .bui-price-display__value')
                price = el.text.strip()
            except Exception:
                pass
            try:
                el = card.find_element(By.CSS_SELECTOR, 'div[data-testid="review-score"], .bui-review-score__badge')
                score = el.text.strip()
            except Exception:
                pass
            results.append([name, price, score])

        return results
