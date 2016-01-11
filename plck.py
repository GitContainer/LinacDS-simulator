#!/usr/bin/python
# -*- coding: utf-8 -*-

# LinacSimulator.py
# This file is part of tango-ds (http://sourceforge.net/projects/tango-ds/)
#
# tango-ds is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# tango-ds is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with tango-ds.  If not, see <http://www.gnu.org/licenses/>.

'''Simulation of the PLC for the Linac's klystrons control at ALBA.
'''

from numpy import array,uint8
import PyTango

READSIZE = 64
WRITESIZE = 18

memoryMap = array([0x00]*(READSIZE),dtype=uint8)

#---- Read from li/ct/plc4 the 20130626
#     first level keys:
#      - type: type of stored data
#      - read_{addr,bit,value}: memory position when memory is send to read
#      - write_{addr,bit,value}: memory position from the received memory to write
#     second level keys:
#      - updatable: this attribute has some noise
#      - std: how big is the noise of this attribute
#      - step: on each refresh loop the change to do.
#      - reference: (TODO) key whose name is readback
#      - formula: (TODO) in case is more a reference than a readback
attributes = \
{'HVPS_I': {'read_addr': 16,
            'read_value': 0.0,
            'type': ('f', 4),
            'updatable':True,
            'std':1.01},
 'HVPS_Interlock_RC': {'read_addr': 62,
                       'read_bit': 2,
                       'read_value': False,
                       'type': PyTango.DevBoolean,
                       'write_addr': 16,
                       'write_bit': 2,
                       'write_value': False},
 'HVPS_ONC': {'read_addr': 62,
              'read_bit': 3,
              'read_value': False,
              'type': PyTango.DevBoolean,
              'write_addr': 16,
              'write_bit': 3,
              'write_value': False},
 'HVPS_ST': {'read_addr': 39,
             'read_value': 8,
             'type': ('B', 1),
             'updatable':False,'range':9},
 'HVPS_V': {'read_addr': 12,
            'read_value': 0.0,
            'type': ('f', 4),
            'updatable': True,
            'std': 0.25,
            'step':0.5,
            'reference':'HVPS_V_setpoint',
            'switch':'HVPS_ONC'},
 'HVPS_V_setpoint': {'read_addr': 46,
                     'read_value': 0.0,
                     'type': ('f', 4),
                     'write_addr': 0,
                     'write_value': 0.0},
 'HeartBeat': {'read_addr': 36,
               'read_bit': 0,
               'read_value': False,
               'type': PyTango.DevBoolean},
 'HEAT_I': {'read_addr': 4,
            'read_value': 0.0,
            'type': ('f', 4),
            'updatable': True,
            'std': 1.01},
 'HEAT_ST': {'read_addr': 38,
             'read_value': 5,
             'type': ('B', 1),
             'updatable':False,'range':5},
 'HEAT_T':  {'read_addr': 44,
             'read_value': 10,
             'type': ('h', 2)},
 'HEAT_V': {'read_addr': 8,
            'read_value': 0.0,
            'type': ('f', 4),
            'updatable': True,
            'std': 1.01},
 'LV_Interlock_RC': {'read_addr': 62,
                     'read_bit': 0,
                     'read_value': False,
                     'type': PyTango.DevBoolean,
                     'write_addr': 16,
                     'write_bit': 0,
                     'write_value': False},
 'LV_ONC': {'read_addr': 62,
            'read_bit': 1,
            'read_value': False,
            'type': PyTango.DevBoolean,
            'write_addr': 16,
            'write_bit': 1,
            'write_value': False},
 'LV_ST': {'read_addr': 37,
           'read_value': 12,
           'type': ('B', 1),
           'updatable':False,'range':12},
 'LV_Time': {'read_addr': 42,
             'read_value': 10,
             'type': ('h', 2),
             #'updatable':True,'range':[0,300]
             },
 'Lock_ST': {'read_addr': 41,
             'read_value': 0,
             'type': ('B',1)},
 'Locking': {'read_addr': 63,
             'read_bit': 0,
             'read_value': False,
             'type': PyTango.DevBoolean,
             'write_addr': 17,
             'write_bit': 0,
             'write_value': False},
 'PEAK_I': {'read_addr': 20,
            'read_value': 0.0,
            'type': ('f', 4),
            'updatable': True,
            'std': 1.01},
 'PEAK_V': {'read_addr': 24,
            'read_value': 0.0,
            'type': ('f', 4),
            'updatable': True,
            'std': 1.01},
 'PULSE_ST': {'read_addr': 40,
              'read_value': 7,
              'type': ('B', 1),
              'updatable':False,'range':8}}

