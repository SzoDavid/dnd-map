# D&D Interactive Map Viewer

A simple django app for creating interactive maps for your D&D campaign or anything else. Just fill up the database and it will be done!

## What *"can"* this project do?

- Display maps with clickable regions, for your cities or else
- Display places even if there are no maps
- Store data of your kingdoms, cities, places:
  - Name
  - Pronunciation (optional)
  - Parent (Ex: the kingdom the city is in)
  - Type (Define if the city is a capital, a large city or just a town, also optional)
  - Description (optional)
  - Map (optional)
  - Coordinates (Define a rectangle using pixel coordinates where this place is located on the parent map, optional)
  - Is it discovered (Makes you able to disallow people to veiw places that were not yet discovered)
 - Set places' discovered state in an admin page

## TODO's

- [X] Display information of places 
- [ ] Admin interface
- [ ] Add css
- [ ] About page
- [ ] Deploy project
- [ ] Add world creation for users
