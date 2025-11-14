# Lesson 01: Spiral Explorations

## Welcome to Computational Design for 3D Printing!

Today we're exploring a fundamentally different approach to designing for 3D printing. Instead of modeling solid objects, we'll **design the toolpath directly** - defining the exact path the 3D printer nozzle follows.

---

## Why FullControl?

Traditional 3D printing workflow:
1. Design a 3D model (CAD software)
2. Slice it into layers (slicer software)
3. Print the G-code

**FullControl approach:**
1. ~~Design a 3D model~~
2. ~~Slice it~~
3. **Write code that generates the toolpath directly**

This gives you **complete control** over:
- Layer heights that vary
- Non-planar printing paths
- Organic, flowing forms
- Parametric variations

---

## Your First Shape: A Spiral

A spiral is defined by:
- **Starting point** (center)
- **Radius growth** (how much bigger each loop gets)
- **Z height growth** (how much it rises)

```python
# Pseudocode
for each_turn in spiral:
    radius = turn_number * radius_growth
    angle = turn_number * angle_step
    height = turn_number * layer_height
```

---

## Experiment!

Try changing these parameters in the notebook:
- **Number of turns** - More or fewer loops?
- **Radius growth** - Tight spiral or wide?
- **Height per turn** - Steep or gradual?
- **Starting position** - Off-center designs?

There are no wrong answers - just different designs!

---

## Design Challenge

Create a spiral that:
1. Starts small and grows outward
2. Has an interesting height profile (not constant)
3. Uses at least 20 turns

**Bonus:** Can you make a double spiral? Or a spiral that grows then shrinks?

---

## Key Concepts

**`fc.Point(x, y, z)`** - A position in 3D space  
**`fc.transform(steps, 'plot')`** - Visualize your design  
**`fc.transform(steps, 'gcode')`** - Generate printable G-code

The beauty: You control every single point the nozzle visits!
