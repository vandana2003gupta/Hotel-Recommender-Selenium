from booking import Booking
from booking.booking_report import BookingReport
from booking.booking_filtration import BookingFiltration
from selenium.webdriver.common.by import By
from tabulate import tabulate
import time

def main():
    place = input("Where do you want to go? ").strip()
    check_in = input("Check-in date (YYYY-MM-DD): ").strip()
    check_out = input("Check-out date (YYYY-MM-DD): ").strip()
    adults = int(input("Number of adults: ").strip() or 1)

    try:
        with Booking(teardown=True, headless=False) as bot:
            bot.land_first_page()
            bot.change_currency("USD")
            bot.select_place_to_go(place)
            bot.select_dates(check_in, check_out)
            bot.select_adults(adults)
            bot.click_search()

            # small wait for page to load before applying filters
            time.sleep(2)
            bot.apply_filters()
            time.sleep(1)

            # now extract results via robust selectors
            results = bot.extract_results()
            print("\n")
            print(tabulate(results, headers=["Hotel", "Price", "Score"], tablefmt="fancy_grid"))

    except Exception as e:
        print("Error:", e)

if __name__ == "__main__":
    main()
