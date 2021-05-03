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
infection <etc.>
```