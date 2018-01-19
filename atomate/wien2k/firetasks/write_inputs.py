# coding: utf-8

from __future__ import division, print_function, unicode_literals, absolute_import

"""
This module defines tasks for writing wien2k input sets for various types of wien2k calculations
"""

import os
from six.moves import range
from importlib import import_module

import numpy as np

from fireworks import FiretaskBase, explicit_serialize
from fireworks.utilities.dict_mods import apply_mod
from pymatgen.core.structure import Structure
from pymatgen.alchemy.materials import TransformedStructure
from pymatgen.alchemy.transmuters import StandardTransmuter
#TODO dupe from pymatgen.io.vasp import Incar, Poscar, Potcar, PotcarSingle
#TODO dupe from pymatgen.io.vasp.sets import MPStaticSet, MPNonSCFSet, MPSOCSet, MPHSEBSSet
from pymatgen.io.wien2k import Struct

from atomate.utils.utils import env_chk, load_class

__author__ = 'Eamon McDermott'
__email__ = 'eamon.mcdermott@cea.fr'


@explicit_serialize
class WriteWien2kFromIOSet(FiretaskBase):
    """
    Create WIEN2k input files using implementations of pymatgen's AbstractWien2kInputSet.
    An input set can be provided as an object or as a String/parameter combo.

    Required params:
        structure (Structure): structure
        vasp_input_set (AbstractWien2kInputSet or str): Either a Wien2kInputSet object or a string
            name for the WIEN2k input set (e.g., "MPRelaxSet").

    Optional params:
        wien2k_input_params (dict): When using a string name for WIEN2k input set, use this as a dict
            to specify kwargs for instantiating the input set parameters. For example, if you want
            to change the user_incar_settings, you should provide: {"user_incar_settings": ...}.
            This setting is ignored if you provide the full object representation of a Wien2kInputSet
            rather than a String.
    """

    required_params = ["structure", "wien2k_input_set"]
    optional_params = ["wien2k_input_params"]

    def run_task(self, fw_spec):
        # if a full Wien2kInputSet object was provided
        if hasattr(self['wien2k_input_set'], 'write_input'):
            vis = self['wien2k_input_set']

        # if Wien2kInputSet String + parameters was provided
        else:
            vis_cls = load_class("pymatgen.io.wien2k.sets", self["wien2k_input_set"])
            vis = vis_cls(self["structure"], **self.get("wien2k_input_params", {}))
        vis.write_input(".")

@explicit_serialize
class WriteWien2kFromPMGObjects(FiretaskBase):
    """
    Write WIEN2k files using pymatgen objects.

    Required params:
        case: case name

    Optional params:
        incar (Incar): pymatgen Incar object
        poscar (Poscar): pymatgen Poscar object
        kpoints (Kpoints): pymatgen Kpoints object
        potcar (Potcar): pymatgen Potcar object
    """
    pass
    required_params = ["case"]
    optional_params = ["struct", "in0", "kpoints", "in1", "in2"]
#TODO test and rehash this
    def run_task(self, fw_spec):
        if "incar" in self:
            self["struct"].write_file(self.case+".struct") #??
        if "poscar" in self:
            self["poscar"].write_file("POSCAR")
        if "kpoints" in self:
            self["kpoints"].write_file("KPOINTS")
        if "potcar" in self:
            self["potcar"].write_file("POTCAR")



@explicit_serialize
class WriteWien2kStaticFromPrev(FiretaskBase):
    """
    Writes input files for a static run. Assumes that output files from a previous
    (e.g., optimization) run can be accessed in current dir or prev_calc_dir.
    """

    optional_params = ["prev_calc_dir"]

    def run_task(self, fw_spec):

        default_reciprocal_density = 200
        other_params = self.get("other_params", {})
        user_settings = other_params.get("user_settins", {})

        vis = MPStaticSet.from_prev_calc(prev_calc_dir=self.get("prev_calc_dir", "."))

        vis.write_input(".")

        #TODO implement wien2k sets.py for MPStaticSet