import sys
from pathlib import Path

from src.json_loader import JSONLoader
from src.simulation import Simulation
from src.spawner import Spawner
from src.viewer import Viewer


def main():
    try:
        parameter_path = Path(sys.argv[1])
    except KeyError:
        print("No argument provided, Please provide path to parameters file")
        sys.exit(1)
    except TypeError:
        print("Invalid argument provided, Please provide path to parameters file")
        sys.exit(1)
    if not parameter_path.exists():
        print(f"Invalid file path provided: {parameter_path}, Please provide path to parameters file")
        sys.exit(1)

    # Load JSONLoadable objects
    loader = JSONLoader(parameter_path)
    simulation_settings = loader.load_simulation_settings()
    viewer_settings = loader.load_viewer_settings()
    missile_generators = loader.load_missiles()
    defences = loader.load_defences()

    spawner = Spawner(simulation_settings)
    viewer = Viewer(viewer_settings)

    # The missile generators require a spawner to function
    for missile_generator in missile_generators:
        missile_generator.set_spawner(spawner)

    simulation = Simulation(simulation_settings, defences, missile_generators, viewer)
    simulation.run(time=simulation_settings.simulation_time)

    viewer.export_gif(file_name='simulation_view.gif',
                      frame_rate=simulation_settings.frame_rate)

    return 0


if __name__ == "__main__":
    main()
