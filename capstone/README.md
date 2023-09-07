# CS50W Capstone Project: Django Fit
## Video Demonstration: https://youtu.be/kGtNh4nayXU
(Hamza-ali-1999)

## Django Fit : Distinctiveness and Complexity

Django Fit is a Fitness Website used for Daily caloric and consumption tracking. It also has a workout exploring feature in which users can create, discover and save workouts for personal use. The caloric tracker is unique compared to other projects because it uses the users personalized stats to calculate BMR and percentages which are displayed on a gauge/meter for each day (gauge caps at 100%). Previous days can be accessed, viewed, and edited aswell. The Workout models are also unique since they use an EmedVideoField to display and play video links on the workout pages. This project is the culmination of the CS50W course and utilizes all teachings and previous project knowledge. It uses Django models, forms, Bootstrap CSS, combination of HTML with python from views, and Javascript for dynamic buttons and actions. It is also distinctive since it requires the use and filtering of objects through dates which is much more complex than previous projects along with a new feature of embedded videos.

## Files
The project is built upon the starting files of the previous project: network. Therefore the project names resemble project 4 and network however the files are built for Django Fit. The base files of project 4 come with the login logout and register features which are kept for the website. The project uses 4 models which include: User, Entry, Stats, Workout.

### views.py
The views.py file includes 3 ModelForm classes which are used to Update Stats, Change the Date, and Create Workouts. Along with the regular rendering views, the file includes 5 API routes which will be discussed below.

- The index view renders the default index.html template for which the logged users stats, entries by date, and percentages are calculated and rendered. The meter on the index page reflects the daily consumption percentage achieved for the date accessed.

- The create_workout, update, change_date paths are all form renderring and processing views used simply as the names describe. The Change date view is used to change the date of the tracker to check entires and tracking for previous days.

- The explore view renders all the Workout objects along with the Embedded videos in a template (explore.html). The Workouts are order by latest and also include Pagination showing 5 videos per page.

- The saved_workouts view is almost identical to the explore view however it combines the workouts that the user created along with the workouts saved to be displayed.

The entries filtered in the views functions and API routes are filtered using Date with the format of ('%Y-%m-%d') which is aquired using .strftime, and the logged user.

### API routes used in Javascript

- The create_entry route uses the variables passed and creates a new entry while returning JsonResponse to be displayed dynamically upon creation.
- The update_meter request calculates the users BMR and daily consumption to calculate and return the correct gauge values to be dynamically changed upon any entry.
- The remove_entry route simply removes entries and recalculates the tracker values.
- The workout_save path adds the user to the workouts savers list so it can be displayed on the saved list. The Save will not be available to the creator and will automatically be added to the users saved workouts page.
- The workout delete path is only available for the creator of workouts and upon access removes the selected workout.

### Index.js
- The create_entry function collects the values from the created form and parses them to the create_entry views.py routes to create and receive the entry model to be appended to the tracker.
- The remove function uses the id of the entry to remove the model object and the tracker div
- Both of the functions above include the update_meter API route to dynamically change the meter reading
- The save function uses the workout_save API route to add the user to the workouts savers list and dynamically changes the button css
- Similarly the delete_workout function uses the delete_workout API route to delete the model and remove its html.

### Templates
layout.html : Default structure with Bootstrap Navbar and utilities up top
index.html : Daily Tracking Page 
update.html : Update User Stats Form template
create_workout.html : Creating workout form template
explore.html : Explorer page for All workouts
saved.html : Personal page for workouts created and saved by user

### Website Flow
Upon Opening the Website, the Default tracker page is shown with a prompt to update stats. Upon Registering or logging in, if the stats have not been updated, the user will be automatically directed to the update stats form. Once the Stats are updated the user is free to make entries, workout, and explore and personalize workouts.

### Additional Information
The project uses a Django app for embedding Youtube videos ---> django-embed-video
It is used similar to the Django model URLField()
To download the package, once in the project directory, run ---> pip install django-embed-video

### How to run Django Fit:
- Download and unzip the project
- cd to the project directory
- In the terminal run ---> pip install django-embed-video
- In the terminal run ---> python manage.py runserver and open the domain


