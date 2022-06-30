# D&D Interactive Map Viewer

A django app for creating interactive maps for your D&D campaign or anything else.
Just fill up the database, and it will be ready!

## What can this project do?

- Create locations with hierarchy, and display them in a table form
- Display maps with clickable regions, which will redirect to the location's page
- Display location on multiple maps
- Store data of your locations:
    - Name
    - Pronunciation
    - Type: classification of the item. Examples: *kingdom, capital, city, town, forest, etc.*
    - Notes for the dungeon master only
    - Description, which can be hidden from the players
    - Parent: for example the kingdom the city is in
    - Map
    - Appearance: define area's on other location's maps, where clicked, it will redirect to the location's page
- Hide location from players if it's not discovered yet
- Admin interface for adding, editing, removing locations and appearances, and toggle buttons for quickly 
showing/hiding locations or descriptions


## TODO's

- [X] Display information of places
- [X] Admin interface
- [X] About page
- [X] Include explanations under new and edit forms
- [X] Remove *kingdom/city/place* structure
- [ ] Move form verification to clean() function
- [ ] Add multiple world hosting, and world creator
- [ ] Add area creator for the maps
- [ ] Discord bot
- [ ] Application
- [ ] Add css
- [ ] Deploy project
- [ ] Add documentations
