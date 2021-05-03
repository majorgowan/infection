# import os
from argparse import ArgumentParser


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
              + "infection <etc.>")

    # get list of built-in examples
    # this_directory = os.path.abspath(os.path.dirname(__file__))
    # example_dir = os.path.join(this_directory, "examples")
    # examples = [f for f in os.listdir(example_dir)
    #             if f.endswith(".json")]

    parser = ArgumentParser(description=description, epilog=epilog)

    parser.add_argument("-o", type=str,
                        default="infection_output.json",
                        help="file to which to write simulation output")

    parser.add_argument("--random_seed", type=int,
                        default=333, help="seed for random number generation")

    return parser.parse_args()


def main():
    # get command-line arguments
    # args = gen_arg_parser()

    # output_file = args.o

    # initialize generation state
    # seed = args.random_seed
    pass


if __name__ == "__main__":
    main()
