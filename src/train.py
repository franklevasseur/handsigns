import csv
import os
import pickle
from dataclasses import dataclass

import sklearn.svm as svm

from .typings import TrainArtifact


@dataclass
class Sample:
    x: list[float]
    y: int


def mk_label_to_int(labels: list[str]):
    def cb(label: str) -> int:
        if label not in labels:
            labels.append(label)
        return labels.index(label)
    return cb


def train(data_dir: str, model_dest: str) -> None:

    all_sources = [f for f in os.listdir(data_dir) if f.endswith('.csv')]
    all_samples: list[Sample] = []

    labels: list[str] = []
    label_to_int = mk_label_to_int(labels)

    for file_name in all_sources:
        file_name = os.path.join(data_dir, file_name)
        label = file_name.split(os.sep)[-1].split('.')[0]
        with open(file_name, 'r', newline='') as f:
            reader = csv.reader(f, delimiter=',', lineterminator='\n')
            for row in reader:
                x = [float(f) for f in row]
                all_samples.append(Sample(x=x, y=label_to_int(label)))

    model = svm.SVC(kernel='linear', C=1.0)
    y = [s.y for s in all_samples]
    X = [s.x for s in all_samples]
    model.fit(X, y)

    artifact = TrainArtifact(model=model, labels=labels)

    with open(model_dest, 'wb') as f:
        pickle.dump(artifact, f)
