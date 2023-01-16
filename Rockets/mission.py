import collections
from launch_utilities import initialize, universal_time, mission_time
from callbacks import start_callbacks
from mission_logging import generate_log_file
from mission_init import MissionParameters as mp, VesselParameters as vp, FlightStats as fs
from launch import launch
from landing import landing
import setup_params
collections.Iterable = collections.abc.Iterable

def main():
    conn, vessel = initialize()
    flight_stats = fs(vessel_mass = vessel.mass)
    mission_params = setup_params.setup_MP()
    vessel_params = setup_params.setup_VP()

    # Start callbacks
    start_callbacks(vessel, conn, flight_stats)

    # Mission Start
    vessel = launch(conn, vessel, mission_params, vessel_params, flight_stats)

    ### Need to unlock tracking station ###
    # TODO: Create orbit profile

    if mission_params.landing_flag:
        # Mission Landing
        vessel = landing(vessel, conn, mission_params, flight_stats)

    # Wait for user input to end mission
    mission_end_input = str(input("Type 'e' and Press Enter to End Mission\n"))
    while mission_end_input != "e":
        pass

    # Record mission end times
    flight_stats.end_time = universal_time(conn)
    flight_stats.total_mission_time = mission_time(vessel)

    # Generate mission logs
    generate_log_file(conn, vessel, mission_params, vessel_params, flight_stats)

if __name__ == "__main__":
    main()
    print("DONE")
    quit()
