# CelebritiesAndPersonalities

The CAP (Celebrities and Personalities) App matches users with celebrities based on similarities between them. 

# Collaboration Considerations

In order to effectively collaborate on this project and learn new skills that we can use in the future, our group used our Github accounts to create our project and collaborate on it. We learned terminal commands in order to push and pull changes, and we learned how to use source control within VSCode. This allowed us to continuously collaborate. 

# app.py explained

In order to program the backend/functionality of our webpages for the cap app, we used an app.py file and the python programming language. We include specific code for each webpage, and this backend performs computation such as determining whether an initially inputted password and confirmation password match, running our custom celebrity matching algorithm, etc.

We also use app.py to execute our SQLite commands that manipulate and use the database to display the contents of each page. 

# helpers.py explained

Our helpers.py file contains the python code for two helper functions: apology and login_required. The apology function provides an apology method containing a message explaining the user error and an error code, with the backdrop being an image of a celebrity at a red carpet event. At some points in our app, we use the apology helper function, while for other instances it is not necessary since we use javascript code within some of our HTML files to print error messages. The login_required function ensures that users have logged into the app in order to be able to view certain pages, such as the account page.


# Matching Algorithm Part 1: Overview of Three Metrics 

We implemented our matching algorithm in app.py, primarily within def test(). Our group knew that we wanted personality traits to factor into our celebrity matches. Therefore, we decided on both Enneagram and MBTI factoring into the matches, especially since we found a website that stores both of these personality types for hundreds of celebrities. We also wanted to add more complexity to our ranking to ensure maximum similarities. Therefore, we thought about how we could use existing information to factor into our rankings, and we found three APIs that analyze first names and return the likely age, gender, and nationality of the name (agify, genderize, and nationalize). Therefore, for our third metric, we decided to implement these APIs to analyze both the user's name and the celebrities' names and determine similarities in the age/gender/nationality. 
 
# Matching Algorithm Part 2: Weighting Each of Three Metrics 

As our group designed a matching algorithm with our three major factors, MBTI type, enneagram type, and name analysis, we considered how to weight each factor into our consideration of which celebrities are "matches" for users. We decided that we wanted users to have input on how these three factors would weigh into their results. Therefore, we decided to implement in our test three questions, corresponding to MBTI, enneagram, and name analysis, where we ask users to rate on a scale of 1-10 how much they would like each factor to weigh in their match with a celebrity. Based on the value inputted, the algorithm takes into account how important each factor is to a user, and is able to determine the final matching index based on that output. 

# Matching Algorithm Part 3: Using Points to Quantify Similarities

Our algorithm determines the degrees of similarity between a user and celebrities in the database by computing a "points" total for each celebrity based on the user inputs. The higher the points total, the greater the level of match between the user and the celebrity. This also makes querying for the celebrities that are most similar to users possible, and we query for the 10 highest points totals (best matches) and then display the corresponding celebrities who are the greatest matches to the user. 

# Matching Algorithm Part 4: Assessing MBTI Similarities (first metric)

We decided that we would assess similarities by iterating through each of the four letters of MBTI, E/I, N/S, T/F, and J/P, and then seeing how many letters the users have in common. For example, an ENTJ user and an ENTP celebrity have three out of four letters in common, while an INTP user and an ISFP celebrity only have one letter in common. In these cases, we then multiply the user's rating (on a scale of 1-10) of how much they want MBTI type to weigh in their match by the fraction of MBTI type letters in common with the celebrity, and add that result to the points for each example. We do this for all celebrities For example, let's say a user says on the test that they are INTJ and that they want MBTI to weigh 8 (on a scale of 1-10). If a celebrity is an INTJ, that celebrity's point total is then increased by (4/4) * 8 = 8 for this user because they share all 4 letters of their type in common (they are the same type). However, for the same user, an ENFJ celebrity's point total would increase by (2/4) * 8 = 4 for the same user because the user only shares 2 out of the 4 letters of their type in common with the celebrity.

