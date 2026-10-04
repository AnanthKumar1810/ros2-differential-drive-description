from glob import glob
import os
from setuptools import find_packages, setup

package_name = 'robot_description'

setup(
    name=package_name,
    version='0.1.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages', ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml', 'LICENSE']),
        (os.path.join('share', package_name, 'urdf'), glob('urdf/*.xacro')),
        (os.path.join('share', package_name, 'launch'), glob('launch/*.launch.py')),
        (os.path.join('share', package_name, 'rviz'), glob('rviz/*.rviz')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='S. Ananth Kumar',
    maintainer_email='sananthkumar3@gmail.com',
    description='Xacro differential-drive robot visualization for ROS 2 Jazzy.',
    license='Apache-2.0',
)

