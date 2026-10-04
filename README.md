# ROS 2 Differential-Drive Robot Description

**Project 4 · ROS 2 Jazzy · URDF/Xacro · TF · RViz**

A reusable `robot_description` package for a basic differential-drive platform: a box chassis, two rotating wheels, a fixed spherical caster, and a LiDAR housing. One launch command expands Xacro, starts the joint-state GUI, publishes transforms, and opens RViz with a saved configuration.

## SIH-style problem statement

**Theme:** Building a robot-description foundation for indoor service and inspection robots.

Teams developing campus delivery, warehouse inspection, or assistance robots need a consistent model of the chassis, wheels, and sensor mounting frames before adding simulation or navigation. Repeated dimensions and disconnected coordinate frames make models difficult to maintain and sensor data difficult to interpret.

**Objective:** Create a modular ROS 2 description that represents the platform, publishes its component transforms, and allows visual inspection of wheel motion and sensor placement.

**Deliverables:** A parameterized Xacro model, installable ROS package, integrated launch file, saved RViz view, and reproducible build and TF inspection instructions. This is a learning-project problem statement inspired by the SIH format, not an official SIH problem ID or competition submission.

## Scope and status

This completes the description and visualization stage of Project 4. The geometry and joint origins follow the learning conversation. Colors, a derived wheel offset, and a saved RViz configuration improve usability.

The model is visual only: it contains no collision geometry, inertia, drive controller, odometry, or simulated laser scan. Moving GUI sliders rotates the wheel frames; it does not drive the chassis. The fixed caster is a simplified representation. Wheel and caster ground contact are not aligned in these original learning dimensions; revise the geometry before physics simulation.

## Architecture

```text
robot.urdf.xacro --Xacro--> URDF XML (robot_description)
                                  |
                    +-------------+-------------+
                    |                           |
         joint_state_publisher_gui     robot_state_publisher
                    |                           ^
                    +------ /joint_states ------+
                                                |
                                     /tf and /tf_static
                                                |
                                               RViz
```

The launch file processes Xacro using its Python API and supplies the generated XML to both publishers. RViz obtains the model from `/robot_description`; its fixed frame is `base_link`. Fixed joints appear on `/tf_static`, while wheel transforms on `/tf` reflect `/joint_states`.

### Link and joint tree

```text
base_link
├── left_wheel_joint  (continuous, Y axis) → left_wheel_link
├── right_wheel_joint (continuous, Y axis) → right_wheel_link
├── caster_joint      (fixed)             → caster_link
└── laser_joint       (fixed)             → laser_link
```

Coordinates use X forward, Y left, and Z up. Distances are metres and angles are radians.

| Component | Geometry | Origin relative to base_link |
|---|---|---|
| Base | 0.6 × 0.4 × 0.2 m box | Root frame at chassis center |
| Left wheel | Radius 0.1 m, width 0.05 m | (0, +0.225, 0) |
| Right wheel | Radius 0.1 m, width 0.05 m | (0, −0.225, 0) |
| Caster | Radius 0.06 m sphere | (−0.22, 0, −0.12) |
| LiDAR housing | Radius 0.07 m, height 0.05 m | (0.10, 0, 0.15) |

The cylinder visuals rotate by π/2 around X so their axes align with the wheel joints' Y axes. Xacro properties centralize dimensions, and the wheel macro generates both wheel links and joints. Changing chassis width also updates wheel spacing.

## Project structure

The repository root is the ROS package root; the repository name and ROS package name intentionally differ.

```text
ros2-differential-drive-description/
├── README.md
├── LICENSE
├── .gitignore
├── package.xml
├── setup.py
├── setup.cfg
├── resource/
│   └── robot_description
├── robot_description/
│   └── __init__.py
├── urdf/
│   └── robot.urdf.xacro
├── launch/
│   └── display_robot.launch.py
└── rviz/
    └── display.rviz
```

`setup.py` installs model, launch, and RViz assets into the package share directory. The resource marker registers the package in the ament index; `package.xml` declares ROS dependencies.

## Installation

