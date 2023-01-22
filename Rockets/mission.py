import collections
from launch_utilities import initialize, universal_time, mission_time, launch_clamp_weight, get_crew_names, get_crew_type
from callbacks import start_callbacks
from mission_logging import generate_log_file
from launch import launch
from landing import landing
from mission_init import MissionParameters, VesselParameters, VesselStats, FlightStats, Crew
collections.Iterable = collections.abc.Iterable

def main():
    conn, vessel = initialize()
    vessel_stats = VesselStats(vessel_mass = vessel.mass + launch_clamp_weight(vessel),
                                vessel_name = vessel.name,
                                vessel_type = str(vessel.type))
    flight_stats = FlightStats()
    mission_params = MissionParameters()
    vessel_params = VesselParameters()

    if vessel_params.crewed_flag:
        crew_stats = Crew(crew_name = get_crew_names(vessel),
                            crew_type = get_crew_type(vessel),
                            crew_capacity = vessel.crew_capacity,
                            crew_count = vessel.crew_count)
    else:
        crew_stats = None

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
    generate_log_file(conn, vessel, mission_params, vessel_params, vessel_stats, flight_stats, crew_stats)

if __name__ == "__main__":
    main()
    print("DONE")
    quit()
