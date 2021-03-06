# -*- coding: utf-8 -*-
#
#
#  TheVirtualBrain-Scientific Package. This package holds all simulators, and 
# analysers necessary to run brain-simulations. You can use it stand alone or
# in conjunction with TheVirtualBrain-Framework Package. See content of the
# documentation-folder for more details. See also http://www.thevirtualbrain.org
#
# (c) 2012-2013, Baycrest Centre for Geriatric Care ("Baycrest")
#
# This program is free software; you can redistribute it and/or modify it under 
# the terms of the GNU General Public License version 2 as published by the Free
# Software Foundation. This program is distributed in the hope that it will be
# useful, but WITHOUT ANY WARRANTY; without even the implied warranty of 
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public
# License for more details. You should have received a copy of the GNU General 
# Public License along with this program; if not, you can download it here
# http://www.gnu.org/licenses/old-licenses/gpl-2.0
#
#

"""
Demonstrate using the simulator at the region level, deterministic interation.

``Run time``: approximately 2 seconds (workstation circa 2010)
``Memory requirement``: < 1GB

.. moduleauthor:: Stuart A. Knock <Stuart@tvb.invalid>

"""

# Third party python libraries
import numpy

"""
# Try and import from "The Virtual Brain"
from tvb.simulator.common import get_logger
LOG = get_logger(__name__)

#Import from tvb.simulator modules:
import tvb.simulator.simulator as simulator
import tvb.simulator.models as models
import tvb.simulator.coupling as coupling
import tvb.simulator.integrators as integrators
import tvb.simulator.monitors as monitors

import tvb.datatypes.connectivity as connectivity

from matplotlib.pyplot import *
"""

from tvb.simulator.lab import *
import time
##----------------------------------------------------------------------------##
##-                      Perform the simulation                              -##
##----------------------------------------------------------------------------##

LOG.info("Configuring...")
#Initialise a Model, Coupling, and Connectivity.
oscilator = models.Generic2dOscillator(a=-0.7, b=-10.0, c=0.0, d=0.02)
white_matter = connectivity.Connectivity()
white_matter.speed = numpy.array([1000.0])
white_matter_coupling = coupling.Linear(a=0.0)

#Initialise an Integrator
heunint = integrators.EulerDeterministic(dt=0.1)

#Initialise some Monitors with period in physical time
momo = monitors.Raw()
#mama = monitors.TemporalAverage(period=2**-2)

#Bundle them
what_to_watch = (momo)

#Initialise a Simulator -- Model, Connectivity, Integrator, and Monitors.
sim = simulator.Simulator(model = oscilator, connectivity = white_matter,
                          coupling = white_matter_coupling, 
                          integrator = heunint, monitors = what_to_watch)

sim.configure()

LOG.info("Starting simulation...")
#Perform the simulation
raw_data = []
raw_time = []
tavg_data = []
tavg_time = []
tic = time.time()
for raw in sim(simulation_length=2**11):
    if not raw is None:
        raw_time.append(raw[0][0])
        raw_data.append(raw[0][1])
toc = time.time()
elapsed = toc -tic
print str(elapsed) + "seconds"
    #if not tavg is None:
    #    tavg_time.append(tavg[0])
    #    tavg_data.append(tavg[1])

LOG.info("Finished simulation.")

##----------------------------------------------------------------------------##
##-               Plot pretty pictures of what we just did                   -##
##----------------------------------------------------------------------------##

#Plot defaults in a few combinations

#Make the lists numpy.arrays for easier use.
RAW = numpy.array(raw_data)
#TAVG = numpy.array(tavg_data)

#Plot raw time series
figure(1)
plot(raw_time, RAW[:, 0, :, 0])
title("Raw -- State variable 0")

figure(2)
plot(raw_time, RAW[:, 1, :, 0])
title("Raw -- State variable 1")

#Plot temporally averaged time series
#figure(3)
#plot(tavg_time, TAVG[:, 0, :, 0])
#title("Temporal average")

#Show them
show()
###EoF###