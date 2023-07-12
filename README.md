
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

## Languages and Tools

<a href="https://azure.microsoft.com/en-in/" target="_blank" rel="noreferrer"><img src="https://www.vectorlogo.zone/logos/microsoft_azure/microsoft_azure-icon.svg" alt="azure" width="40" height="40"/> </a> 
<a href="https://getbootstrap.com" target="_blank" rel="noreferrer"> <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/bootstrap/bootstrap-plain-wordmark.svg" alt="bootstrap" width="40" height="40"/> </a> 
<a href="https://www.w3schools.com/css/" target="_blank" rel="noreferrer"> <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/css3/css3-original-wordmark.svg" alt="css3" width="40" height="40"/> </a> 
<a href="https://www.djangoproject.com/" target="_blank" rel="noreferrer"> <img src="https://cdn.worldvectorlogo.com/logos/django.svg" alt="django" width="40" height="40"/> 
</a> <a href="https://git-scm.com/" target="_blank" rel="noreferrer"> <img src="https://www.vectorlogo.zone/logos/git-scm/git-scm-icon.svg" alt="git" width="40" height="40"/> </a> 
<a href="https://www.w3.org/html/" target="_blank" rel="noreferrer"> <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/html5/html5-original-wordmark.svg" alt="html5" width="40" height="40"/> </a> 
<a href="https://developer.mozilla.org/en-US/docs/Web/JavaScript" target="_blank" rel="noreferrer"> <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/javascript/javascript-original.svg" alt="javascript" width="40" height="40"/> </a> 
<a href="https://pandas.pydata.org/" target="_blank" rel="noreferrer"> <img src="https://raw.githubusercontent.com/devicons/devicon/2ae2a900d2f041da66e950e4d48052658d850630/icons/pandas/pandas-original.svg" alt="pandas" width="40" height="40"/> </a> 
<a href="https://www.postgresql.org" target="_blank" rel="noreferrer"> <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/postgresql/postgresql-original-wordmark.svg" alt="postgresql" width="40" height="40"/> </a> 
<a href="https://postman.com" target="_blank" rel="noreferrer"> <img src="https://www.vectorlogo.zone/logos/getpostman/getpostman-icon.svg" alt="postman" width="40" height="40"/> </a> 
<a href="https://www.python.org" target="_blank" rel="noreferrer"> <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/python/python-original.svg" alt="python" width="60" height="40"/> </a><a href="https://www.django-rest-framework.org" target="_blank" rel="noreferrer"> <img src="https://www.django-rest-framework.org/img/logo.png" alt=“djangorestframework” width="80" height="60"/> </a>
<a href="https://www.nginx.com" target="_blank" rel="noreferrer"> <img src="https://download.logo.wine/logo/Nginx/Nginx-Logo.wine.png" alt=“Ngnix” width="80" height="60"/> </a>
<a href="https://gunicorn.org" target="_blank" rel="noreferrer"> <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/0/00/Gunicorn_logo_2010.svg/1280px-Gunicorn_logo_2010.svg.png" alt=“gunicorn width="100" height="60"/></a>

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

- Version control skills

- Web scraping skills

- Automation skills


## Other Projects

Checkout some of my other projects [here](https://github.com/BishKhadka). 


## 🔗 Connect
[![linkedin](https://img.shields.io/badge/linkedin-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/khadka-bishal/)

