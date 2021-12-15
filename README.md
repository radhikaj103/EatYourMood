# Eat Your Mood!

A web-based application that allows the user to select a mood from a drop-down menu on the home page and suggests a list of restaurants within a 10 km radius of the user’s location based on the mood that they select.

## Features of the Application

The project is designed to help foodies select a cuisine to try based on their mood. When the user selects a mood from the dropdown menu for moods, the application first asks the user to share their location, then suggests a certain type of cuisine to suit the mood, and then gives a list of 15 restaurants to match that cuisine within a 10 km radius of their location. At present, the application does not work if the user chooses not to share their location.

The main features of the application are:
1. The homepage gives a list containing the name, location, phone number, distance from the user's location, and the price tag of the restaurants. The name is a URL that takes the user to the restaurant's yelp page.
2. Once the user registers and logs in, they can add the restaurants from the list to their favorites or remove them from their favorites, which appear in the 'Favorites' page that can be accessed from the navigation bar.
3. The application also allows the user to set a budget for eating out and keep a track of their restaurant expenses. To use this feature, the user can select 'My Home' from the navigation bar. The default budget along with the total expense is set at 0 for every user. The user can update their monthly restaurant budget by clicking the Update Budget button. Initially, there are no transactions for the user. To add a new transaction, the user can enter the name of the restaurant, the date of the transaction, and the expense in the displayed fields at the bottom and submit their entries by clicking the submit button. The new transaction now shows up in the transaction table. The user can add additional transactions and the expense for each transaction is added to the total expense field at the top, which in turn is deducted from the budget to reflect the remaining budget for the month.
4. The transaction list on the 'My Home' page only shows 5 of the most recent transactions, while the entire list of all the transactions can be seen on the 'History' page from the navigation bar.

## Demo of the Web-Application
```
[Demo]: https://youtu.be/cm8CX8ZgwaI
```

## Future Upgrades
1. If the user does not share their location, the application allows the user to input their city name to retrieve their location.
2. The application will have the feature to reset the budget every month.

## Built With
The application was built using the following major frameworks:
1. Flask
2. HTML
3. JavaScript
4. Bootstrap

The code is based in part on the finance distribution code provided in the web-track’s assignment. I used Mozilla's navigation method to get the user’s location, here developer’s API to convert the location coordinates to its postal code, and yelp’s API to look up the list of restaurants by key-words.

