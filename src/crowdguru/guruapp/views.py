from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect, render_to_response
from django.http import HttpResponseRedirect
from django.core.context_processors import csrf
from .models import User, Question, Recommendation, Category, Achievement, Item, QuestionVote, RecommendationVote, QuestionSpamVote, RecommendationSpamVote, UserDetails

from django.contrib.auth import authenticate, login, logout

from django.utils import timezone

from IPython import embed
import json
from datetime import datetime
from math import log
from collections import defaultdict
import csv                                                                  


# Create your views here.


CACHED_USER_POINTS = {}

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
    context = {}
    this_user = User.objects.get(pk=id)
    ud_query = UserDetails.objects.filter(user=this_user)
    if not ud_query:
        user_details = UserDetails(user=this_user)
        user_details.save()
        print 'Made new user details for ', this_user.username
    else:
        user_details = ud_query[0]
    context['interests'] = user_details.interests
    context['details'] = user_details
    return render(request, 'profile.html', context)

def profile(request):
    if not request.user.is_authenticated():
        return redirect('index')
    context = {'questions': [{'votes': sum(x.value for x in question.questionvote_set.all()), 'title': question.title, 'description':question.description, 'category': question.category.name.strip(), 'created_at': question.created_at, 'id': question.id, 'author': question.author, 'num_recs': len(question.recommendation_set.all())} for question, score in ranked_questions(request.user)]}
    ud_query = UserDetails.objects.filter(user=request.user)
    if not ud_query:
        user_details = UserDetails(user=request.user)
        user_details.save()
        print 'Made new user details for ', request.user.username
    else:
        user_details = ud_query[0]
    context['interests'] = user_details.interests
    context['details'] = user_details
    return render(request, 'profile.html', context)

def all_questions(request):
    if not request.user.is_authenticated():
        return redirect('index')
    context = {'questions': sorted([{'votes': sum(x.value for x in question.questionvote_set.all()), 'title': question.title, 'description':question.description, 'category': question.category.name.strip(), 'created_at': question.created_at, 'id': question.id, 'author': question.author} for question in Question.objects.all()], key=lambda x: x['votes'], reverse=True)}
    
    return render(request, 'all_questions.html', context)

def edit_profile(request):
    if not request.user.is_authenticated():
        return redirect('index')
    ud_query = UserDetails.objects.filter(user=request.user)
    if not ud_query:
        user_details = UserDetails(user=request.user)
        user_details.save()
        print 'Made new user details for ', request.user.username
    else:
        user_details = ud_query[0]
    # interests = ' ,'.join([category.name for category in user_details.interests.all()])
    interests = user_details.interests
    # birthday = '{}-{}-{}'.format(user_details.birthday.year, user_details.birthday.month, user_details.birthday.day)
    return render(request, 'update_profile.html', {'details': user_details, 'interests': interests})


# BIO

