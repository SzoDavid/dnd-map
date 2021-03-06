# D&D Interactive Map Viewer (and Hub)

A django app for creating and hosting multiple interactive maps for your D&D campaign or anything else.
Just fill up the database, and it will be ready!

## What can this project do?

- Create and host multiple worlds
- Create locations with hierarchy, and display them in a table form
- Display maps with clickable regions, which will redirect to the location's page
- Display location on multiple maps
- Store data of your locations:
    - Name
    - Pronunciation
    - Type: classification of the item. Examples: *kingdom, capital, city, town, forest, etc.*
    - Notes for the dungeon master/owner only
    - Description, which can be hidden from the players
    - Parent: for example the kingdom the city is in
    - Map
    - Appearance: define area's on other location's maps, where clicked, it will redirect to the location's page
- Hide location from players if it's not discovered yet
- Admin interface for adding, editing, removing locations and appearances, and toggle buttons for quickly 
showing/hiding locations or descriptions


## TO-DO's

- [X] Display information of places
- [X] Admin interface
- [X] About page
- [X] Include explanations under new and edit forms
- [X] Add area creator for the maps
- [X] Search for locations
- [X] Create favicon
- List view improvements
    - [X] List view open/close
    - [X] Make discovered and description toggles async
    - [ ] List view group by type
- [X] Add multiple world hosting, and world creator
- [X] User page
- [ ] Import/Export with json - automatically export before removing worlds
- [ ] 404 page
- [ ] Features on the index page of dnd_imh - Admins can send nessages to users and if they agree their world will be featured on the front page
- [ ] Move form verification to clean() function
- [ ] Discord bot
- [ ] Application
- [ ] Add css
- [ ] Deploy project
- [ ] Add documentations
