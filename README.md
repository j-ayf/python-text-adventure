#Python Text Adventure

I made this over the course of a couple of months to make more myself familiar with Python. Don't expect too much,
however, I am very happy with the outcome.

##Start the game

Run `textAdventure.py` to play the game.

Run game.py in src/ directly (as `py -m src.game`) for debugging mode.

##Possible Commands:
- show inventory
- look around
- look at `object`
- look `north / south / west / east`
- look in `object` / open `object`
- go `north / south / west / east`
- unlock `object`
- take `object` (when the `object` lies directly in the location)
- take `object` from `container` (when the `object` is in a chest or something)
- talk to `NPC`
- buy `object`
- exit / stop

##Things to keep in mind
- This game is very primitive and does not include all the commands you might know from other established text adventures
- Some commands are very strict, so if you want to take an item out of a chest you _have to_ include the `from` keyword (see above)
- All objects of interest are shown by the 'quotation marks', so if you are ever stuck, make sure to `look at` all of them