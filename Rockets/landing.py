def landing(vessel, conn, mission_params, flight_stats):
    # Wait until vessel starts decending
    vertical_speed_check(conn, vessel)

    print("\nDecent Profile Started")
    print(f"Waiting for Parachute Target Altitude of {mission_params.parachute_altitude} Meters")
    vessel.auto_pilot.disengage()

    # Wait for target parachute altitude
    surface_altitude_check(conn, vessel, mission_params)
    print("Parachute Target Altitude Reached")
    print("Parachutes Deployed\n")

    # Deploy parachute
    vessel.control.activate_next_stage() 

    # Wait until vessel has landed
    while vessel.flight(vessel.orbit.body.reference_frame).vertical_speed < -0.1:
        if vessel.flight(vessel.orbit.body.reference_frame).surface_altitude < 5 and flight_stats.touchdown_speed == 0:
            flight_stats.touchdown_speed = vessel.flight(vessel.orbit.body.reference_frame).speed    
        pass
            
    print(f"{vessel.name} has Landed\n")
    return vessel

def vertical_speed_check(conn, vessel):
    vertical_Speed = conn.get_call(getattr, 
        vessel.flight(vessel.orbit.body.reference_frame), 'vertical_speed')
    # Create an expression on the server
    expr = conn.krpc.Expression.less_than(
        conn.krpc.Expression.call(vertical_Speed),
        conn.krpc.Expression.constant_double(-0.1))
    # Create an event from the expression
    event = conn.krpc.add_event(expr)
    # Wait on the event
    with event.condition:        
        event.wait()

def surface_altitude_check(conn, vessel, mission_params):
    srf_altitude = conn.get_call(getattr, 
        vessel.flight(vessel.orbit.body.reference_frame), 'surface_altitude') 
    # Create an expression on the server
    expr = conn.krpc.Expression.less_than(
        conn.krpc.Expression.call(srf_altitude),
        conn.krpc.Expression.constant_double(mission_params.parachute_altitude))
    # Create an event from the expression
    event = conn.krpc.add_event(expr)
    # Wait on the event
    with event.condition:
        event.wait()
