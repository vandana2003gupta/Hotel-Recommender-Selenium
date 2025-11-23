from selenium.webdriver.common.by import By

class BookingFiltration:
    def __init__(self, driver):
        self.driver = driver

    def apply_star_rating(self, *star_values):
        try:
            box = self.driver.find_element(By.ID, 'filter_class')
            children = box.find_elements(By.CSS_SELECTOR, '*')
            for sv in star_values:
                want = f"{sv} stars"
                for ch in children:
                    try:
                        if want == ch.text.strip():
                            ch.click()
                    except Exception:
                        pass
        except Exception:
            pass

    def sort_price_lowest_first(self):
        try:
            self.driver.find_element(By.CSS_SELECTOR, 'li[data-id="price"]').click()
        except Exception:
            try:
                self.driver.find_element(By.CSS_SELECTOR, 'button[data-id="price"]').click()
            except Exception:
                pass
