#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2022 Intel Corporation
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from .pattern import Pattern, pattern_registry
from collections import namedtuple, OrderedDict
import copy
from .. import graph_utils as util


@pattern_registry(pattern_type='AddClsToken')
class AddClsToken(Pattern):
    def __call__(self, model):

        pattern_mapping_config = {
            'AddClsToken': [
                {
                    'patterns': {
                        'in': [[(0, 'Transpose'), (1, 'Shape'), (2, 'Gather'), (3, 'Unsqueeze'), (4, 'Concat'),
                                (5, 'Reshape'), (6, 'Shape'), (7, 'ConstantOfShape'), (8, 'Mul'), (9, 'Equal'),
                                (10, 'Where'), (11, 'Expand'), (12, 'Concat')]],
                        'out': [[(0, 'Transpose'), (1, 'Concat')]]
                    },
                    'search_mode': 'op_type',
                    'node_names': {
                        0: 0,
                        1: 12
                    },
                    'input_tensors': {
                        0: [[{
                            0: [0]
                        }], [[0], 1]],
                        1: [[{
                            11: [0]
                        }], [[0], 2]]
                    },
                    'output_tensors': {
                        0: [[{
                            0: [0]
                        }], [[0], 1]],
                        1: [[{
                            12: [0]
                        }], [[0], 1]]
                    },
                    'returns': [0, 12]
                }
            ]
        }

        for i in range(len(pattern_mapping_config['AddClsToken'])):
            pattern_dict = pattern_mapping_config['AddClsToken'][i]
            model, new_node_names, ret_old_nodes = util.pattern_mapping('AddClsToken',
                                                                        pattern_dict, model)
            if len(new_node_names) != 0:
                for j in range(len(new_node_names)):
                    transpose_node_idx = model.get_node_id(new_node_names[j][0])
                    model.nodes[transpose_node_idx].attr = ret_old_nodes[j][0].attr
                    concat_node_idx = model.get_node_id(new_node_names[j][1])
                    model.nodes[concat_node_idx].attr = ret_old_nodes[j][1].attr

                return model

        return model
