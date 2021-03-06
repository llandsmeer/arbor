# -*- coding: utf-8 -*-
#
# test_event_generators.py

import unittest

import arbor as arb

# to be able to run .py file from child directory
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

try:
    import options
except ModuleNotFoundError:
    from test import options

"""
all tests for event generators (regular, explicit, poisson)
"""

class EventGenerator(unittest.TestCase):

    def test_event_generator_regular_schedule(self):
        cm = arb.cell_local_label("tgt0")
        rs = arb.regular_schedule(2.0, 1., 100.)
        rg = arb.event_generator(cm, 3.14, rs)
        self.assertEqual(rg.target.label, "tgt0")
        self.assertEqual(rg.target.policy, arb.selection_policy.univalent)
        self.assertAlmostEqual(rg.weight, 3.14)

    def test_event_generator_explicit_schedule(self):
        cm = arb.cell_local_label("tgt1", arb.selection_policy.round_robin)
        es = arb.explicit_schedule([0,1,2,3,4.4])
        eg = arb.event_generator(cm, -0.01, es)
        self.assertEqual(eg.target.label, "tgt1")
        self.assertEqual(eg.target.policy, arb.selection_policy.round_robin)
        self.assertAlmostEqual(eg.weight, -0.01)

    def test_event_generator_poisson_schedule(self):
        ps = arb.poisson_schedule(0., 10., 0)
        pg = arb.event_generator("tgt2", 42., ps)
        self.assertEqual(pg.target.label, "tgt2")
        self.assertEqual(pg.target.policy, arb.selection_policy.univalent)
        self.assertEqual(pg.weight, 42.)

def suite():
    # specify class and test functions in tuple (here: all tests starting with 'test' from class EventGenerator
    suite = unittest.makeSuite(EventGenerator, ('test'))
    return suite

def run():
    v = options.parse_arguments().verbosity
    runner = unittest.TextTestRunner(verbosity = v)
    runner.run(suite())

if __name__ == "__main__":
    run()
