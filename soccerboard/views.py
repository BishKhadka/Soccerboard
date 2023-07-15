from django.shortcuts import render, redirect
from .models import TableModel
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .serializers import TeamSerializer, TeamNameSerializer
from soccerboard.direct_scrapper import LeagueTable
from django.core.mail import send_mail
from decouple import config
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
import re

def home(request):
    '''
    Handles the home page view and redirects to stats of the team or league table depending on the form selected.
    '''

    all_leagues = {"Bundesliga":"Bundesliga", "La-Liga":"La Liga", "Ligue-1":"Ligue 1", "Premier-League":"Premier League", "Serie-A":"Serie A"}
    if request.method == 'POST':
        header_selected = request.POST.get('header_selected', '')

        if header_selected == 'Quiz':
            return redirect('quiz')
        
        elif header_selected in all_leagues:
            league = all_leagues[header_selected]
            return redirect('search_page', league)

    return render(request, 'home.html')

def quiz(request):
    '''
    Start the quiz
    '''
    return render(request, 'quiz.html')


def search_page(request, league = "Premier League"):
    '''
    Handles the home page view and redirects to stats of the team or league table depending on the form selected.
    '''
    league_logo = {"Bundesliga":"logo_bundesliga.png", "La Liga":"logo_laliga.jpeg", "Serie A":"logo_serie_a.jpeg",
                   "Premier League": "logo_pl.jpeg", "Ligue 1":"logo_ligue_1.png"}
    logo_path = "soccerboard/images/"+league_logo[league]
    team_names = TableModel.objects.filter(Competition=league).values('Team').distinct()
    if request.method == 'POST':
        form_type = request.POST.get('form_type', '')
        
        #match the form ID
        if form_type == 'search-team-button':
            team_name = request.POST.get('club_name', '')
            return redirect('stats', league_name= league, team_name=team_name)
        
        elif form_type == 'search-table-button':
            league_name = request.POST.get('leagueName', '')
            print("This is the league", league_name)
            return redirect('league_table', league_name=league_name)
    
    return render(request, 'search_page.html', {"league":league, "logopath":logo_path, "team_names":team_names})

def stats(request, league_name, team_name):
    '''
    Renders the 'stats.html' template with the statistics for the specified team.
    '''
    team_instance = TableModel.objects.filter(Team=team_name).order_by('-Date')[:5]
    opponent_instance = []
    for item in team_instance:
        opponent_instance.append(TableModel.objects.filter(Date=item.Date, Team=item.Opponent).first())
    combined_instance = zip(team_instance, opponent_instance)
    return render(request, 'stats.html', {'combined_instance': combined_instance})

def league_table(request, league_name):
    '''
    Renders the 'league_table.html' template with the table data for the specified league.
    '''
    data = LeagueTable(league_name.lower()).get_table()
    return render(request, 'league_table.html', {'data': data, 'league_name': league_name})

def contact(request):
    '''
    Renders the contact.html with server side validation and http header injection filtering. 
    Send a copy via email to the requester and the receiver
    '''
    def contains_malicious_headers(message):
        pattern = r'(Content-Type:|Bcc:|Cc:|To:|MIME-Version:|Content-Transfer-Encoding:|X-Priority:|X-MSMail-Priority:|X-Mailer:|Return-Path:|Message-ID:|X-Originating-IP:|X-Sender:|X-Authentication-Warning:|X-Yahoo-Newman-Property:|X-Yahoo-Newman-Id:|X-YMail-OSG:|X-YMail-OSG-Original-Recipient:|X-Yahoo-Filtered-Bulk:|X-Yahoo-Group-Id:|X-Yahoo-Profile:|X-YMail-User-Id:|X-YMail-Trace:|X-Originating-Email:|X-Yahoo-SMTP:|X-Yahoo-Newman-Property:|X-Yahoo-Newman-Id:|X-YMail-OSG:|X-YMail-OSG-Original-Recipient:|X-Yahoo-Filtered-Bulk:|X-Yahoo-Group-Id:|X-Yahoo-Profile:|X-YMail-User-Id:|X-YMail-Trace:|X-Originating-Email:|X-Yahoo-SMTP:)'
        if re.search(pattern, message, re.IGNORECASE):
            raise ValidationError("The input contains malicious headers")
    
    def is_not_alpha(text):
        if not re.match(r'^[a-zA-Z\s]+$', text):
            raise ValidationError("Name should contain only alphabets")

    def name_validation(errors, first, last):
        first = first.strip()
        last = last.strip()

        try:
            if not first:
                errors['first'] = 'Please enter your first name'
            else:
                is_not_alpha(first)
                contains_malicious_headers(first)
        except ValidationError:
            errors['first'] = 'First name contains invalid characters'

        try:
            if not last:
                errors['last'] = 'Please enter your last name'
            else:
                is_not_alpha(last)
                contains_malicious_headers(last)
        except ValidationError:
            errors['last'] = 'Last name contains invalid characters'
                
    def email_validation(errors, email):
        email.lower()
        email = email.strip()
        try:
            if not email:
                errors['email'] = 'Please enter your email'
            else:
                validate_email(email)
                contains_malicious_headers(email)

        except ValidationError:
            errors['email'] = 'Please enter a valid email'

    def message_validation(errors, message):
        message = message.strip()
        try:
            if not message:
                errors['message'] = 'Please enter a valid message'
            contains_malicious_headers(message)
        except ValidationError:
            errors['message'] = 'Message contains malicious headers'

    if request.method == 'POST':
        first = request.POST.get('firstName')
        last = request.POST.get('lastName')
        email = request.POST.get('email')
        message = request.POST.get('message')
        subject = request.POST.get('subject')

        #server-side validation
        errors = {}
        name_validation(errors, first, last)
        email_validation(errors, email)
        message_validation(errors, subject)
        message_validation(errors, message)

        if errors:
            return render(request, 'contact.html', {'errors': errors, 'first':first, 'last':last, 'email':email, 'message':message})
        else:
            full_name = first.strip() + " " + last.strip()
            message = f'Name:\n\t{full_name}\n Email:\n\t{email}\n Message:\n\t{message}\n'
            send_mail('RE: ' + subject, message, '', [email])

            #send email
            send_mail('Soccerboard: '+ subject, message, '', [config('EMAIL_HOST_USER')])
            return render(request, 'contact_success.html', {'full_name':full_name})

    return render(request, 'contact.html')

    


def acknowledgement(request):
    return render(request, 'acknowledgement.html')

@api_view(["GET"])
def team_list(request):
    '''
    Returns a list of distinct team names as JSON response.
    '''
    teams = TableModel.objects.values('Team').distinct()
    serializer = TeamNameSerializer(teams, many=True)
    return Response(serializer.data)


@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delete_entire_model(request):
    '''
    Deletes all model instances from the database.
    '''
    TableModel.objects.all().delete()
    return Response({'Message': 'All instances of tableModel have been deleted.'})


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def add_data(request):
    '''
    Adds a new model instance with the provided data.
    '''
    serializer = TeamSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)

@api_view(["GET"])
def all_data(request):
    '''
    Returns all data in the table as a JSON.
    '''
    teams = TableModel.objects.all()
    serializer = TeamSerializer(teams, many=True)
    return Response(serializer.data)