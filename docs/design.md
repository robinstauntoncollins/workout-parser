# MVP

User will keep track of their workout in a text file (Google Keep for example) and when completed the user
will upload that text file to the web app which will automatically parse and store the workout accurately.

The app will then be able to keep track of the day, exercises, sets, reps etc of the user over time.


# Future

* Calendar to show the user when they completed a workout
* Some way to integrate with Google Keep/Docs to automatically retrieve uploaded workouts
* Also push measurement entries (eg. weight)


# Database Schema Design
User:
    id: INT
    username: TEXT
    email: TEXT
    password: TEXT
    workouts: INT; FK reference to workouts that have this user's Id

Workout:
    id: INT
    date: DATE (UTC)
    user_id: INT; Id of the user who logged this workout
    
Exercise Log Entry:
    id: INT
    workout_id: INT ; Id of the workout this section belongs to
    exercise_id: INT
    section: TEXT; Eg. Warmup, Strength, Core
    set_number: INT
    reps: INT
    weight: FLOAT; Eg. 7.5kg
    hold: INT; seconds held position for
    rest: int; eg. 90 seconds

Exercise:
    id: INT
    name: TEXT
    description: TEXT
    FK variation_id: INT
    FK equipment_id: INT
    FK category_id: INT
    Eg. Pullups, Rollouts, Squat, Dips, 

Exercise Variation:
    id: INT
    name: TEXT
    description: TEXT
    difficulty: INT
    Eg. unmodified, assisted, beginner, negatives, weighted, L-sit, Shrimp

Exercise Equipment:
    id: INT
    name: TEXT
    Eg. Rings, Bar, Ab wheel

Exercise Category: (which part of body does this exercise use?)
    id: INT
    name: TEXT
    Eg. Push, Pull, Legs


## User Story 1:
Signed in user copies and pastes their workout text into the text box and clicks
'verify'. The website returns the parsed version of the workout and asks user
to confirm the accuracy. The user confirms that it has been parsed accurately
and clicks 'upload' to upload and store their workout.



