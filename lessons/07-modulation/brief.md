# 07 · Stacking modulations

**Day 4 · ~2 h**

## The move

Everything so far comes out of two numbers per point: how far from the centre, how high.
Every feature — star cross-section, twist, bumps, flat base — is a small function nudging
one of those. They don't know about each other. You stack them.

`reference/bauble.py` is four of these on a sphere. Open it after this lesson and it
should read as ordinary.

## Do

Get each modulation on its own first, then combine.

Then add a fifth of your own into the loop. Anything that changes `r`, `angle` or `z` as
a function of position counts.

Move one modulation above another in the code and re-run. Twist-then-star is not
star-then-twist.

## Leave on

**Order matters, and nothing tells you what the right order is.** You find out by moving
lines.
