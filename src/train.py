import csv
import os
import pickle

import sklearn.svm as svm

Sample = tuple[float, float, float, str]

labels: list[str] = []


def label_to_int(label: str) -> int:
    if label not in labels:
        labels.append(label)
    return labels.index(label)


def train(data_dir: str, model_dest: str) -> None:

    all_sources = [f for f in os.listdir(data_dir) if f.endswith('.csv')]
    all_samples: list[Sample] = []

    for file_name in all_sources:
        file_name = os.path.join(data_dir, file_name)
        label = file_name.split(os.sep)[-1].split('.')[0]

        with open(file_name, 'r', newline='') as f:
            reader = csv.reader(f, delimiter=',', lineterminator='\n')
            for row in reader:
                all_samples.append((float(row[0]), float(row[1]), float(row[2]), label))

    model = svm.SVC(kernel='linear', C=1.0)
    y = [label_to_int(s[3]) for s in all_samples]
    X = [list(s[:3]) for s in all_samples]
    model.fit(X, y)

    with open(model_dest, 'wb') as f:
        pickle.dump(model, f)
