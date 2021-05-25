# supix
Simple supervisor for Linux! LOG your hardware usage in memory RAM to avoid desnecessary writes in flash/hd/sd. Focused on simple devices like Raspberry PI.

![image](/docs/grafana.png)


# What is it?
This simple python script, capture some infos about your hardware and save it in temporary file system (RAM) with SQLite.

With this variables wrote in SQLite database, you can visualize with any program, like Grafana!

# How many variables?
14!

 * CPU: Average in 1, 5 and 15min.
 * RAM: Total, Used, Free Shared, Cached and Available.
 * Network bandwidth: Bytes received and Sent from specific interface or all interfaces (change this in code).
 * SWAP: Total, Used and Free.

# Why?
The intention of this script is write this variables in RAM to avoid desnecessary writes in your flash/hd/sd disk, to increase memory life. With this feature, you can use small delays, like 1sec.

# Where can I use?
Basically in any Linux! I tested in Raspberry PI 4/3B+/ZeroW, Ubuntu Server/Desktop.

# What I need?
 * Python.
 * Python lib: **psutil**. (pip install psutil)
 * Grafana (Optional).
 * TMPFS mounted in your device with path **'/dev/shm'**. Some systems (like ubuntu and Raspberry PI) already have this by default.


# How to use?
Just execute the script! Script write all data (by default) in **'/dev/shm/cpu_stats.db'**

 * Note 1: By default, script get network bandwidth from **all interfaces**. If you need to capture some specific interface, like **'eth0'**, change the line that call **'get_network(None)'** to **'get_network('eth0')'**.

 * Note 2: CPU usage is the same from 'top' or 'htop' command, then, pay attention with number of cores and value returned. Eg: In CPU with 4 cores, script return 100% when CPU usage is 25%, because 400% is the max!


If you would like to visualize in Grafana, see below:

 * 1. Execute script.
 * 2. Download Grafana (https://grafana.com/grafana/download)
 * 3. Download SQLite Plugin for Grafana (https://grafana.com/grafana/plugins/frser-sqlite-datasource/)
 * 4. Add the database file path to SQLite Plugin (default is **'/dev/shm/cpu_stats.db'**)
 * 5. Import **server.json** file in your Grafana.
