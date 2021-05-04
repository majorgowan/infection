## Infection
* Package for dynamic simulation of transmission in epidemic of non-lethal infection

### Basic usage
```python
from infection import Infection

runner = Infection()

# lists to log state each day
days = []
infecteds = []
immunes = []

# iterate over days
for day, n_infected, n_immune in runner.run(steps=2000, random_seed=333,
                                            restart=True):
    days.append(day)
    infecteds.append(n_infected)
    immunes.append(n_immune)
```


### Usage with animation
```python
from infection import Infection
from infection import viz_utils as vzu
import matplotlib.pyplot as plt
from celluloid import Camera
from IPython.display import HTML

fig = plt.figure(figsize=(10, 10))
camera = Camera(fig)

runner = Infection()

# iterate over days
for day, n_infected, n_immune in runner.run(steps=100, random_seed=333,
                                            restart=True):
    # add next frame to camera
    vzu.plot_frame(fig, runner.people_, runner.temperature_, runner.walls_)
    camera.snap()

animation = camera.animate()
# save animation to file
animation.save("animation.mp4")

# display animation in jupyter notebook
HTML(animation.to_html5_video())
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