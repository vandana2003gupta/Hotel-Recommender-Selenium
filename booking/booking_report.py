from selenium.webdriver.common.by import By

class BookingReport:
    def __init__(self, container_element):
        self.container = container_element

    def pull_deal_box_elements(self):
        cards = self.container.find_elements(By.CSS_SELECTOR, 'div[data-testid="property-card"]')
        if not cards:
            cards = self.container.find_elements(By.CSS_SELECTOR, '.sr_property_block')
        return cards

    def pull_deal_box_attributes(self):
        results = []
        for box in self.pull_deal_box_elements():
            try:
                name = box.find_element(By.CSS_SELECTOR, 'div[data-testid="title"], .sr-hotel__name').text.strip()
            except Exception:
                name = 'N/A'
            try:
                price = box.find_element(By.CSS_SELECTOR, 'span[data-testid="price-and-discounted-price"], .bui-price-display__value').text.strip()
            except Exception:
                price = 'N/A'
            try:
                score = box.find_element(By.CSS_SELECTOR, 'div[data-testid="review-score"], .bui-review-score__badge').text.strip()
            except Exception:
                score = 'N/A'
            results.append([name, price, score])
        return results
