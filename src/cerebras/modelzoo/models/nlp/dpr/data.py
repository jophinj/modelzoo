# Copyright 2022 Cerebras Systems.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import sys

from cerebras.modelzoo.data.nlp.dpr.DPRSyntheticProcessor import (  # noqa
    DPRSyntheticDataProcessor,
)

from cerebras.modelzoo.data.nlp.dpr.DPRHDF5DataProcessor import (  # noqa
    DPRHDF5DataProcessor,
)


def train_input_dataloader(params):
    data_obj = getattr(
        sys.modules[__name__], params["train_input"]["data_processor"]
    )(params["train_input"])
    dataloader = data_obj.create_dataloader()
    return dataloader


def eval_input_dataloader(params):
    data_obj = getattr(
        sys.modules[__name__], params["eval_input"]["data_processor"]
    )(params["eval_input"])
    dataloader = data_obj.create_dataloader()
    return dataloader
