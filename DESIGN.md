# CelebritiesAndPersonalities

The Cap (Celebrities and personalities) App matches users with celebrities based on similarities between them. 

# Collaboration Considerations

In order to effectively collaborate on this project and learn new skills that we can use in the future, our group used our Github accounts to create our project and collaborate on it. We learned terminal commands in order to push and pull changes, and we learned how to use source control within VSCode. This allowed us to continuously collaborate. 

# Matching Algorithm Decisions and Explanation

We implemented our matching algorithm in app.py, primarily within def test().

Determining our inital three matching factors: Deciding on our three factors for our matching algorithm: Our group knew that we wanted personality traits to factor into our celebrity matches. Therefore, we decided on both enneagram and mbti factoring into the matches, especially since we found a website that stores both of these personality types for thousands of celebrities. We also wanted to add more complexity to our ranking to ensure maximum similarities. Therefore, we thought about how we could use existing information to factor into our rankings, and we found three APIs that analyze first names and return the likely age, gender, and nationality of the name. Therefore, for our third metric, we decided to implement these APIs to analyze both the user's name and the celebrities' names and determine similarities in the age/gender/nationality. 

Determining how much each of the three factors goes into the celebrity matches: As our group designed a matching algorithm with our three major factors, MBTI type, enneagram type, and name analysis, we considered how to weight each factor into our consideration of which celebrities are "matches" for users. We decided that we wanted users to have input in how these three factors would weight into their results. Therefore, we decided to implement in our test three questions, corresponding to MBTI, enneagram, and name analysis, where we ask users to rate on a scale of 1-10 how much they would like each factor to weigh in their match with a celebrity. 

Using points to track similarities: Our algorithm determines the degrees of similarity between a user and celebrities in the database by computing a "points" total for each celebrity based on the user inputs. The higher the points total, the greater the level of match between the user and the celebrity. This also makes querying for the celebrities that are most similar to users possible, because we can query for the 10, 20 or other number of highest points totals and then have can display the corresponding celebrities who are the greatest matches. 

Assessing MBTI similarities between users and celebrities: We decided that we would assess similarities by iterating through each of the four letters of MBTI, E/I, N/S, T/F, and J/P, and then seeing how many letters the users have in common. For example, an ENTJ user and an ENTP celebrity have three out of four letters in common, while an INTP user and an ISFP celebrity only have one letter in common. In these cases, we then multiply the user's rating (on a scale of 1-10) of how much they want MBTI type to weigh in their match by the fraction of MBTI type letters in common with the celebrity, and add that result to the points for each example. We do this for all celebrities For example, let's say a user says on the test that they are INTJ and that they want MBTI to weigh 8 (on a scale of 1-10). If a celebrity is an INTJ, that celebrity's point total is then increased by (4/4) * 8 = 8 for this user because they share all 4 letters of their type in common (they are the same type). However, for the same user, an ENFJ celebrity's point total would increase by (2/4) * 8 = 4 for the same user because the user only shares 2 out of the 4 letters of their type in common with the celebrity.

Assessing Enneagram similarities between users and celebrities: In order to assess enneagram similarities, we reward points to celebrities who have the same enneagram type as the user, and otherwise we do not provide points. When users and celebrities share the same enneagram type, we increase the celebrity's point total by the amount that the user wanted enneagram to factor into their match (on a scale of 1-10). For example, let's say a user says on the test that they are a type 3w4 and that they want enneagram to weigh 4 (on a scale of 1-10). If a celebrity is a type 3w4, that celebrity's point total is then increased by 4 points because they share the same enneagram type (type 3) as the user. However, a type 8 celebrity (or any other type besides the user's type, which in this case is type 3) would not receive any points.

Assessing name analysis similarities between users and celebrities: Finally, we use the agify, genderize, and nationalize APIs to compute the most likely age, gender, and nationality, respectively, for both the user and all celebrities that we assess. These APIs compute these three factors based on first names. To determine how much the user wants this name analysis to factor into their match, we request a rating on a scale of 1-10 (called name_rating). We then iterate through the celebrities and determine how much overlap exists between the the age, gender, and nationality computed for the user and each celebrity. For each of the three matches, we reward (1/3 * name_rating) points to the celebrity. For example, if these APIs use a user's name to determine that they are likely 34, male, and Russian, a celebrity whom the APIs determine to be 45, male, and Russian would receive points = 2/3 * name_rating (because the celebrity matches on 2 out of 3 categories). We designed the algorithm this way so that each component of name analysis contributes equally to the algorithm, but the user has ultimate control over how name analysis contributes to the algorithm. 


# MBTI and Enneagram Sources of Information

We sourced all information about a celebrity's mbti personality type and enneagram personality type from the site https://www.personality-database.com/. We pulled information from this site in order to populate our celebs.db database of celebrities and their personality types.

# Name Analysis Sources of Information 

We sourced the name analysis by running the user and every celebrity within our database through three APIs: https://agify.io, https://nationalize.io, and https://genderize.io. We pulled the first names of celebrities from our celebs.db database and ran the first names through each site in order to determine the most likely names/ages/nationalities, and then compared that with the user's results which are stored as variables.

# Login and Registration Decisions 

Our group wanted users to be able to view our site without logging in or creating an account first so that they can learn about the project and what the site offers, but we also did not want users to be able to take our test or view results without creating an account. Therefore, our website contains login and registration pages within the site, rather than when a user first enters the site (like how was implemented in the finance pset). Some of our pages (like match test) require that the user first logs in (or registers if they have not done so) so that their results can be stored. 

# Other Layout Decisions

Our group wanted a simple yet effective layout for our website. We also wanted it to be clear for users how to use our site. That's why we decided to add a navbar containing Home, Methodology, Match Test, Compatibility Test, Register, Login, and About Us pages.

# Testing Layout and Site

We used flask to test our site and preview various layouts. This enabled us to test the site continuously and preview changes. 

# SQL Decisions

Our group wanted to challenge ourselves in regard to SQL so that we could learn to implement SQL in the future without being dependent on any CS50 imports. So, we used SQLite and created custom connections for our SQL databases. We created databases in order to store information about users (their username and password) and celebrities (their names, mbti type, enneagram type, a custom id, and a points value corresponding to the degree to which a celebrity is a match for a certain user). 



