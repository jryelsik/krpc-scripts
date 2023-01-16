import os.path
from launch_utilities import ut_format, met_format

def mission_log_write(vessel, mission_params):
    file_loc = "C:/Users/yelsi/Desktop/krpcFiles/KerbX/Mission Logs/" + mission_params.mission_type + " Logs/" + vessel.name + "_Log.txt"

    if not os.path.exists(file_loc):    
        log_file = open(file_loc, "w")        
    else:
        log_file = open(file_loc, "a")
    return log_file

def vessel_attributes_log(vessel, mission_params, flight_stats):
    log_file = mission_log_write(vessel, mission_params)
    vessel_type = str(vessel.type)
    log_file.write("----- Vessel Attributes -----" 
                    + "\nVessel Name: " + vessel.name
                    + "\nVessel Type: " + vessel_type.partition(".")[2].capitalize()
                    + "\nVessel Mass: " + str(f'{flight_stats.vessel_mass/1000:.03f}') + " t"
                    + "\nMax Vessel Thrust: " + str(f'{flight_stats.max_thrust:.02f}') + " kN"
                    + "\nVessel ISP ASL: " + str(f'{flight_stats.isp:.02f}') + " seconds")

    if vessel.crew_capacity != 0:
        log_file.write("\nVessel Crew Capacity: " + str(vessel.crew_capacity)
                        + "\nVessel Crew Count: " + str(vessel.crew_count))
        # TODO: Test crew names and type
        for x in range(vessel.crew_count):
            log_file.write("\nVessel Crew Member Name: " + str(vessel.crew.name[x])
                            + "\nVessel Crew Type: " + str(vessel.crew.type[x]))
    log_file.close()

def mission_parameters_log(vessel, mission_params, vessel_params):
    log_file = mission_log_write(vessel, mission_params)

    log_file.write("\n\n----- Mission Parameters -----"
                    + "\nMission Type = " + str(mission_params.mission_type))

    if vessel_params.first_decouple_stage != 0:
        log_file.write("\nFirst Decouple Stage = " + str(vessel_params.first_decouple_stage))
    if vessel_params.second_decouple_stage != 0:
        log_file.write("\nSecond Decouple Stage = " + str(vessel_params.second_decouple_stage))
    if vessel_params.third_decouple_stage != 0:
        log_file.write("\nThird Decouple Stage = " + str(vessel_params.third_decouple_stage))
    if mission_params.gravity_turn_flag == True:
        log_file.write("\nTarget Apoapsis = " + str(mission_params.target_apoapsis)
                        + "\nTarget Roll = " + str(mission_params.target_roll)
                        + "\nTurn Angle = " + str(mission_params.turn_angle)
                        + "\nGravity Turn Start Altitude = " + str(mission_params.turn_start_altitude)
                        + "\nGravity Turn End Altitude = " + str(mission_params.turn_end_altitude))
    else:
        log_file.write("\nGravity Turn = " + str(mission_params.gravity_turn_flag))

    log_file.write("\nTarget Pitch = " + str(mission_params.target_pitch)
                    + "\nTarget Heading = " + str(mission_params.target_heading))

    if mission_params.parachute_altitude != None:
        log_file.write("\nParachute Release Altitude = " + str(mission_params.parachute_altitude))
    log_file.close()

def contract_log(conn, vessel, mission_params):
    log_file = mission_log_write(vessel, mission_params)
    active_contracts = conn.space_center.contract_manager.active_contracts

    log_file.write("\n\n----- Contracts -----")
    if len(active_contracts) == 0:
        log_file.write("\nNo Active Contracts")
    for x in range(len(active_contracts)):
        if not active_contracts[x].state.completed:
            log_file.write("\nContract Type: " + str(active_contracts[x].type.partition("Contracts.")[2])
                            + "\nContract Title: " + str(active_contracts[x].title)
                            + "\nContract Description: " + str(active_contracts[x].description)
                            + "\nContract Synopsis: " + str(active_contracts[x].synopsis)
                            + "\nFunds on Completion: " + str(active_contracts[x].parameters[0].funds_completion)
                            + "\nReputation on Completion: " + str(active_contracts[x].parameters[0].reputation_completion)
                            + "\nScience on Completion: " + str(active_contracts[x].parameters[0].science_completion)
                            + "\nContract Completion: " + str(active_contracts[x].parameters[0].completed) + "\n")
    log_file.close()

def experiments_log(vessel, mission_params):
    log_file = mission_log_write(vessel, mission_params)    
    total_science = 0

    log_file.write("\n\n----- Experiments Deployed on Vessel -----")
    for i in range(len(vessel.parts.experiments)):
        experiment = experiment_name(vessel, i)
        y = vessel.parts.with_title(experiment)
        t = len(y)
        if vessel.parts.with_title(experiment)[i-t].experiment.has_data:
            log_file.write("\n" + str(experiment)
                + "\n    "
                #+ str(vessel.parts.with_title(experiment)[i-t]
                #    .experiment.science_subject.title)
                + str(vessel.parts.experiments[i-t].title)
                + "\n    Science: "
                + str(round(vessel.parts.with_title(experiment)[i-t]
                    .experiment.data[0].science_value, 2)))
            total_science += round(vessel.parts.with_title(experiment)[i-t]
                .experiment.data[0].science_value, 2)
    if total_science != 0:
        log_file.write("\n\nTotal Science Collected: " + str(total_science))
    else:
        log_file.write("\nNo Experiments Deployed on Vessel")
    log_file.close()

def experiment_name(vessel, x):
    if vessel.parts.experiments[x].part.title == "2HOT Thermometer":
        experiment = vessel.parts.experiments[x].part.title
    elif vessel.parts.experiments[x].part.title == "3PresMat Barometer":
        experiment = vessel.parts.experiments[x].part.title
    return experiment

def flight_stats_log(vessel, mission_params, flight_stats):
    log_file = mission_log_write(vessel, mission_params)
    log_file.write("\n\n----- Flight Stats -----"
                    + "\nApoapsis = " + str(f'{max(flight_stats.max_ap):.02f} meters')
                    + "\nMax Altitude = " + str(f'{max(flight_stats.max_alt):.02f} meters')
                    + "\nMax Velocity = " + str(f'{max(flight_stats.max_vel):.02f} m/s')
                    + "\nMax G-force = " + str(f'{max(flight_stats.max_g):.02f} ' + "g's")
                    + "\nTouchdown Velocity = " + str(f'{flight_stats.touchdown_speed:.02f} ' + "m/s"))
    log_file.close()
                  
def mission_time_log(vessel, mission_params, flight_stats):
    log_file = mission_log_write(vessel, mission_params)
    log_file.write("\n\n----- Mission Time -----"
                    + "\nMission Start = " + str(ut_format(flight_stats.start_time))
                    + "\nMission End = " + str(ut_format(flight_stats.end_time))
                    + "\nTotal Mission Time = " + str(met_format(flight_stats.total_mission_time, mission_params)))
    log_file.close()

def notes(vessel, mission_params):
    log_file = mission_log_write(vessel, mission_params)
    log_file.write("\n\nNotes: ")
    log_file.close()

def generate_log_file(conn, vessel, mission_params, vessel_params, flight_stats):
    print("\nGenerating Log File...")
    vessel_attributes_log(vessel, mission_params, flight_stats)
    mission_parameters_log(vessel, mission_params, vessel_params)
    contract_log(conn, vessel, mission_params)
    experiments_log(vessel, mission_params)
    mission_time_log(vessel, mission_params, flight_stats)
    flight_stats_log(vessel, mission_params, flight_stats)
    notes(vessel, mission_params)
    print("Log File Generated")