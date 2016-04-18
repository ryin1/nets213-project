import json
import os

user1 = {'username': 'ccb', 'reputation': 9001}
user2 = {'username': 'epav', 'reputation': 400}
user3 = {'username': 'ryin', 'reputation': 0}
user4 = {'username': 'jmeng', 'reputation': 0}
user5 = {'username': 'neilwei', 'reputation': -10}

question1 = {'author': user2, 'title': "Best way to get funding?", 'description': 'I need funding for my research project in NETS213. It is very interesting but I can\'t make progress without my money', 'field': 'Research', 'upvotes': 0, 'downvotes': 0, 'timestamp': 1, 'preferences': [], 'tags': ['funding'], 'is_resolved': False, 'recommendation_ids': []}

rec1 = {'id': 1, 'question': question1, 'author': user1, 'timestamp': 2, 'recommendation': 'Apply for grants here: http://www.darpa.mil/work-with-us/opportunities. Also, bake cookies. -CCB', 'upvotes': 0, 'downvotes': 0, 'spam_counts': 0, 'is_star': False}

rec2 = {'id': 2, 'question': question1, 'author': user3, 'timestamp': 3, 'recommendation': 'DARPA is EVIL!', 'upvotes': 0, 'downvotes': 0, 'spam_counts': 0, 'is_star': False}

rec3 = {'id': 3, 'question': question1, 'author': user3, 'timestamp': 3, 'recommendation': 'Hire a burglar to invade Wells Fargo to obtain currency.', 'upvotes': 0, 'downvotes': 0, 'spam_counts': 0, 'is_star': False}

rec4 = {'id': 4, 'question': question1, 'author': user5, 'timestamp': 16, 'recommendation': 'It\'s probably your best bet to set up a booth on a street corner and solicit donations. People are very generous to academic researchers!', 'upvotes': 1, 'downvotes': 1, 'spam_counts': 0, 'is_star': False}

rec5 = {'id': 5, 'question': question1, 'author': user5, 'timestamp': 16, 'recommendation': "Why not take advantage of crowdsourcing to fund your crowdsourcing project? I'm sure people will be happy to fund your project! Try a site like this one: https://www.gofundme.com/", 'upvotes': 1, 'downvotes': 1, 'spam_counts': 0, 'is_star': False}

recommendations = [rec1, rec2, rec3, rec4, rec5]

# We can use this code to load from input. However, we found it easier to just work with all of the references already linked as defined in the python file here.

# question1 = json.load(open(os.path.join('..', 'data', 'question1_input.json'), 'r'))
# rec1, rec2, rec3, rec4, rec5 = json.load(open(os.path.join('..', 'data', 'recommendations_output.json'), 'r'))
# question1 = rec1['question']


def add_recommendation(question, recommendation):
    '''Aggregation: adding a recommendation to question'''
    question['recommendation_ids'].append(recommendation['id'])

def add_to_news_feed(question, news_feed):
    news_feed.append(question)

def upvote(post, user):
    '''user: user who upvoted the post
    post: post dict/object'''
    post['upvotes'] += 1
    post['author']['reputation'] += 1

def downvote(post, user):
    '''user: user who upvoted the post
    post: post dict/object'''
    post['downvotes'] += 1
    post['author']['reputation'] -= 1

def mark_as_star(recommendation, author):
    if recommendation['question']['author']['username'] == author['username']:
        recommendation['is_star'] = True
        recommendation['question']['is_resolved'] = True
        return 'Success'
    else:
        return 'Author is not original author of question'


def mark_as_spam(recommendation, user):
    '''QC: user marks recommendation as spam'''
    recommendation['spam_counts'] += 1

for rec in [rec1, rec2, rec3, rec4, rec5]:
    add_recommendation(question1, rec)

upvote(question1, user3)
upvote(question1, user4)
upvote(question1, user5)

upvote(rec1, user5)
downvote(rec1, user4)
upvote(rec1, user3)

downvote(rec2, user4)
downvote(rec2, user5)
downvote(rec2, user1)
downvote(rec2, user2)

downvote(rec3, user1)
downvote(rec3, user2)
downvote(rec3, user3)
downvote(rec3, user4)

upvote(rec3, user1)
upvote(rec3, user2)
upvote(rec3, user3)
upvote(rec3, user5)

mark_as_spam(rec2, user2)
mark_as_spam(rec2, user4)

assert('Author is not original author of question' == mark_as_star(rec1, user1))
assert(not question1['is_resolved'])

assert('Success' == mark_as_star(rec1, user2))

json.dump(question1, open(os.path.join('..', 'data', 'question1_output.json'), 'w'))
json.dump(recommendations, open(os.path.join('..', 'data', 'recommendations_output.json'), 'w'))

assert(question1['is_resolved'])