# Matching Algorithm Part 5: Assessing Enneagram Similarities (second metric)

In order to assess enneagram similarities, we reward points to celebrities who have the same enneagram type as the user, and otherwise we do not provide points. When users and celebrities share the same enneagram type, we increase the celebrity's point total by the amount that the user wanted the enneagram to factor into their match (on a scale of 1-10). For example, let's say a user says on the test that they are a type 3w4 and that they want enneagram to weigh 4 (on a scale of 1-10). If a celebrity is a type 3w2, that celebrity's point total is then increased by 4 points because they share the same primary enneagram type (type 3) as the user. However, a type 8 celebrity (or any other type besides the user's type, which in this case is type 3) would not receive any points. 

# Matching Algorithm Part 6: Assessing Name Similarities (third metric)

Finally, we use the agify, genderize, and nationalize APIs to compute the most likely age, gender, and nationality, respectively, for both the user and all celebrities that we assess. These APIs compute these three factors based on first names. To determine how much the user wants this name analysis to factor into their match, we request a rating on a scale of 1-10 (called name_rating). We then iterate through the celebrities and determine how much overlap exists between the age, gender, and nationality computed for the user and each celebrity. 

For each of the three sub-metrics within name analysis, we reward ⅓ of the user’s name rating points if there is a match (since each sub-metric is ⅓ of the name analysis we conduct). For each of the three matches, we reward (1/3 * name_rating) points to the celebrity. For example, if these APIs use a user's name to determine that they are likely 34, male, and Russian, a celebrity whom the APIs determine to be 45, male, and Russian would receive points = 2/3 * name_rating (because the celebrity matches on 2 out of 3 categories). We designed the algorithm this way so that each component of name analysis contributes equally to the algorithm, but the user has ultimate control over how name analysis contributes to the algorithm.  

# Matching Algorithm Part 7: Agify, Nationalize, and Genderize APIs

We used three APIs, agify, nationalize, and genderize, for our name analysis in our algorithm. The agify API takes a first name as an input and predicts and returns the most likely age of someone who has that name. The nationalize API takes a first name as an input and predicts and returns the most likely nationality of someone who has that name. The genderize API takes a first name as an input and predicts and returns the most likely gender of someone who has that name. Some of these APIs also return associated probabilities for their predictions or second-most likely options, but for our purposes we only used the most likely output and did not consider probabilities for the predictions in our algorithm. 

Because we used the free versions of these APIs, we were limited to 1,000 requests per day on this site. This meant that we could not exceed this number of requests, such as when we populated our celebs.db database and had to run each celebrity’s name through this site in order to retrieve and store the predicted age, nationality, and gender. 

# Matching Algorithm Part 8: Justification for Applying APIs to User’s Name 

At first, we had considered asking the user to input their nationality/age/gender, and then comparing that to the result of name analysis on celebrity names using the APIs. However, we decided to also pull nationality/gender/age from the user’s name because we felt that this would yield a more accurate match. We feel that this is more accurate because agify outputs a most likely age, and nationalize outputs most likely nationality, so we felt that this would better compensate for more attributes (like someone whose name is a different nationality than their home country) to provide a match. 

# MBTI and Enneagram Sources of Information

We sourced all information about a celebrity's MBTI personality type and Enneagram personality type from the site https://www.personality-database.com/. We pulled information from this site in order to populate our celebs.db database of celebrities and their personality types.

# Name Analysis Sources of Information 

We sourced the name analysis by running the user and every celebrity within our database through three APIs: https://agify.io, https://nationalize.io, and https://genderize.io. We pulled the first names of celebrities from our celebs.db database and ran the first names through each site in order to determine the most likely names/ages/nationalities, and then compared that with the user's results which are stored as variables.

# Login and Registration Decisions 

