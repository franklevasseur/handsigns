from dataclasses import dataclass

import sklearn.svm as svm


@dataclass
class TrainArtifact:
    model: svm.SVC
    labels: list[str]
