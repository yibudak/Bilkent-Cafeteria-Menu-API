# Copyright 2023 Yiğit Budak (https://github.com/yibudak)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from datetime import datetime
from selenium.webdriver.common.by import By
from backend import models, conf

chrome_options = Options()
chrome_options.add_argument("--headless")
driver = webdriver.Chrome(options=chrome_options, executable_path=conf.app.CHROMEDRIVER_PATH)
url = "http://kafemud.bilkent.edu.tr/monu_eng.html"

menu_object = models.env["daily_menus"]
meals_model = models.env["meals"]


def get_meals(meals):
    today_meals = []
    for single in meals:
        for single2 in single.split(" veya / or "):
            splitted = single2.split(" / ")
            today_meals.append({"name": splitted[0], "english_name": splitted[1]})
    return [meals_model.create(meal) for meal in today_meals]


def parse_fixed_menu():
    fixed_menus = driver.find_elements(By.XPATH, "//table[@cellpadding='2']//tr")[1:]
    for el in fixed_menus:
        no_date = False
        meals = el.find_element(By.XPATH, ".//td[@class='style18']").text.split("\n")[
            1:
        ]
        today_meals = get_meals(meals)

        nutrition_facts = el.find_elements(By.XPATH, ".//td")[-1].text
        try:
            date_el = el.find_element(By.XPATH, ".//td[@rowspan='2']").text.split("\n")
        except:
            no_date = True
            pass

        menu_object.create_or_update(
            {
                "date": datetime.strptime(date_el[0], "%d.%m.%Y").date(),
                "name": date_el[1],
                "english_name": date_el[2],
                "menu_type": "dinner" if no_date else "lunch",
                "nutrition_facts": nutrition_facts.replace("\n", " "),
                "meal_ids": today_meals,
            }
        )


def parse_alternative_menu():
    alt_menus = driver.find_elements(By.XPATH, "//table[@cellpadding='3']//tr")[1:]
    for el in alt_menus:
        meals = el.find_element(By.XPATH, ".//td[@class='style18']").text.split("\n")
        today_meals = get_meals(meals)
        date_el = el.find_elements(By.XPATH, ".//td")[0].text.split("\n")
        menu_object.create_or_update(
            {
                "date": datetime.strptime(date_el[0], "%d.%m.%Y").date(),
                "name": date_el[1],
                "english_name": date_el[2],
                "menu_type": "alternative",
                "nutrition_facts": "",
                "meal_ids": today_meals,
            }
        )


def scrap_menu():
    driver.get(url)
    parse_fixed_menu()
    parse_alternative_menu()
    driver.quit()
