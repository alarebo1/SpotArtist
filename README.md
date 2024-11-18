# project1_alarebo1

links for mileston 1 and 2 are the same since this git is linked to heroku
heroku link
https://guarded-taiga-17886.herokuapp.com/

![image](https://user-images.githubusercontent.com/77553304/134118406-42cd2d1c-1542-4f08-9461-3caccdf4f6cd.png)

<h1> how to run locally </h1>
to run the this project locally you will need to install flask and create .env file in project folder which encludes the folowing paramters
    <br>export CLIENT_ID=  your spotify client id 
    <br>export CLIENT_SECRET= your spotify client screte'  
    <br>export CLIENT_TOKEN=  your genius client token<br>
you will need to get client id,client secrete from a spotify api and client token from genius api



<h2>How the program fetchs data</h2><br><br>
I am using client id and client secrete to  get access token  form the authorization url of spotify.

After getting  the access_token I used the browse API to get ten new release albums 

I fetched the album name,  artist name, and image URL from the browser API to create a list, which I sent to the HTML.

From the album API, I fetched the song name and a preview link of the song

For the genius api i am using an accesss token to access the search api and for the song api i created a header with few paramter and the access token.

To access the info from the genius app, I created a list of songs and artists, which I used in search API  

after accessing the search API, I formed a key  from api_path to  access the lyric from the song API

I took the embedded lyric HTML from song API and used the replace() method to keep a string of ids as inputs for my HTML code and to execute the javascript in Html.

<br><br><h3>Techinical issues</h3>
i have a list of song title which i use to access the genius api. i had a issues with pulling lyrics if the song title includes (feat. artis name)
i was able to resolve this isue by spliting the song title string before the '(' and keeping the first portion of the title in my list of title.<br>
for my song preview i was using a link that sent to preview webite but it was causing issues since some of the elements in the preview list were set to None.So i used a forloop to change None to an empty string in my preview.<br>
another thing i encounter was getting index outbound error for song api which i had set to get the first result for the lyrics. i noticed that the error was occering when my random was at 9 so i set it to cap at 8 eventhough i had fetched ten songs from spotify api. the issue is whatever the 9th song is it is not finding a result for it in song api. so, it trigger the index outbound error because i am trying to get data from the song json using a foor loop and the first result doesn't exist.
<br>if i had more time i would try figure out a way fix the error properly and also to push the embeded html code as is instead of using a the replace method and i would figure out a way to add search song functionality to the app.

<br><br><h2>Milestone 2</h2>
https://guarded-taiga-17886.herokuapp.com/
 i pulled this git and created a milestone2 branch named milestone2 branch.
 <h3>How to run locally</h3>
 to run the project locally you will need to install flask_login flask-SQLAlchemy, psycopg2-binary,
 flask, and postgresql libraries<br><br>
    $ pip install Flask<br>
    $ pip install psycopg2-binary<br>
    $ pip install Flask-SQLAlchemy==2.1<br>
    $ sudo apt install postgresql<br><br>
   
<h3>Techinical issues and improvements</h3>
i created this program using the spotify search api if i had more time i could remedy this by passing
the artist id saved in database to artist track api and get information from there. i already have 
the function set up in this project but am using it to check it the artist id is valid.
<br><br>
when i buit the database i was trying to save the artist information and user login using a 
relational database where user id would be my foriegn key and username would be my primary key. 
i had issues with pushing to databases to this databases. i tryied to change the relationship of the 
tables since i figured that was the isue but it did not fix the problem so i ended up pushing all of 
the user information into one table.<br><br>

one feature that i would add if i had time would be the abality to delete saved artist from the 
database. i would have a form input box connected to my welcome route in my app.py which handels 
deletion. the method then will search the users input and check if it exist in database it will
first new add row with the users info leaving the artist name and aid empty and delete the searched 
artist form the database.

![image](https://github.com/user-attachments/assets/a5e6a55b-3153-4b5f-86f2-de6eb7fb15d0)
![image](https://github.com/user-attachments/assets/22ca0fd0-96d6-4cbd-8570-f7b20c5a1484)
![image](https://github.com/user-attachments/assets/8b5c2151-bbdb-4c42-9e07-88e026481b54)

If the album has a preview available in the Spotify API and you hit play, the album info div will shift to vibrant colors while its playing the preview.
![image](https://github.com/user-attachments/assets/75ffdef2-9f3a-44ed-aa9e-40d67f22a789)
![image](https://github.com/user-attachments/assets/c5b33da5-6811-447b-bb95-c49ba18fe4b7)







