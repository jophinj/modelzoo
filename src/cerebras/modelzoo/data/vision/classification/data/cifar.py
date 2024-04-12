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

import torchvision

from cerebras.modelzoo.data.vision.classification.dataset_factory import (
    Processor,
)


class CIFAR10Processor(Processor):
    def __init__(self, params):
        super().__init__(params)
        self.allowable_split = ["train", "test"]
        self.num_classes = 10

    def create_dataset(self, use_training_transforms=True, split="train"):
        self.check_split_valid(split)
        transform, target_transform = self.process_transform(
            use_training_transforms
        )
        dataset = torchvision.datasets.CIFAR10(
            root=self.data_dir,
            train=use_training_transforms,
            transform=transform,
            target_transform=target_transform,
            download=False,
        )
        return dataset


class CIFAR100Processor(Processor):
    def __init__(self, params):
        super().__init__(params)
        self.allowable_split = ["train", "test"]
        self.num_classes = 100

    def create_dataset(self, use_training_transforms=True, split="train"):
        self.check_split_valid(split)
        transform, target_transform = self.process_transform(
            use_training_transforms
        )
        dataset = torchvision.datasets.CIFAR100(
            root=self.data_dir,
            train=use_training_transforms,
            transform=transform,
            target_transform=target_transform,
            download=False,
        )
        return dataset

    def create_vtab_dataset(
        self, use_1k_sample=True, train_split_percent=None, seed=42
    ):
        train_transform, train_target_transform = self.process_transform(
            use_training_transforms=True
        )
        eval_transform, eval_target_transform = self.process_transform(
            use_training_transforms=False
        )

        trainval_set = torchvision.datasets.CIFAR100(
            root=self.data_dir,
            train=True,
            transform=None,
            download=False,
        )
        test_set = torchvision.datasets.CIFAR100(
            root=self.data_dir,
            train=False,
            transform=eval_transform,
            download=False,
        )

        # By default, 90% of the official training split is used as a new
        # training split and the rest is used for validation
        train_percent = train_split_percent or 90
        val_percent = 100 - train_percent
        train_set, val_set = self.split_dataset(
            trainval_set, [train_percent, val_percent], seed
        )

        if use_1k_sample:
            train_set.truncate_to_idx(800)
            val_set.truncate_to_idx(200)

        train_set.set_transforms(
            transform=train_transform, target_transform=train_target_transform
        )
        val_set.set_transforms(
            transform=eval_transform, target_transform=eval_target_transform
        )

        return train_set, val_set, test_set
