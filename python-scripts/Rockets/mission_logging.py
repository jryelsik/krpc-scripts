import os.path

def mission_log_write(vessel, mission_params):
    file_loc = f"C:/Users/yelsi/Desktop/Programming/krpcFiles/KerbX/Mission Logs/{mission_params.mission_type} Logs/{vessel.name}_Log.txt"

    if not os.path.exists(file_loc):    
        log_file = open(file_loc, "w")        
    else:
        log_file = open(file_loc, "a")
    return log_file

def vessel_attributes_log(vessel, mission_params, vessel_stats, crew_stats, vessel_params):
    log_file = mission_log_write(vessel, mission_params)
    log_file.write(f"----- Vessel Attributes -----"
                    f"\nVessel Name: {vessel_stats.vessel_name}"
                    f"\nVessel Type: {str(vessel_stats.vessel_type.partition('.')[2].capitalize())}"
                    f"\nVessel Mass: {str(f'{vessel_stats.vessel_mass/1000:.03f}')} t"
                    f"\nVessel Liftoff Thrust: {str(f'{vessel_stats.vessel_liftoff_thrust:.02f}')} kN"
                    f"\nVessel Liftoff ISP ASL: {str(f'{vessel_stats.vessel_liftoff_isp:.02f}')} seconds")

    log_file.write("\n\n--- Crew ---")
    if vessel_params.crewed_flag:
        log_file.write(f"\nVessel Crew Capacity: {str(crew_stats.crew_capacity)}"
                        f"\nVessel Crew Count: {str(crew_stats.crew_count)}")
        # TODO: Test crew names and type
        for i in range(crew_stats.crew_count):
            log_file.write(f"\nVessel Crew Member Name: {str(crew_stats.crew.name[i])}"
                            f"\nVessel Crew Type: {str(crew_stats.crew.type[i])}")
    else:
        log_file.write("\nVessel is Uncrewed")
    log_file.close()

def mission_parameters_log(vessel, mission_params, vessel_params):
    log_file = mission_log_write(vessel, mission_params)

    log_file.write(f"\n\n----- Mission Parameters -----"
                    f"\nMission Type = {str(mission_params.mission_type)}")

    if vessel_params.first_decouple_stage != 0:
        log_file.write(f"\nFirst Decouple Stage = {str(vessel_params.first_decouple_stage)}")
    if vessel_params.second_decouple_stage != 0:
        log_file.write(f"\nSecond Decouple Stage = {str(vessel_params.second_decouple_stage)}")
    if vessel_params.third_decouple_stage != 0:
        log_file.write(f"\nThird Decouple Stage = {str(vessel_params.third_decouple_stage)}")
    if mission_params.gravity_turn_flag == True:
        log_file.write(f"\nTarget Apoapsis = {str(mission_params.target_apoapsis)}"
                        f"\nTarget Roll = {str(mission_params.target_roll)}"
                        f"\nTurn Angle = {str(mission_params.turn_angle)}"
                        f"\nGravity Turn Start Altitude = {str(mission_params.turn_start_altitude)}"
                        f"\nGravity Turn End Altitude = {str(mission_params.turn_end_altitude)}")
    else:
        log_file.write(f"\nGravity Turn = {str(mission_params.gravity_turn_flag)}")

    log_file.write(f"\nTarget Pitch = {str(mission_params.target_pitch)}"
                    f"\nTarget Heading = {str(mission_params.target_heading)}")

    if mission_params.parachute_altitude != None:
        log_file.write(f"\nParachute Release Altitude = {str(mission_params.parachute_altitude)}")
    log_file.close()

def contract_log(conn, vessel, mission_params):
    log_file = mission_log_write(vessel, mission_params)
    active_contracts = conn.space_center.contract_manager.active_contracts

    log_file.write("\n\n----- Contracts -----")
    if len(active_contracts) == 0:
        log_file.write("\nNo Active Contracts")
    for x in range(len(active_contracts)):
        if not active_contracts[x].state.completed:
            log_file.write(f"\nContract Type: {str(active_contracts[x].type.partition('Contracts.')[2])}"
                            f"\nContract Title: {str(active_contracts[x].title)}"
                            f"\nContract Description: {str(active_contracts[x].description)}"
                            f"\nContract Synopsis: {str(active_contracts[x].synopsis)}"
                            f"\nFunds on Completion: {str(active_contracts[x].parameters[0].funds_completion)}"
                            f"\nReputation on Completion: {str(active_contracts[x].parameters[0].reputation_completion)}"
                            f"\nScience on Completion: {str(active_contracts[x].parameters[0].science_completion)}"
                            f"\nContract Completion: {str(active_contracts[x].parameters[0].completed)}'\n'")
    log_file.close()
    
