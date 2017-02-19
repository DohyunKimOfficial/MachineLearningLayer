from tsfresh.examples.robot_execution_failures import download_robot_execution_failures, \
    load_robot_execution_failures
download_robot_execution_failures()
timeseries, y = load_robot_execution_failures()
timeseries[timeseries.id == 3][['time', 'a', 'b']].plot(x='time', title='Success example (id 3)', figsize=(12, 6));
