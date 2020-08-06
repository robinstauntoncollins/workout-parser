# MVP

User will keep track of their workout in a text file (Google Keep for example) and when completed the user
will upload that text file to the web app which will automatically parse and store the workout accurately.

The app will then be able to keep track of the day, exercises, sets, reps etc of the user over time.


# Future

* Calendar to show the user when they completed a workout
* Some way to integrate with Google Keep/Docs to automatically retrieve uploaded workouts
* 


# Database Schema Design
User:
    id: INT
    username: TEXT
    email: TEXT
    password: TEXT
    workouts: INT; FK reference to workouts that have this user's Id

Workout:
    id: INT
    sections: INT; Linked (one-to-many) to Section - each workout contains several sections
    date: DATE (UTC)
    user_id: INT; Id of the user who logged this workout

    
Section: (each section contains one or more exercise log entries)
    id: int
    name: text; eg. Warmup
    exercise_logs: int; Link (one-to-many) to Exercise log entries
    rest: int; eg. 90
    workout_id: int; Id of the workout this section belongs to

    Eg. Warmup: arch hangs, squat reaches etc, rest 90s
    Eg2. Pair 1: ring pullups, beginner shrimp squat, rest 90s
    Eg3. Core: Ab wheel rollout, rest 90s

Set: (for a single performance of a single exercise in a workout)
    id: INT
    exercise_id: INT - linked to a particular exercise
    set_number: INT - number of sets performed
    reps: INT - number of reps performed in each set
    weight: INT - amount of weight used for each rep

Exercise:
    id: INT
    name: TEXT
    description: TEXT
    FK variation_id: INT
    FK equipment_id: INT
    FK category_id: INT
    Eg. Pullups, Rollouts, Squat, Dips, 

Variation:
    id: INT
    name: TEXT
    description: TEXT
    difficulty: INT
    Eg. unmodified, assisted, beginner, negatives, weighted, L-sit, Shrimp

Equipment:
    id: INT
    name: TEXT
    Eg. Rings, Bar, Ab wheel

Category: (which part of body does this exercise use?)
    id: INT
    name: TEXT
    Eg. Push, Pull, Legs