Use Ubuntu 24.04 with ROS 2 Jazzy installed and a graphical desktop. See the [official Jazzy installation guide](https://docs.ros.org/en/jazzy/Installation/Ubuntu-Install-Debs.html).

```bash
source /opt/ros/jazzy/setup.bash
sudo apt update
sudo apt install git python3-colcon-common-extensions python3-rosdep \
  ros-jazzy-xacro ros-jazzy-robot-state-publisher \
  ros-jazzy-joint-state-publisher-gui ros-jazzy-rviz2 \
  ros-jazzy-tf2-ros ros-jazzy-tf2-tools liburdfdom-tools

mkdir -p ~/ros2_ws/src
cd ~/ros2_ws/src
git clone https://github.com/AnanthKumar1810/ros2-differential-drive-description.git
```

If rosdep has never been initialized on this machine, run `sudo rosdep init` once. Then:

```bash
rosdep update
cd ~/ros2_ws
rosdep install --from-paths src/ros2-differential-drive-description \
  --ignore-src --rosdistro jazzy -r -y
```

## Build and launch

```bash
cd ~/ros2_ws
source /opt/ros/jazzy/setup.bash
colcon build --symlink-install --packages-select robot_description
source install/setup.bash
ros2 launch robot_description display_robot.launch.py
```

RViz and Joint State Publisher GUI should open. The saved view enables RobotModel and TF with `base_link` as the fixed frame. Adjust each wheel slider to inspect its frame rotation. A cylinder is rotationally symmetric, so the TF axes make wheel rotation easier to see.

After editing installed assets, rebuild and relaunch. In every new terminal, source both `/opt/ros/jazzy/setup.bash` and `~/ros2_ws/install/setup.bash`.

## Inspect the model and TF

Expand the source model and check the resulting URDF:

```bash
cd ~/ros2_ws/src/ros2-differential-drive-description
xacro urdf/robot.urdf.xacro > /tmp/project4_robot.urdf
check_urdf /tmp/project4_robot.urdf
```

With the launch running, inspect ROS in another sourced terminal:

```bash
ros2 node list
ros2 topic list
ros2 topic echo /joint_states --once
ros2 topic echo /tf --once
ros2 topic echo /tf_static --qos-durability transient_local --once
ros2 run tf2_ros tf2_echo base_link laser_link
ros2 run tf2_ros tf2_echo base_link left_wheel_link
ros2 run tf2_tools view_frames
```

Expected nodes are `/robot_state_publisher`, `/joint_state_publisher_gui`, and `/rviz2`. The LiDAR translation should be approximately (0.10, 0, 0.15) m. The left wheel translation is (0, 0.225, 0) m and its orientation changes with the GUI. `view_frames` saves a TF graph in the current directory. Stop continuous inspection commands with Ctrl+C.

There are no `map` or `odom` frames at this stage.

## Concepts learned

- **URDF:** Describe a robot as a tree of rigid links and joints.
- **Joint types:** Continuous joints allow wheel rotation; fixed joints preserve rigid mounting transforms.
- **Origins and axes:** Separate component placement, visual orientation, and the joint's rotation axis.
- **Xacro:** Replace duplicated XML with shared properties, expressions, and reusable macros.
- **Joint states:** Supply positions for movable joints through `sensor_msgs/JointState`.
- **Robot state publisher and TF:** Convert the model and joint positions into spatial relationships.
- **RViz:** Inspect geometry and coordinate frames without a physics engine.
- **ROS packaging:** Install assets, declare dependencies, build with colcon, and locate package resources through ament.

## Troubleshooting

| Symptom | Action |
|---|---|
| Package or launch file not found | Rebuild from the workspace root and source the overlay. |
| Xacro import or executable missing | Install `ros-jazzy-xacro` and source Jazzy. |
| RViz shows no model | Check fixed frame `base_link`, RobotModel topic `/robot_description`, and Transient Local durability. |
| Wheel transforms missing | Check the joint-state GUI is running and `/joint_states` contains both wheel joints. |
| GUI cannot open | Use a graphical session; remote/headless hosts need display forwarding configured. |

## Next steps: Project 5 in Gazebo

1. Align chassis, wheel, and caster ground contact; choose a ground reference frame.
2. Add collision geometry, realistic masses, and valid inertial tensors.
3. Integrate with Gazebo Harmonic and ROS 2 Jazzy using `ros_gz`.
4. Add differential-drive control, publish odometry, and establish `odom → base_link`.
5. Replace GUI joint states with the simulator or a controller's joint-state output.
6. Add a simulated LiDAR producing `/scan`, then verify sensor TF and ROS/Gazebo bridging.
7. Validate motion and sensing before adding SLAM or Nav2.

## References

- [ROS 2 Jazzy: Xacro tutorial](https://docs.ros.org/en/jazzy/Tutorials/Intermediate/URDF/Using-Xacro-to-Clean-Up-a-URDF-File.html)
- [Robot state publisher](https://github.com/ros/robot_state_publisher)
- [Joint state publisher](https://github.com/ros/joint_state_publisher/tree/ros2)
- [Gazebo ROS installation guidance](https://gazebosim.org/docs/harmonic/ros_installation/)

## Validation

Source XML, Python syntax, expanded link/joint structure, packaging assets, and saved RViz configuration are checked during repository preparation. Full colcon build and graphical ROS execution require a Jazzy environment; they have not been run on the Windows preparation host.

## License

Apache License 2.0. See [LICENSE](LICENSE).

