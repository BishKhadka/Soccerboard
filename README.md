
# Soccerboard

Soccerboard is a responsive web application build in Python using Django framework. You can play soccer trivia, get latest match stats of your favorite teams in top 5 league and also view the current league table.



## Description

Webscraping is the integral part of this project. The data for the league tables are scraped from the web using BeautifulSoup library and served to the user directly without storing in the database. The stats, however, are stored in the PostgreSQL database and are queried from the Django models using Django ORM commands. The data collection process for stats runs automatically at 7 am every morning using APScheduler. To speed up the data collection and avoid memory leaks, the project uses parallel programming and threading techniques. Function-based views are predominantly used rather than class based views to avoid a lot of abstraction.


The templates follow a well-structured approach. The project uses a base template that contains the common elements of the web pages such as HTML introduction and Bootstrap. The other templates extend the base template and add their own content. The static files, such as CSS and JavaScript, are stored in a separate folder following the industry standards to facilitate static file collection during deployment.

The project also provides APIs for users to access the data about the teams using function-based views. The APIs return JSON responses that contain the team name, rank, points, goals scored, goals conceded, etc. 

The project follows the Python PEP 8 conventions for code style and formatting. The code is well commented and documented using docstrings and comments.
## Deployment

The project is deployed on an Azure Virtual Machine by using Gunicorn as the Python WSGI server to run the web application. I use Nginx as reverse proxy and PostgreSQL as a database backend. I have used industry-wide best practices to protect the sensitive information that might otherwise be leaked to the website visitors. 

Here is the link to the website on my
[studio](http://bishalkhadka.studio/soccer/). 

## API Reference
I used Django REST Framework to create REST APIs and execute CRUD operations.

#### Get all data
Returns all the data of all the teams in top 5 league

```http
  GET /api/all-data/
```


#### Get team names
Returns the names of all the clubs in top 5 league
```http
  GET /api/teams/
```

#### Post results
Create data and add it to the model (requires admin privilege)

```http
  POST /api/add/
```

#### Remove model
Remove the entire model (requires admin privilege)


```http
  DELETE /api/delete-entire-model/
```

## Tech Stack

**Front-end**: HTML, CSS, Bootstrap, JavaScript

**Back-end**: Python, Django, Django REST Framework

**Database**: PostgreSQL

**API Testing**: Postman

**Deployment**: Azure, Ngnix, Gunicorn

**Version Control**: GitHub




## 🛠 Skills

I learnt these skills through this project. 

- Full-stack web development skill

- Cloud computing skills

- API testing skills

- Web scraping skills

- Automation skills


## Other Projects

Checkout some of my other projects [here](https://github.com/BishKhadka). 


## 🔗 Connect
[![linkedin](https://img.shields.io/badge/linkedin-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/khadka-bishal/)