Our group wanted users to be able to view our site without logging in or creating an account first so that they can learn about the project and what the site offers, but we also did not want users to be able to take our test or view results without creating an account. Therefore, our website contains login and registration pages within the site, rather than when a user first enters the site (like how was implemented in the finance PSET). Some of our pages (like match test) require that the user first logs in (or registers if they have not done so) so that their results can be stored. 

# General Layout Decisions

Our group wanted a simple yet effective layout for our website. For many of our pages, we used bootstrap in order to create aesthetic pages. We also wanted it to be clear for users how to use our site. That's why we decided to add a navbar containing Home, Methodology, Match Test, Compatibility Test, Register, Login, and About Us pages. In order to make the website more appealing to user, we created out logo “CAP App”, found in the navigational bar, to have a color text gradient with our website’s color theme (blue and white). Additionally, within the navigational bar, there is a dropdown menu called “Account” that allows users to easily change their password and logout. This helps condense relevant information in a singular place for users to easily complete functions in their account.

# General CSS and HTML Decisions

We use a styles.css file in order to add stylistic additions to our HTML which is stored in a folder called “static”. We also include a templates folder with our HTML files in order to clearly organize our CSS and HTML. Within some HTML pages that required user input that did not need to validate the user input because of the multiple-choice style (like test.html), we decided to create the error message within the HTML page using javascript because the error message was more distinct in these cases by appearing on the same screen as the page, as opposed to redirecting to an error message page. 

# Testing Layout and Site

We used flask to test our site and preview various layouts. This enabled us to test the site continuously and preview changes. 

# Logo and Gradient

For our Cap App logo, which is displayed at the top left of our navbar, we implemented a gradient in order to give the logo an aesthetic and modern look. We wanted the name of our app to be prominently displayed.

# Home Page Decisions

Our group wanted a homepage that was aesthetic, simple, and provided an overview of our site. We used canvas to design our home page and imported that into our code by converting to HTML.
 
# Methodology Page Decisions

Our group wanted our users to be able to understand the matching algorithm that we use in order to match them with celebrities. So, we included this page where we explain each of our three key metrics for our matching algorithm. We also link the tests for the MBTI and Enneagram personality tests so that users can take the test and figure out which personality type they are. We included explanations of MBTI and enneagram as well. For name analysis, we linked the three packages that we use in order to conduct the name analysis. We also added boxes around each metric and used varying font sizes so that these metrics appeared separate and were more digestible for the user. 

# Match Test Page Decisions

Our match test page collects all of the necessary information from the user in order for our matching algorithm to work. That is why we ask for their MBTI type, enneagram type, name, and the respective weight that they would like each of these to factor into their ranking. This is important to us because, rather than us deciding ourselves that each metric would weight 1/3, for example, we wanted the user to have more customization and personalization during this process. 

# Registration Page Decisions

We wanted a registration page that was efficient for users to complete and provided us with all necessary information. That is why we ask users for an email address, their password, to confirm their password (to make sure they didn’t make a mistake when inputting their password), and for the answers to two security questions. The answers to the security questions are used if the user forgets their password, in order to provide more security to the site.

# Login Page Decisions

Our users wanted a simple yet effective login experience, so we asked users for their email address and password in order to log in. 

# About Us Page Decisions

Our group included an about us page in order to provide a general overview of the creators of the app. We wanted to keep it simple, so we decided to include pictures of each of our team members and a brief bio. 

# Account Page Decisions

Our group wanted our account page to be somewhere that the user could manage their account, so we decided to dedicate a part of the navbar to this so that it was clear to users where they could manage their account. 

# Change Password Functionality Decisions

We wanted to allow users to change their password if needed, so we added this functionality to our site. Users must be logged into their account in order to access this functionality. We require users to input their old password (in order to confirm that they are actually the user that is trying to edit their account) as well as a new password, and we ask users to confirm their new password. 

# Forgot Password Functionality Decisions

