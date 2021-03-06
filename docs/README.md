# nets213-project
NETS 213 Final Project

# Concepts
- Users
    - general userbase for both asking questions and providing recommendations
    - can sign up, login
    - have some reputation and individual profile information 
- Questions
    - Asked by users
    - Have topics
    - Can be upvoted/downvoted (only once per each user)
    - Can mark as spam (only once per each user)
- Recommendations
    - Provided by other users
    - Can be upvoted/downvoted by other users (only once per each user)
    - Can mark as spam (only once per each user)
    - Original asker can select best answer/recommendation
- Aggregation
    - Upvote/downvote system to organize recommendations (only once per each user)
    - sort recommendations from highest to lowest net votes (upvotes - downvotes)
- Quality Control (spam)
    - Users can mark questions or recommendations as spam
    - Threshold limit to determine if posts should be hidden or deleted
- Quality Control (voting)
    - Each user can vote on questions and recommendations (+1/-1)
    - Crowd ensures quality of other users' answers and helps original answer see the "best" answers more naturally

# Major Components
- Frontend
    - Sign Up / Login (1)
    - Profile (2)
        - Adding interface to edit bio 
        - Upload picture
        - Show Guru status/leaderboard rankings
        - Recent recommendations / questions
        - Reputation
    - Homepage / News feed of questions (3)
    - Asking questions (2)
    - Providing/viewing recommendations (2)
- Backend
    - Designing database for Users, Questions, Recommendations (2)
    - Aggregation of Questions and Recommendations (1)
    - Quality Control (voting system) (1)
    - Quality Control (spam) (1)

Total points: 15

# Data
Our current sample data format is in JSON in order to preload information for the QC/Aggregation module in Final Project Part 2 Deliverable 2. However, our final implementation will rely on a backend SQL/Django database in which we will utilize database calls to feed input into our methods using Django's ORM. Each user, recommendation, and question are represented as classes inheriting from Django's base model. As such, using JSON is purely for proof of concept. Below is our schema for our users, questions, and recommendation objects.

User
- username (unique identifier)
- password
- achievements [list of "top guru" etc]
- profile info
    - birthday
    - firstname, lastname
    - bio
    - affiliation
- recommendations
- questions
- news feed
- favorite fields/interests (e.g. Music, DARPA funding)

Question
- author
- title :string
- description :string
- field (general, e.g. Music)
- timestamp
- upvotes
- downvotes
- current preferences
- tags [optional] (more specific)
- is_resolved? bool [OP marked it ]
- recommendations[foreign key: Answer]
- spam_counts (how many times marked as spam)

Recommendation
- question (original question)
- timestamp
- author
- recommendation
- upvotes
- downvotes
- spam_counts (how many times marked spam)
- is_star? bool

For CrowdGuru, our QC and aggregation modules are intrinsically intertwined. We use the crowd to both do quality control as well as aggregation. More specifically, we plan to implement an upvote/downvote system for both questions and recommendations. We will sort the questions/recommendations based on their net upvotes. Users will see the highest quality questions on their newsfeeds and the highest quality recommendations will be listed on the top of their respective question feed. Additionally each question and recommendation post will have an associated "mark as spam" label in which users can filter out spam posts (after a certain threshold of spam counts, the post will be hidden). Finally the original author of the question can select a particular recommendation as the best using the "is_star" label. In terms of aggregation, we will implement a machine learning algorithm to match questions with their most relevant gurus. This ensures that users' newsfeeds will be populated by questions that they are most qualified to answer. Aggregation will also be done on the recommendation level through question newsfeeds which displays all of the recommendations for that given question. 

# Quality Control / Aggregation
In the src/ directory, qc_aggregation.py contains our combined quality control + aggregation module.

Aggregation:
- add_recommendation: adds a recommendation object/dict to a question.
- storing the recommendation_ids in each question
- add_to_news_feed: adds the question to a person's news feed

Quality Control:
- upvote: allows users to upvote any question or recommendation, signifying the question/rec has a high quality
- downvote: allows users to downvote any question or recommendation, signifying the question/rec has a low quality
- mark_as_star: allows the original author of the question to select the best recommendation of all of them
- mark_as_spam: allows a user to mark a recommendation as spam, which increments the number of spam counts. Once the number of spam counts goes over the spam threshold of a post, the recommendation is hidden as spam.

