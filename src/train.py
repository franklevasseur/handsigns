import csv
import pathlib as pl
import pickle
from dataclasses import dataclass

import sklearn.svm as svm

from . import logger as log
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


def train(data_dir: pl.Path, model_dest: pl.Path, logger: log.Logger) -> None:

    logger.info(f"Training model with data from {data_dir}")

    all_sources = [f for f in data_dir.iterdir() if f.name.endswith('.csv')]
    all_samples: list[Sample] = []

    labels: list[str] = []
    label_to_int = mk_label_to_int(labels)

    for file_path in all_sources:
        file_path = data_dir / file_path
        label = file_path.stem
        with open(file_path, 'r', newline='') as f:
            reader = csv.reader(f, delimiter=',', lineterminator='\n')
            for row in reader:
                x = [float(f) for f in row]
                all_samples.append(Sample(x=x, y=label_to_int(label)))

    model = svm.SVC(kernel='linear', C=1.0, probability=True)
    y = [s.y for s in all_samples]
    X = [s.x for s in all_samples]
    model.fit(X, y)

    artifact = TrainArtifact(model=model, labels=labels)

    with open(model_dest, 'wb') as f:
        pickle.dump(artifact, f)
