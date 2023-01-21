import collections
from launch_utilities import initialize, universal_time, mission_time
from callbacks import start_callbacks
from mission_logging import generate_log_file
from launch import launch
from landing import landing
from mission_init import MissionParameters, VesselParameters, VesselStats, FlightStats
collections.Iterable = collections.abc.Iterable

def main():
    conn, vessel = initialize()
    vessel_stats = VesselStats(vessel_mass = VesselStats.total_vessel_mass(vessel),
                                vessel_name = vessel.name,
                                vessel_type = str(vessel.type))
    flight_stats = FlightStats()
    mission_params = MissionParameters
    vessel_params = VesselParameters

    # Start callbacks
    start_callbacks(vessel, conn, flight_stats)

    # Mission Start
    vessel = launch(conn, vessel, mission_params, vessel_params, vessel_stats, flight_stats)

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
    generate_log_file(conn, vessel, mission_params, vessel_params, vessel_stats, flight_stats)

if __name__ == "__main__":
    main()
    print("DONE")
    quit()
