## Infection
Package for dynamic simulation of transmission in epidemic of non-lethal pathogen
![sample animation](static/example_animation.gif)

### Basic usage
```python
from infection import Infection

runner = Infection().initialize_all(random_seed=333)

# lists to log state each day
days = []
infecteds = []
immunes = []

# iterate over days
for day, n_infected, n_immune in runner.run(steps=2000):
    days.append(day)
    infecteds.append(n_infected)
    immunes.append(n_immune)
```

### Usage with animation
```python
from infection import Infection
from infection import viz_utils as vzu
import matplotlib.animation as manimation

writer = manimation.writers["ffmpeg"](fps=12)

runner = Infection().initialize_all(random_seed=333)

# initialize plotting frame
fig, scatter, qcs = vzu.init_frame(runner)

# context for file to write animation
with writer.saving(fig, "my_animation.mp4", dpi=60):
    # iterate over days
    for day, n_infected, n_immune in runner.run(steps=100):
        # generate next frame
        fig, scatter, qcs = vzu.update_frame(fig, scatter, qcs, runner)
        # write frame
        writer.grab_frame()
        
# display animation in jupyter notebook
vzu.display_html("my_animation.mp4")
```

### Command Line Interface
```
usage: infection [-h] [--steps STEPS] [-i INPUT_FILE] [-o OUTPUT_FILE]
                 [--random_seed RANDOM_SEED] [--video] [--graph] [--verbose]

epidemic simulator and visualizer

optional arguments:
  -h, --help                    show this help message and exit
  --steps STEPS                 number of steps/days to simulate
  -i INPUT_FILE                 json file with configuration, or one of quadrants, large_population
  -o OUTPUT_FILE                file to which to write simulation output
  --random_seed RANDOM_SEED     seed for random number generation
  --video                       if set, generate an mp4 animation of simulation
  --graph                       if set, plot infected/immune vs. day
  --verbose                     if set, print results to screen

EXAMPLE: infection --steps 100 -i quadrants -o my_results --video
```