def experiments_log(vessel, mission_params):
    log_file = mission_log_write(vessel, mission_params)    
    total_science = 0
    parts_with_exp_title = []
    experiment_list = []

    log_file.write("\n\n----- Experiments Deployed on Vessel -----")
    for i in range(len(vessel.parts.experiments)):
        experiment_title = vessel.parts.experiments[i].part.title
        parts_with_exp_title = vessel.parts.with_title(experiment_title)
        for j in range(len(parts_with_exp_title)):
            if experiment_list != parts_with_exp_title and len(experiment_list) <= i:
                experiment_list += parts_with_exp_title

    for e in range(len(experiment_list)):
        if experiment_list[e].experiment.has_data:
            log_file.write(f"\n {str(experiment_list[e].title)}"
                f"\n    "
                f"{str(vessel.parts.experiments[e].title)}"
                f"\n    Science: "
                f"{str(round(experiment_list[e].experiment.data[0].science_value, 2))}")
            total_science += round(experiment_list[e].experiment.data[0].science_value, 2)

    if total_science != 0:
        log_file.write(f"\n\nTotal Science Collected: {str(total_science)}")
    else:
        log_file.write("\nNo Experiments Deployed on Vessel")
    log_file.close()

def flight_stats_log(vessel, mission_params, flight_stats):
    log_file = mission_log_write(vessel, mission_params)
    log_file.write(f"\n\n----- Flight Stats -----"
                    f"\nApoapsis = {str(f'{max(flight_stats.max_ap, default = 0):.02f} meters')}"
                    f"\nMax Altitude = {str(f'{max(flight_stats.max_alt, default = 0):.02f} meters')}"
                    f"\nMax Velocity = {str(f'{max(flight_stats.max_vel, default = 0):.02f} m/s')}"
                    f"\nMax G-force = {str(f'{max(flight_stats.max_g, default = 0):.02f} ')}" f"g's"
                    f"\nTouchdown Velocity = {str(f'{flight_stats.touchdown_speed:.02f} ' 'm/s')}")
    log_file.close()
                  
def mission_time_log(vessel, mission_params, flight_stats):
    log_file = mission_log_write(vessel, mission_params)
    log_file.write(f"\n\n----- Mission Time -----"
                    f"\nMission Start = {str(ut_format(flight_stats.start_time))}"
                    f"\nMission End = {str(ut_format(flight_stats.end_time))}"
                    f"\nTotal Mission Time = {str(met_format(flight_stats.total_mission_time, mission_params))}")
    log_file.close()

def notes(vessel, mission_params):
    log_file = mission_log_write(vessel, mission_params)
    log_file.write("\n\nNotes: ")
    log_file.close()

def generate_log_file(conn, vessel, mission_params, vessel_params, vessel_stats, flight_stats, crew_stats):
    print("\nGenerating Log File...")
    vessel_attributes_log(vessel, mission_params, vessel_stats, crew_stats, vessel_params)
    mission_parameters_log(vessel, mission_params, vessel_params)
    contract_log(conn, vessel, mission_params)
    experiments_log(vessel, mission_params)
    mission_time_log(vessel, mission_params, flight_stats)
    flight_stats_log(vessel, mission_params, flight_stats)
    notes(vessel, mission_params)
    print("Log File Generated")

def ut_format(x):
    seconds = x%60
    minutes = (x//60)%60
    hours = (x//3600)%6
    days = (x//21600)%426.08
    years = (x//9203328)

    return (f'Y{years+1:.0f}:D{days+1:.0f}:{hours:.0f}h:{minutes:.0f}m:{seconds:.0f}s UT')

def met_format(x, mission_params):
    x += mission_params.clamp_release_time
    seconds = x%60
    minutes = (x//60)%60
    hours = (x//3600)%6
    days = (x//21600)%426.08
    years = (x//9203328)

    return (f'T + {years:.0f}y:{days:.0f}d:{hours:.0f}h:{minutes:.0f}m:{seconds:.01f}s MET')