We wanted to allow users who forgot their password to recover it, so we added a forgot password feature to our site. In order to verify a user so that not anyone can change a password associated with an account, we require that a user inputs their email address and answers to both security questions that they answered during registration.

# Password Specifications Across Registration, Change Password, and Forgot Password

Across each of these pages where users create a new password, we require that the user’s inputted password contains at least 5 letters, 1 numeric digit, and 1 special character so that the password is less easily guessable and vulnerable. We also require that the password cannot contain the user’s inputted email, as we felt that this could make the password more easily guessable. 

# Results Page Decisions

Our team knew that we needed a page to display a user’s results. We decided that we would display the top 10 matches so that the results are more digestible to the user, as we felt that displaying every celebrity in the database would be excessive and too much information for the user to sift through. We also wanted to provide a percent match (what percent of a perfect score is the celebrity’s point total) to provide the user with a quantitative metric for the ranking.


# Creating the actual SQL Databases

First, we went into SQlite by typing "sqlite3 database.db"

We went ahead and created the tables in SQLite by executing the schema in "#SQL Decisions and Design"

From there, we ran the file "setup.py" to populate the actual database.



# SQL Decisions and Design

Our group wanted to challenge ourselves in regards to SQL so that we could learn to implement SQL in the future without being dependent on any CS50 imports.

SQL Architecture: We used SQLite and created custom connections for our SQL databases. We created databases in order to store information about users (their username and password) and celebrities (their names, mbti type, enneagram type, a custom id, and a points value corresponding to the degree to which a celebrity is a match for a certain user). 

We chose to implement 3 SQL tables in one large database named database.db. The tables have the schema below: 

CREATE TABLE users (
                id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, 
                email TEXT NOT NULL, 
                password TEXT NOT NULL, 
                maiden TEXT NOT NULL, 
                nickname TEXT NOT NULL
            );
CREATE TABLE points (
                id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                celeb_id INTEGER NOT NULL,
                user_id INTEGER NOT NULL,
                points NUMERIC,
                FOREIGN KEY(celeb_id) REFERENCES celebs(id),
                FOREIGN KEY(user_id) REFERENCES users(id)
            );
CREATE TABLE celebs (
                id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, 
                name TEXT NOT NULL, 
                MBTI TEXT NOT NULL, 
                enne TEXT NOT NULL,
                nationality TEXT,
                gender TEXT,
                age NUMBER
            );


The users table has the above fields to ensure that a user can adjust their password as long as they remember their answers to the security questions and have a unique email. 

The points table has the above fields in order to ensure that point values (or the amount a celebrity and user match) are specific to the user. For instance, user1’s point value associated with the celebrity “Harry Styles” would differ from user2 because they each took the match test from different accounts. The points table does this by referencing unique ids from the celebs table and users table. 

The celebs table has the above fields in order to keep track of the personality qualities of the celebrity, as well as the nationalty, gender, and age predictions for the celebrity that we obtained by running APIs on the celebrity’s first name. Such makes it easier to compare the user’s qualities against the celebrity’s qualities in our matching algorithm. 

We chose to store elements in the tables as tuples, instead of dictionaries. Although we currently do not have that many users on this website, we wanted to be able to scale the website for future use. Because our points table has a row for every celebrity in the database per user, it is particularly important to conserve memory, and a tuple takes up significantly less memory than a dictionary type. 

We also do not anticipate any changes to any individual attribute of a row in any table once that row has been stored, so the fact that tuples are immutable does not affect the functionality of our program. 

# Specific SQL Queries:


---------Finding user information entered given the inputted email

rows = db.execute("SELECT * FROM users WHERE email = ?", (email,)).fetchone()
 
We want to only grab the user information for one unique email, so a fetchone() call is sufficient. 
 
—--------
---------Update new password into database

db.execute("UPDATE users SET password = ? WHERE email = ?",(generate_password_hash(newpassword), email))
       
connection.commit()