#---- Read from li/ct/plc5 the 20130626
#{'HVPS_I': {'read_addr': 16,
#            'read_value': 0.043401718139648438,
#            'type': ('f', 4),
#            'write_addr': None,
#            'write_value': None},
# 'HVPS_Interlock_RC': {'read_addr': 62,
#                       'read_bit': 2,
#                       'read_value': False,
#                       'type': PyTango.DevBoolean,
#                       'write_addr': 16,
#                       'write_bit': 2,
#                       'write_value': False},
# 'HVPS_ONC': {'read_addr': 62,
#              'read_bit': 3,
#              'read_value': False,
#              'type': PyTango.DevBoolean,
#              'write_addr': 16,
#              'write_bit': 3,
#              'write_value': False},
# 'HVPS_ST': {'read_addr': 39,
#             'read_value': 8,
#             'type': ('B', 1),
#             'write_addr': None,
#             'write_value': None},
# 'HVPS_V': {'read_addr': 12,
#            'read_value': 0.05786895751953125,
#            'type': ('f', 4),
#            'write_addr': None,
#            'write_value': None},
# 'HVPS_V_setpoint': {'read_addr': 46,
#                     'read_value': 28.600032806396484,
#                     'type': ('f', 4),
#                     'write_addr': 0,
#                     'write_value': 28.600032806396484},
# 'HeartBeat': {'read_addr': 36,
#               'read_bit': 0,
#               'read_value': True,
#               'type': PyTango.DevBoolean,
#               'write_addr': None,
#               'write_bit': 0,
#               'write_value': None},
# 'Heat_I': {'read_addr': 4,
#            'read_value': 21.614048004150391,
#            'type': ('f', 4),
#            'write_addr': None,
#            'write_value': None},
# 'Heat_ST': {'read_addr': 38,
#             'read_value': 5,
#             'type': ('B', 1),
#             'write_addr': None,
#             'write_value': None},
# 'Heat_Time': {'read_addr': 44,
#               'read_value': 0,
#               'type': ('h', 2),
#               'write_addr': None,
#               'write_value': None},
# 'Heat_V': {'read_addr': 8,
#            'read_value': 22.908412933349609,
#            'type': ('f', 4),
#            'write_addr': None,
#            'write_value': None},
# 'LV_Interlock_RC': {'read_addr': 62,
#                     'read_bit': 0,
#                     'read_value': False,
#                     'type': PyTango.DevBoolean,
#                     'write_addr': 16,
#                     'write_bit': 0,
#                     'write_value': False},
# 'LV_ONC': {'read_addr': 62,
#            'read_bit': 1,
#            'read_value': True,
#            'type': PyTango.DevBoolean,
#            'write_addr': 16,
#            'write_bit': 1,
#            'write_value': True},
# 'LV_ST': {'read_addr': 37,
#           'read_value': 12,
#           'type': ('B', 1),
#           'write_addr': None,
#           'write_value': None},
# 'LV_Time': {'read_addr': 42,
#             'read_value': 300,
#             'type': ('h', 2),
#             'write_addr': None,
#             'write_value': None},
# 'Lock_ST': {'read_addr': 41,
#             'read_value': None,
#             'type': PyTango.DevString,
#             'write_addr': None,
#             'write_value': None},
# 'Locking': {'read_addr': 63,
#             'read_bit': 0,
#             'read_value': None,
#             'type': PyTango.DevBoolean,
#             'write_addr': 17,
#             'write_bit': 0,
#             'write_value': None},
# 'Peak_I': {'read_addr': 20,
#            'read_value': 0.0,
#            'type': ('f', 4),
#            'write_addr': None,
#            'write_value': None},
# 'Peak_V': {'read_addr': 24,
#            'read_value': 0.0,
#            'type': ('f', 4),
#            'write_addr': None,
#            'write_value': None},
# 'Pulse_ST': {'read_addr': 40,
#              'read_value': 7,
#              'type': ('B', 1),
#              'write_addr': None,
#              'write_value': None}}
