#!/usr/bin/env python

import glob
import os
import sys

try:
    sys.path.append(glob.glob('**/*%d.%d-%s.egg' % (
        sys.version_info.major,
        sys.version_info.minor,
        'win-amd64' if os.name == 'nt' else 'linux-x86_64'))[0])
except IndexError:
    pass

import carla

import random
import time

client = carla.Client('localhost', 2000)
client.set_timeout(2.0)

world = client.get_world()
map = world.get_map()

blueprint_library = world.get_blueprint_library()
bp = random.choice(blueprint_library.filter('vehicle.tesla.*'))
# color = random.choice(bp.get_attribute('color').recommended_values)
# print(color)
bp.set_attribute('color', '139,0,0')

sloc = carla.Location(x=40.0076, y=138.993, z=-0.0129659)
floc = carla.Location(x=220, y=62.9, z=1.0)

start = map.get_waypoint(sloc)
print(start)
finish = map.get_waypoint(floc)

topology = map.get_topology()

# for duo in topology:
# 	print(duo)
# 	if start == duo[0] or start == duo[1]:
# 		print(str(duo))
# 		print('hi')

vehicle = world.spawn_actor(bp, start.transform)

try:
	waypoint = start

	while waypoint!=finish:
		# Find next waypoint 2 meters ahead.
		print(waypoint.next(0.2))
		waypoint = random.choice(waypoint.next(1.0))
		# Teleport the vehicle.
		vehicle.set_transform(waypoint.transform)
		time.sleep(0.2)
except KeyboardInterrupt:
	vehicle.destroy()

