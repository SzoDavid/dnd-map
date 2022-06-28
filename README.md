# D&D Interactive Map Viewer

A django app for creating interactive maps for your D&D campaign or anything else. 
Just fill up the database, and it will be ready!

## What can this project do?

 - Display maps with clickable regions, for your settlements
 - Display settlements in a table form
 - Display terrain features (forests, mountains, etc.) on multiple maps
 - Hide terrain feature description from users, if it's undiscovered
 - Store data of your settlements: kingdoms, cities, places:
   - Name
   - Pronunciation (optional)
   - Parent (Ex: the kingdom the city is in)
   - Type (Define if the city is a capital, a large city or just a town, also optional)
   - Description (optional)
   - Map (optional)
   - Coordinates (Define a rectangle using pixel coordinates where this place is located on the parent map, optional)
   - Is it discovered (Makes you able to disallow people to view places that were not yet discovered)
 - Admin interface for adding, editing, removing settlements, and toggle buttons for quickly changing discovered state


## TODO's

- [X] Display information of places 
- [X] Admin interface
- [X] Add terrain features (links for forests, mountains, etc.)
- [ ] Add help page and include explanations under new and edit forms
- [ ] Host multiple worlds
- [ ] Add css
- [X] About page
- [ ] Deploy project
- [ ] Add world creation for users
- [ ] Remove *kingdom/city/place* structure
