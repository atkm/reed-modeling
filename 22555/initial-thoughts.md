# MCM Problem A #
## Oven ##
- Width/Length = Const
- Height?
- Power and Position of Heat Source
- Thermostat
- Constant temperature T-Br?
- Pan Placement
  1. Initially start with two racks, evenly spaced
  2. What are other possible placements?
- Critical Time t-c, where T-br == T-out.

## Brownie ##
- Conductivity (K-br)
- Expand? baking powder or not.
- Cook at 325~350 F for 40 mins
- Sugar burns at 350F (cream or tomato soup burns easily)
- sugar C12H22O11 => dehydration => Leaves carbon behind (which is black)
- Burn = dehydration and oxidation? (e.g. freezer burn: water sublimates)
- http://cooking.stackexchange.com/questions/10460/what-causes-sticking-and-what-can-i-do-to-reduce-food-sticking-to-my-cast-iron-s
- http://www.edinformatics.com/math_science/science_of_cooking/why_food_sticks.htm
- Flashpoints
- Ingredients (24 servings) from http://baking.about.com/od/brownies/r/ultimate.htm :
    8- 1 ounce squares of unsweetened chocolate
    1 cup butter
    5 eggs
    3 cups sugar
    1 tablespoon vanilla
    1-1/2 cups flour
    1 teaspoon salt
    2-1/2 cups chopped pecans or walnuts, lightly toasted

## Pan ##
- Area = Const
- Generate shape by GA
  1. Does initial population matter?
- Material
  1. Conductivity (K-pan)
  2. "glass or darkly colored pans results in hard or burned edges, according to Diana's Desserts." (http://www.livestrong.com/article/511157-how-to-keep-brownies-from-getting-hard-around-the-edge-of-the-pan/)
  3. "Using a pan that is too small ends up with burned edges and a raw center."
  4. "Select a light-colored, shiny baking pan."

## Heat Equation ##
- du/dt = K (du^2/dx^2 + du^2/dy^2 + du^2/dz^2)
- K: Conductivity constant
- Initial condition?

## Other Thoughts ##
- If K-pan much higher than K-br, then we can ignore the time that heat conducts through K-pan
