from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect, render_to_response
from django.http import HttpResponseRedirect
from django.core.context_processors import csrf
from .models import User, Question, Recommendation, Category, Achievement, Item, QuestionVote, RecommendationVote, QuestionSpamVote, RecommendationSpamVote

from django.contrib.auth import authenticate, login, logout

from IPython import embed
import json

# Create your views here.

def index(request):
    if not request.user.is_authenticated():
        return render(request, 'registration/registration_form.html')
    return redirect('profile')


def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        if not User.objects.filter(username=username).exists():
            user = User.objects.create_user(username, email=None, password=password)
            user.save()
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('profile')
        else:
            # username exists
            print 'username already exists'
            return render(request, 'registration/registration_form.html', {'error': 'Username exists'})
    else:
        return render(request, 'registration/registration_form.html')



def log_in(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    if user is not None:
        # password is verified
        login(request, user)
        return redirect('profile')
    else:
        context = {'error': 'Incorrect login information.'}
        return render(request, 'registration/registration_form.html', context)

def log_out(request):
    if not request.user.is_authenticated():
        redirect('index')
    logout(request)
    return redirect('index')


def show_user(request, id):
    if not request.user.is_authenticated():
        redirect('index')
    context = {'questions': [{'votes': sum(x.value for x in question.questionvote_set.all()), 'title': question.title, 'description':question.description, 'category': question.category.name, 'created_at': question.created_at, 'id': question.id} for question in Question.objects.all()], 'username': User.objects.get(pk=id).username}
    return render(request, 'profile.html', context)

def profile(request):
    if not request.user.is_authenticated():
        return redirect('index')
    context = {'questions': sorted([{'votes': sum(x.value for x in question.questionvote_set.all()), 'title': question.title, 'description':question.description, 'category': question.category.name, 'created_at': question.created_at, 'id': question.id} for question in Question.objects.all()], key=lambda x: x['votes'], reverse=True)}
    return render(request, 'profile.html', context)

def show_question(request, id):
    if not request.user.is_authenticated():
        redirect('index')
    '''shows recommend window for a given question'''
    question = Question.objects.get(pk=id)
    category = {'name': question.category.name, 'id': question.category.id}
    preferences = json.loads(question.preferences)
    tags = json.loads(question.tags)
    author = {'username': question.author.username, 'id': question.author.id}
    recommendations = []
    # embed()
    for r in question.recommendation_set.all():
        votes = sum(x.value for x in r.recommendationvote_set.all())
        spam_votes = len(r.recommendationspamvote_set.all())
        if spam_votes <= 5:
            recommendations.append({'created_at': r.created_at, 'spam_counts': spam_votes, 'is_star': r.is_star, 'id': r.id, 'author': {'username': r.author.username, 'id': r.author.id}, 'recommendation': r.recommendation, 'net_votes': votes})
    recommendations.sort(key=lambda x: x['net_votes'], reverse=True)
    # embed()
    votes = sum(x.value for x in question.questionvote_set.all())
    spam_votes = len(question.questionspamvote_set.all())
    context = {'category': category, 'title': question.title, 'author': author,
               'description': question.description, 'preferences': preferences,
               'is_resolved': question.is_resolved, 'tags': tags,
               'preferences': preferences, 'recommendations':recommendations,
               'net_votes': votes, 'spam_votes': spam_votes, 'id': question.id}
    return render(request, 'question.html', context)

def upvote_question(request):
    ''' Upvote given question_id '''
    # embed()
    question = Question.objects.get(pk=int(request.POST['question_id']))
    if question.questionvote_set.filter(user=request.user).exists():
        vote = question.questionvote_set.filter(user=request.user).all()[0]
        if vote.value == -1:
            vote.delete()
    else:
        vote = QuestionVote(user=request.user, question=question, value=1)
        vote.save()
    return redirect(question)

def downvote_question(request):
    ''' downvote given question_id '''
    question = Question.objects.get(pk=int(request.POST['question_id']))
    if question.questionvote_set.filter(user=request.user).exists():
        vote = question.questionvote_set.filter(user=request.user).all()[0]
        if vote.value == 1:
            vote.delete()
    else:
        vote = QuestionVote(user=request.user, question=question, value=-1)
        vote.save()

    return redirect(question)

def upvote_recommendation(request):
    ''' Upvote given recommendation_id '''
    recommendation = Recommendation.objects.get(pk=int(request.POST['recommendation_id']))
    if recommendation.recommendationvote_set.filter(user=request.user).exists():
        vote = recommendation.recommendationvote_set.filter(user=request.user).all()[0]
        if vote.value == -1:
            vote.delete()
    else:
        vote = RecommendationVote(user=request.user, recommendation=recommendation, value=1)
        vote.save()
    return redirect(recommendation.question)

def downvote_recommendation(request):
    ''' Downvote given recommendation_id '''
    recommendation = Recommendation.objects.get(pk=int(request.POST['recommendation_id']))
    if recommendation.recommendationvote_set.filter(user=request.user).exists():
        vote = recommendation.recommendationvote_set.filter(user=request.user).all()[0]
        if vote.value == 1:
            vote.delete()
    else:
        vote = RecommendationVote(user=request.user, recommendation=recommendation, value=-1)
        vote.save()

    return redirect(recommendation.question)

def spam_question(request):
    question = Question.objects.get(pk=int(request.POST['question_id']))
    if not question.questionspamvote_set.filter(user=request.user).exists():
        vote = QuestionSpamVote(user=request.user, question=question)
        vote.save()
    return redirect(question)

def spam_recommendation(request):
    recommendation = Recommendation.objects.get(pk=int(request.POST['recommendation_id']))
    if not recommendation.recommendationspamvote_set.filter(user=request.user).exists():
        vote = RecommendationSpamVote(user=request.user, recommendation=recommendation)
        vote.save()
    return redirect(recommendation.question)

def show_ask_question(request):
    return render(request, 'ask_question.html')

def post_question(request):
    # embed()
    d = dict(request.POST)
    num_interests = len(d) - 4
    interests = []
    for i in range(1, num_interests + 1):
        # interest_i
        interests.append(request.POST['interest_{}'.format(i)])
    query_set = Category.objects.filter(name__iexact=request.POST['category'])
    if query_set.exists():
        category = query_set.all()[0]
    else:
        category = Category(name=request.POST['category'])
        category.save()
    question = Question(author=request.user, title=request.POST['title'], description=request.POST['description'], category=category, preferences=json.dumps(interests), tags='[]', is_resolved=False)
    question.save()
    return redirect(question)


def add_recommendation(request):
    if 'recommendation' in request.POST:
        question = Question.objects.get(pk=int(request.POST['question_id']))
        author = request.user
        recommendation_text = request.POST['recommendation']
        recommendation = Recommendation(question=question, author=author, recommendation=recommendation_text, is_star=False)
        recommendation.save()
    return redirect(question)


def export_questions(request):
    data = []
    for question in Question.objects.all():
        net_votes = sum(x.value for x in question.questionvote_set.all())
        num_recommendations = len(question.recommendation_set.all())
        data.append((net_votes, num_recommendations))
    return render(request, 'export.html', {'data': data})


# def register(request):
#     if request.method == 'POST':
#         form = UserCreationForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect(request, '/accounts/register/complete')

#     else:
#         form = UserCreationForm()
#     token = {}
#     token.update(csrf(request))
#     token['form'] = form

#     return render_to_response('registration/registration_form.html', token)


# def registration_complete(request):
#     return render_to_response('registration/registration_complete.html')