def update_profile(request):
    if not request.user.is_authenticated():
        redirect('index')
    new_info = {}
    user_details = UserDetails.objects.filter(user=request.user)[0]
    fields = ['email', 'firstname', 'lastname', 'bio', 'location', 'interests']
    # embed()
    for field in fields:
        new_info[field] = request.POST.get(field) or getattr(user_details, field)
    # embed()
    if request.POST.get('birthday'):
        new_info['birthday'] = datetime.strptime(request.POST.get('birthday'), '%Y-%M-%d')

    for k, v in new_info.items():
        setattr(user_details, k, v)
    user_details.save()
    return redirect('profile')


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
    best_recommendation = None
    for r in question.recommendation_set.all():
        votes = sum(x.value for x in r.recommendationvote_set.all())
        spam_votes = len(r.recommendationspamvote_set.all())
        if r.is_star:
            best_recommendation = {'created_at': r.created_at, 'spam_counts': spam_votes, 'is_star': r.is_star, 'id': r.id, 'author': {'username': r.author.username, 'id': r.author.id}, 'recommendation': r.recommendation, 'net_votes': votes}
        elif spam_votes <= 5:
            recommendations.append({'created_at': r.created_at, 'spam_counts': spam_votes, 'is_star': r.is_star, 'id': r.id, 'author': {'username': r.author.username, 'id': r.author.id}, 'recommendation': r.recommendation, 'net_votes': votes})
        
    recommendations.sort(key=lambda x: x['net_votes'], reverse=True)
    # embed()
    votes = sum(x.value for x in question.questionvote_set.all())
    spam_votes = len(question.questionspamvote_set.all())
    context = {'best': best_recommendation, 'category': category, 'title': question.title, 'author': author,
               'description': question.description, 'preferences': preferences,
               'is_resolved': question.is_resolved, 'tags': tags,
               'preferences': preferences, 'recommendations': recommendations,
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


def star_recommendation(request):
    recommendation = Recommendation.objects.get(pk=int(request.POST['recommendation_id']))
    if request.user.username == recommendation.question.author.username:
        # make sure that all recommendations of the question are not starred
        if not recommendation.question.recommendation_set.filter(is_star=True).exists():
            # none are starred yet
            recommendation.is_star = True
            recommendation.save()
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

# LEADERBOARDS


def show_leaderboards(request):
    if not request.user.is_authenticated():
        redirect('index')
    category_top_users = get_leaderboards()[0]
    leaderboards = [{'category': category, 'users': [(User.objects.get(pk=user[0]), user[1]) for user in users[:5]]} for category, users in category_top_users.items()]
    # break up leaderboards into 4-size chunks
    results = [leaderboards[i:i + 4] for i in xrange(0, len(leaderboards), 4)]
    # embed()
    return render(request, 'leaderboards.html', {'results': results})

def get_leaderboards():
    user_points = defaultdict(dict)
    category_top_users = defaultdict(dict)
    user_ids = [user.id for user in User.objects.all()]
    for category in Category.objects.all():
        if not category.name:
            continue
        # calc each users stuff
        for question in category.question_set.all():
            for recommendation in question.recommendation_set.all():
                votes = sum(x.value for x in recommendation.recommendationvote_set.all())
                if category.name in user_points[recommendation.author.id]:
                    user_points[recommendation.author.id][category.name] += votes + 1
                else:
                    user_points[recommendation.author.id][category.name] = votes + 1
        res = sorted([(user_id, user_points[user_id][category.name]) for user_id in user_ids if category.name in user_points[user_id]], key=lambda x: x[1], reverse=True)
        if res:
            category_top_users[category.name] = res
    CACHED_USER_POINTS = user_points
    return (category_top_users, user_points)


def ranked_questions(user):
    '''
    algorithm for ranking questions.
    user is a User object
    '''
    questions = Question.objects.all()
    interests = get_interests(user)
    ranked_list = [(q, hot(q, user, interests)) for q in questions]
    res =  sorted(ranked_list, key=lambda x: x[1], reverse=True)[:15]
    # embed()
    return res

def get_interests(user):
    ud_query = UserDetails.objects.filter(user=user)
    if not ud_query:
        user_details = UserDetails(user=user)
        user_details.save()
        print 'Made new user details for ', user.username
    else:
        user_details = ud_query[0]
    return [x.lower() for x in user_details.interests.split(', ')]


def epoch_seconds_delta(date):
    # 1451606400 = epoch timestamp for 1/1/2016 00:00:00

    td = date - datetime(1970, 1, 1, tzinfo=timezone.utc)
    return (td.days * 86400 + td.seconds + (float(td.microseconds) / 1000000)) - 1460319408

def adjusted_votes(question):
    # adj_votes(question) = quesiton's net_votes + 2 * (# recommendations)
    net_votes = sum(x.value for x in question.questionvote_set.all())
    return net_votes + 2 * len(question.recommendation_set.all()) + 3

def hot(question, user, interests):
    # f(q, user) = log_2(influence(user, c)) * log_1.5(adjusted_votes(question) + 2*question.|recommendations| + t/45000)
    s = adjusted_votes(question)
    global CACHED_USER_POINTS
    if not CACHED_USER_POINTS:
        CACHED_USER_POINTS = get_leaderboards()[1]
    category_lc = question.category.name.lower()
    adj_influence = log((CACHED_USER_POINTS[user.id].get(question.category.name, 0) + 4), 2)

    if category_lc in interests:
        adj_influence *= 1.5
        # print 'category:',category_lc, 'is a match'
        # embed()


    order = log(max(abs(s), 1), 1.5)
    if s >= 0:
        sign = 1
    elif s < 0:
        sign = -1

    seconds = epoch_seconds_delta(question.created_at)
    # print 'adj votes:', s,'adj inf', adj_influence, 'sign',sign, 'order', order, 't/45000', seconds / 45000, '=> actual result: ', round(adj_influence * sign * order + seconds / 45000, 7)
    return round(adj_influence * sign * order + seconds / 45000, 7)




# EXPORT


def export_questions(request):
    data = []
    for question in Question.objects.all():
        net_votes = sum(x.value for x in question.questionvote_set.all())
        num_recommendations = len(question.recommendation_set.all())
        data.append((net_votes, num_recommendations))
    return render(request, 'export.html', {'data': data})

def export_skills_data():
    user_points = get_leaderboards()[1]
    data = {key: sorted(vals.values(), reverse=True) for key, vals in user_points.items()}
    with open('skills_data.csv', 'w') as csvfile:
        fieldnames = ['total rep over categories', 'rep1', 'rep2', 'rep3', 'other']
        writer = csv.writer(csvfile)
        writer.writerow(fieldnames)
        for lst in data.values():
            writer.writerow([sum(lst)] + sorted(lst[:3], reverse=True))
    return 'Success! check skills_data.csv'
