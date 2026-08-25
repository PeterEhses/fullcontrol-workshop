# 04 · One continuous path

**Day 2 · ~90 min**

## The move

Stop treating layers as steps. Let z climb continuously while the path goes round — one
unbroken bead from bed to top. No layer changes, no seams, no retractions.

Slicers call this vase mode and offer it as a checkbox. Here it is just what happens
when you never reset z, which is the more useful way to know it.

## Do

Work through the silhouettes. Then write your own `radius_at` — it takes a number
between 0 and 1 and returns a radius multiplier. That one function is the whole outline
of the object.

Segments per lap down to `5`: still one continuous path, now pentagonal.

## Leave on

Every lap is held up by the one below it.

**So what happens to the part that sticks out past it?**