We update the users table with the new password, then tell the cursor to commit these changes so it is actually reflected in the database. 

—-------------

---------Get all information for that user using their inputted email name

rows = db.execute("SELECT * FROM users WHERE email = ?", (email,)).fetchall()
     
By the time they are logging in, even though it is not possible for a user to create more than one account with a single email, we use fetchall() just to be safe. As long as rows does not contain any values, the account is not stored within our system. 
 
—-----------Inserting into users
 
db.execute("INSERT INTO users (email, password, maiden, nickname) VALUES(?, ?, ?, ?)", (email, generate_password_hash(password), securityques1, securityques2))
connection.commit()
 
We insert the values obtained from the user input into the users table as tuples, then tell the cursor to commit these changes in the database. 
—------------------

---------Retrieving celebrities with highest points count for given user and their input 

top10 = db.execute("SELECT DISTINCT user_id, name, MBTI, enne, points FROM points JOIN celebs ON points.celeb_id = celebs.id WHERE user_id = ? ORDER BY points DESC LIMIT 10", (session["user_id"],))

We find the top 10 celebrities with the highest match index points for the user. We execute a join statement because we want to access and display attributes for the celebrities AND the user AND their points (user_id and points are stored in the points table). 

Ordering by descending points and limiting to 10 will give us the top 10 celebrities matched. 

—----------------
---------Fetching information for user in users database given their id

rows = db.execute("SELECT * FROM users WHERE id = ?", (session["user_id"],)).fetchall()
 
---------Deleting previous results for user

if len(rows) != 0:
      db.execute("DELETE FROM points WHERE user_id = ?", (session["user_id"],))
      connection.commit()
 

We want the user to be able to take the test again and again from the same account, with the same user_id, because we realize that perhaps they inputted the wrong personality type or have since taken the personality tests again with changed results. 

In order to do this, we query for the user_id with a SELECT statement, and delete the previous results for the user from our points table so that they are able to see their new results. 

—-----------------------
for i in range(1, CELEB_COUNT + 1):
---------Setting points counter variable for each celeb to zero
       points = 0
      
       # Selecting appropriate information for each celebrity
       celeb_mbti = db.execute("SELECT MBTI FROM celebs WHERE id = ?", (i,)).fetchone()[0]
       celeb_enne = db.execute("SELECT enne FROM celebs WHERE id = ?", (i,)).fetchone()[0]
       celeb_nat = db.execute("SELECT nationality FROM celebs WHERE id = ?", (i,)).fetchone()[0]
       celeb_gen = db.execute("SELECT gender FROM celebs WHERE id = ?", (i,)).fetchone()[0]
       celeb_age = db.execute("SELECT age FROM celebs WHERE id = ?", (i,)).fetchone()[0]
 
 
	. . . 
 
       db.execute("INSERT INTO points (celeb_id, user_id, points) VALUES (?, ?, ?)", (i, session["user_id"], points))
      
connection.commit()

Here, we are able to make use of the autoincrement id of celebs and synchronize this value with the loop index. Because we have stored all the attributes we need to reference in the celebs table, we simply query with a SELECT statement and use the loop index as our condition (which matches the celeb’s id). 

Then, in the loop, we insert the point values for a specific celebrity in relation to a specific user in our points table. 

We tell the cursor to commit the changes outside of the loop so that just in case there is something wrong inside of the loop/while running the loop, we can fix the new entries all at once as a batch instead of committing changes prematurely. 


# Error Message

Our group also implemented error/apology methods in two ways. In some cases, error messages are included within the HTML files as javascript code, so that a user is prompted on the same page (as opposed to being re-routed to an apology page) when they have made an error (such as forgetting to complete a field during registration). In other cases, we implemented an apology page that the user is re-routed to when they have made an error, and this apology page explains the error that the user has made. The apology message has a backdrop of an image of a celebrity at a red carpet event (that we chose because it was fitting for the celebrity theme of the website). 

