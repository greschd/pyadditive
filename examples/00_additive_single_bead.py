# Copyright (C) 2023 ANSYS, Inc. and/or its affiliates.
# SPDX-License-Identifier: MIT
#
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of
# this software and associated documentation files (the "Software"), to deal in
# the Software without restriction, including without limitation the rights to
# use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies
# of the Software, and to permit persons to whom the Software is furnished to do
# so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
"""
Single bead analysis
====================

This example shows how you can use PyAdditive to determine
melt pool characteristics for a given material and machine
parameter combinations.

Units are SI (m, kg, s, K) unless otherwise noted.
"""
###############################################################################
# Perform required imports and connect
# ------------------------------------
# Perform the required imports and connect to the Additive service.

import matplotlib.pyplot as plt

from ansys.additive.core import (
    Additive,
    AdditiveMachine,
    MeltPoolColumnNames,
    SimulationError,
    SingleBeadInput,
)

additive = Additive()

###############################################################################
# Get server connection information
# ---------------------------------
# Get server connection information using the :meth:`about() <Additive.about>` method.

additive.about()

###############################################################################
# Select material
# ---------------
# Select a material. You can use the
# :meth:`materials_list() <ansys.additive.core.additive.Additive.materials_list>`
# method to obtain a list of available materials.

additive.materials_list()

###############################################################################
# You can obtain the parameters for a single material by passing a name
# from the materials list to the
# :meth:`material() <ansys.additive.core.additive.Additive.material>`
# method.

material = additive.material("17-4PH")

###############################################################################
# Specify machine parameters
# --------------------------
# Specify machine parameters by first creating an
# :class:`AdditiveMachine <ansys.additive.core.machine.AdditiveMachine>` object
# then assigning the desired values. All values are in SI units (m, kg, s, K)
# unless otherwise noted.

machine = AdditiveMachine()

# Show available parameters
print(machine)

###############################################################################
# Set laser power and scan speed
# ------------------------------
# Set the laser power and scan speed.

machine.scan_speed = 1  # m/s
machine.laser_power = 300  # W

###############################################################################
# Specify inputs for single bead simulation
# -----------------------------------------
# Create a :class:`SingleBeadInput <ansys.additive.core.single_bead.SingleBeadInput>`
# object containing the desired simulation parameters.

input = SingleBeadInput(
    machine=machine, material=material, id="single-bead-example", bead_length=0.0012  # meters
)

###############################################################################
# Run simulation
# --------------
# Use the :meth:`simulate() <ansys.additive.core.additive.Additive.simulate>`
# method of the ``additive`` object to run the simulation. The returned object is a
# either a :class:`SingleBeadSummary <ansys.additive.core.single_bead.SingleBeadSummary>`
# object containing the input and a
# :class:`MeltPool <ansys.additive.core.single_bead.MeltPool>` or a
# :class:`SimulationError <ansys.additive.core.simulation.SimulationError>`.

summary = additive.simulate(input)
if isinstance(summary, SimulationError):
    raise Exception(summary.message)

###############################################################################
# Plot melt pool statistics
# -------------------------
# Obtain a :class:`Pandas DataFrame <pandas.DataFrame>` containing the melt pool
# statistics by using the :meth:`data_frame() <ansys.additive.core.single_bead.MeltPool.data_frame>`
# property of the ``melt_pool`` attribute of the ``summary`` object. Use the
# :meth:`DataFrame.plot() <pandas.DataFrame.plot>` method to plot the melt
# pool dimensions as a function of bead length.

df = summary.melt_pool.data_frame().multiply(1e6)  # convert from meters to microns
df.index *= 1e3  # convert bead length from meters to millimeters

df.plot(
    y=[
        MeltPoolColumnNames.LENGTH,
        MeltPoolColumnNames.WIDTH,
        MeltPoolColumnNames.DEPTH,
        MeltPoolColumnNames.REFERENCE_WIDTH,
        MeltPoolColumnNames.REFERENCE_DEPTH,
    ],
    ylabel="Melt Pool Dimensions (µm)",
    xlabel="Bead Length (mm)",
    title="Melt Pool Dimensions vs Bead Length",
)
plt.show()


###############################################################################
# List melt pool statistics
# -------------------------
# You can show a table of the melt pool statistics by typing the name of the
# data frame object and pressing enter. For brevity, the following code
# uses ``head()`` so that only the first few rows are shown.

df.head()

# .. note::
#    If running this example as a Python script, no output is shown.
###############################################################################
# Save melt pool statistics
# -------------------------
# Save the melt pool statistics to a CSV file using the
# :meth:`to_csv() <pandas.DataFrame.to_csv>` method.

df.to_csv("melt_pool.csv")
