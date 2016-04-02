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
    - Can be upvoted/downvoted
- Recommendations
    - Provided by other users
    - Can be upvoted/downvoted by other users
    - Original asker can select best answer/recommendation
- Aggregation
    - Upvote/downvote system to organize recommendations
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
