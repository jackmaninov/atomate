# coding: utf-8

from __future__ import absolute_import, division, print_function, \
    unicode_literals

import warnings

#TODO from atomate.vasp.config import HALF_KPOINTS_FIRST_RELAX, RELAX_MAX_FORCE

"""
Defines standardized Fireworks that can be chained easily to perform various
sequences of WIEN2k calculations.
"""

from fireworks import Firework

from pymatgen import Structure
#TODO from pymatgen.io.wien2k.sets import MPRelaxSet, MITMDSet, MITRelaxSet, \
    MPStaticSet, MPSOCSet

from atomate.common.firetasks.glue_tasks import PassCalcLocs
#TODO from atomate.wien2k.firetasks.glue_tasks import CopyVaspOutputs, pass_vasp_result
#TODO from atomate.wien2k.firetasks.neb_tasks import TransferNEBTask
#TODO from atomate.wien2k.firetasks.parse_outputs import VaspToDb, BoltztrapToDb
#TODO from atomate.wien2k.firetasks.run_calc import RunVaspCustodian, RunBoltztrap
"""TODO from atomate.wien2k.firetasks.write_inputs import WriteNormalmodeDisplacedPoscar, \
    WriteTransmutedStructureIOSet, WriteVaspFromIOSet, WriteVaspHSEBSFromPrev, \
    WriteVaspNSCFFromPrev, WriteVaspSOCFromPrev, WriteVaspStaticFromPrev
    """
from atomate.wien2k.firetasks.write_inputs import WriteWien2kFromIOSet, \
    WriteWien2kStaticFromPrev, WriteWien2kFromPMGObjects
#TODO from atomate.vasp.firetasks.neb_tasks import WriteNEBFromImages, \
    WriteNEBFromEndpoints


class StaticFW(Firework):
    def __init__(self, structure, name="static", wien2k_input_set=None,
                 wien2kcmd="run",
                 prev_calc_loc=True, db_file=None, parents=None, **kwargs):
        """
        Standard static calculation Firework - either from a previous location or from a structure

        Args:
        :param structure: (Structure) Input structure. Note that for prev_calc_loc jobs, the
            structure is only used to set the name of the FW and any structure with the same
            composition can be used.
        :param name: Name for the Firework.
        :param wien2k_input_set: input set to use (for jobs w/no parents) Defaults to MPStaticSet()
            if None.
        :param wien2kcmd: Command to run WIEN2k.
        :param prev_calc_loc: (bool or str) if True (default), copies outputs from previous calc.
            If a str value, grabs a previous calculation output by name. If False/None, will create
            new static calculation using the provided structure.
        :param db_file: Path to file specifying db credentials.
        :param parents: (Firework) Parents of this particular Firework. FW or list of FWS.
        :param kwargs: Other kwargs that are passed to Firework.__init__.
        """

        t = []

        if parents:
            if prev_calc_loc:
                t.append(CopyWien2kOutputs(calc_loc=prev_calc_loc))
                t.append(WriteWien2kStaticFromPrev())