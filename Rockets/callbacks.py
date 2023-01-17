def current_biome(vessel, conn):
    c_biome = conn.add_stream(getattr, vessel, 'biome')
    def check_biome(biome):
        print(f"Entering {biome} biome")
        return biome
    c_biome.start()
    c_biome.add_callback(check_biome)

def max_gforce(vessel, conn, flight_stats):
    gforce = conn.add_stream(getattr, vessel.flight(), 'g_force')
    def check_g(g):
        if max(flight_stats.max_g, default = 0) < g:
            flight_stats.max_g.append(g)
        return flight_stats.max_g
    gforce.start()
    gforce.add_callback(check_g)

def max_apoapsis(vessel, conn, flight_stats):
    apoapsis = conn.add_stream(getattr, vessel.orbit, 'apoapsis_altitude')
    def check_apoapsis(ap):
        if max(flight_stats.max_ap, default = 0) < ap:
            flight_stats.max_ap.append(ap)
        return flight_stats.max_ap
    apoapsis.start()
    apoapsis.add_callback(check_apoapsis)

def max_altitude(vessel, conn, flight_stats):
    altitude = conn.add_stream(getattr, vessel.flight(), 'mean_altitude')
    def check_altitude(alt):
        if max(flight_stats.max_alt, default = 0) < alt:
            flight_stats.max_alt.append(alt)
        return flight_stats.max_alt
    altitude.start()
    altitude.add_callback(check_altitude)
    
def max_velocity(vessel, conn, flight_stats):
    velocity = conn.add_stream(getattr, vessel.flight(vessel.orbit.body.reference_frame), 'speed')
    def check_velocity(vel):
        if max(flight_stats.max_vel, default = 0) < vel:
            flight_stats.max_vel.append(vel)
        return flight_stats.max_vel
    velocity.start()
    velocity.add_callback(check_velocity)

def start_callbacks(vessel, conn, flight_stats):
    current_biome(vessel, conn)
    max_gforce(vessel, conn, flight_stats)
    max_apoapsis(vessel, conn, flight_stats)
    max_altitude(vessel, conn, flight_stats)
    max_velocity(vessel, conn, flight_stats)