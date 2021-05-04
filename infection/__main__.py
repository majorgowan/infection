import os
import json
from argparse import ArgumentParser
from infection import Infection
from infection import viz_utils as vzu
import matplotlib.pyplot as plt
from celluloid import Camera


def gen_arg_parser():
    """
    Read command-line arguments

    Returns
    -------
    Namespace object
        parsed command-line arguments
    """
    description = "epidemic simulator and visualizer"
    epilog = ("EXAMPLE:\n\n"
              + "infection -i quadrants -o my_results --video")

    # get list of built-in examples
    this_directory = os.path.abspath(os.path.dirname(__file__))
    example_dir = os.path.join(this_directory, "examples")
    examples = [f.split(".")[0] for f in os.listdir(example_dir)
                if f.endswith(".json")]

    parser = ArgumentParser(description=description, epilog=epilog)

    parser.add_argument("--steps", type=int,
                        default=100,
                        help="number of steps/days to simulate")
    parser.add_argument("-i", type=str,
                        help=("json file with configuration, or one of "
                              + ", ".join(examples)))
    parser.add_argument("-o", type=str,
                        default="infection_output.json",
                        help="file to which to write simulation output")
    parser.add_argument("--random_seed", type=int,
                        default=333, help="seed for random number generation")
    parser.add_argument("--video", action="store_true",
                        help="if set, generate an mp4 animation of simulation")
    parser.add_argument("--graph", action="store_true",
                        help="if set, plot infected/immune vs. day")
    parser.add_argument("--verbose", action="store_true",
                        help="if set, print results to screen")

    return parser.parse_args()


def main():
    # get command-line arguments
    args = gen_arg_parser()

    steps = args.steps
    input_file = args.i
    output_file = args.o
    random_seed = args.random_seed
    video = args.video
    graph = args.graph
    verbose = args.verbose

    this_directory = os.path.abspath(os.path.dirname(__file__))
    example_dir = os.path.join(this_directory, "examples")
    examples = [f.split(".")[0] for f in os.listdir(example_dir)
                if f.endswith(".json")]

    configuration = {}
    if input_file is not None:
        if input_file in examples:
            input_file = os.path.join(example_dir, f"{input_file}.json")
        with open(input_file, "r") as jsf:
            configuration = json.load(jsf)

    fig = None
    camera = None

    if video:
        fig = plt.figure(figsize=(10, 10))
        camera = Camera(fig)

    runner = Infection(**configuration)

    days = []
    infecteds = []
    immunes = []
    temperatures = []

    for day, n_infected, n_immune in runner.run(steps=steps,
                                                random_seed=random_seed,
                                                restart=True):
        n_people = len(runner.people_)
        mean_temp = runner.temperature_.temperature.mean()

        days.append(day)
        infecteds.append(100 * n_infected / n_people)
        immunes.append(100 * n_immune / n_people)
        temperatures.append(mean_temp)

        if video:
            vzu.plot_frame(fig, runner.people_, runner.temperature_,
                           runner.walls_)
            camera.snap()

        if verbose:
            if not day % 50:
                print(f"day: {day:4d}\t"
                      + f"infected: {100 * n_infected / n_people:4.2f}\t"
                      + f"immune: {100 * n_immune / n_people:4.2f}\t"
                      + f"mean_temp: {mean_temp:5.3f}")

    if video:
        animation = camera.animate()
        animation.save(f"{output_file.split('.')[0]}.mp4")

    if graph:
        fig, axs = plt.subplots(2, 1, sharex="all", figsize=(12, 6))
        axs[0].plot(days, infecteds, label="% infected")
        axs[0].plot(days, immunes, label="% immune")
        axs[0].legend()
        axs[1].plot(days, temperatures)
        axs[1].set_ylabel("mean temperature")
        axs[1].set_xlabel("day")
        fig.savefig(f"{output_file}.png")

    # write json file
    with open(f"{output_file}.json", "w") as jsf:
        json.dump({"days": days,
                   "n_infected": infecteds,
                   "n_immune": immunes,
                   "mean_temperature": temperatures}, jsf,
                  indent=2)


if __name__ == "__main__":
    main()
