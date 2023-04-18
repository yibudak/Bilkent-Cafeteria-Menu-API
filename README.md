
![Logo](./assets/banner.jpg)


# Bilkent Cafeteria Menu API

This project is designed to publish the weekly food list of Bilkent Cafeterias Management in a user-friendly way via a REST API.

Important note: This project is not affiliated with Bilkent Cafeterias Management.

## Features

- Parse HTML content according to the SQLAlchemy ORM structure.
- Stores daily meals, nutritional values in a database.
- Transmits this data to the user via REST API.

## Requirements
- Linux (Ubuntu 20.04 preferred)
- Selenium with ChromeDriver
- Python 3+ (Python 3.11 preferred)
- MariaDB or MySQL (database)
- Virtual environment with Gunicorn installed. (WSGI)
- Nginx or Apache (reverse proxy)
## Installation

Clone the repo and install dependencies

```bash
  git clone https://github.com/yibudak/Bilkent-Cafeteria-Menu-API
  cd Bilkent-Cafeteria-Menu-API
  python3 -m venv venv
  source ./venv/bin/activate
  python3 -m pip install -r requirements.txt
```

Import Database structure

```bash
  mysql -u root -p < ./database/base.sql
```


Configuration file deployment

```bash
  sudo nano /etc/bilkent_cafeteria_menu_api.conf
  
  EXAMPLE:
  
    [DB]
    SQLALCHEMY_DATABASE_URI = mysql://user:pass@127.0.0.1/bilkentkafemud_db?charset=utf8mb4
    
    [APP]
    API_KEY = YOUR_API_KEY
```

And deploy the application with Gunicorn and reverse proxy...
## API Reference

#### Get weekly food list

```http
  GET /getWeeklyMenu
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `apiKey` | `string` | **Required**. Your API key |

![Example Data](./assets/json_visual.jpg)

#### Parse the menu

```http
  GET /parseMenu
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `apiKey` | `string` | **Required**. Your API key |

## Database structure

![Database structure](./assets/database_diagram.png)


## Authors

- [@yibudak](https://www.github.com/yibudak)


## License

[GNU Affero General Public License v3.0](https://github.com/yibudak/Bilkent-Cafeteria-Menu-API/blob/main/LICENSE)

## Contributing

Contributions are always welcome!

If you encounter an error, you can leave a message in the issue section. We also welcome pull requests to add new features or bug-fixes.

Make sure to use the [Black](https://black.readthedocs.io/en/stable/the_black_code_style/current_style.html) code style when writing your code.