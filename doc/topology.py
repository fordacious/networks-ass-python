for unit in workload:
    self.num_vc_requests += 1
    path = self.get_path(unit)
    current_time = unit["time_activated"]
    self.topology.clear_obsolete_connections(current_time)

    if self.topology.valid_connection_path(path):
        self.topology.add_connection_path(path, current_time, unit["time_to_live"])
    else:
        self.num_blocked += 1
