# Copyright 2023 Yiğit Budak (https://github.com/yibudak)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from datetime import datetime
from selenium.webdriver.common.by import By
from backend import models, conf
from backend.models.daily_menus import meal_menu_rel


menu_object = models.env["daily_menus"]
meals_model = models.env["meals"]
nutrition_facts_model = models.env["nutrition_facts"]


def get_meals(meals):
    """
    Create meals and return them.
    """
    today_meals = []
    for single in meals:
        for single2 in single.split(" veya / or "):
            splitted = single2.split(" / ")
            today_meals.append({"name": splitted[0], "english_name": splitted[1]})
    return [meals_model.create(meal) for meal in today_meals]


def update_meals_sequence(menu, meals):
    """
    Keep the sequence of meals.
    """
    for idx, meal in enumerate(meals):
        rel = models.db.session.query(meal_menu_rel).filter_by(
            meal_id=meal.id, menu_id=menu.id
        )
        rel.update({"sequence": idx})

    return True


def parse_fixed_menu(driver):
    """
    Parse the fixed menu.
    """
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

        created_menu = menu_object.create_or_update(
            {
                "date": datetime.strptime(date_el[0], "%d.%m.%Y").date(),
                "name": date_el[1],
                "english_name": date_el[2],
                "menu_type": "dinner" if no_date else "lunch",
                "meal_ids": today_meals,
            }
        )
        nutrition = nutrition_facts.split("\n")
        nutrition_facts_model.create_or_update(
            {
                "energy": nutrition[1],
                "carbohydrate": nutrition[2].split("Karbonhidrat / Carbohydrate: ")[1],
                "protein": nutrition[3].split("Protein / Protein: ")[1],
                "fat": nutrition[4].split("Yağ / Fat:")[1],
                "menu_id": created_menu.id,
            }
        )
        update_meals_sequence(created_menu, today_meals)


def parse_alternative_menu(driver):
    """
    Alternative menus are not in the same table as fixed menus. So we need to
    parse them separately also alternative menus are not in the same format
    as fixed menus. In example, there is no nutrition facts for alternative
    menus.
    """
    alt_menus = driver.find_elements(By.XPATH, "//table[@cellpadding='3']//tr")[1:]
    for el in alt_menus:
        meals = el.find_element(By.XPATH, ".//td[@class='style18']").text.split("\n")
        today_meals = get_meals(meals)
        date_el = el.find_elements(By.XPATH, ".//td")[0].text.split("\n")
        created_menu = menu_object.create_or_update(
            {
                "date": datetime.strptime(date_el[0], "%d.%m.%Y").date(),
                "name": date_el[1],
                "english_name": date_el[2],
                "menu_type": "alternative",
                "meal_ids": today_meals,
            }
        )
        update_meals_sequence(created_menu, today_meals)


def scrap_menu():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(
        options=chrome_options, executable_path=conf.app.CHROMEDRIVER_PATH
    )
    url = "http://kafemud.bilkent.edu.tr/monu_eng.html"
    driver.get(url)
    parse_fixed_menu(driver)
    parse_alternative_menu(driver)
    driver.quit()
