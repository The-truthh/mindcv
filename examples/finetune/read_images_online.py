""" Read images online """
import numpy as np

from mindspore.dataset import GeneratorDataset


class ImageClsDataset:
    def __init__(self, annotation_dir, images_dir):
        # Read annotations
        self.annotation = {}
        with open(annotation_dir, "r") as f:
            lines = f.readlines()
            for line in lines:
                image_label = line.replace("\n", "").replace("/", "_").split(" ")
                image = image_label[0] + ".jpg"
                label = " ".join(image_label[1:])
                self.annotation[image] = label

        # Transfer string-type label to int-type label
        self.label2id = {}
        labels = sorted(list(set(self.annotation.values())))
        for i in labels:
            self.label2id[i] = labels.index(i)

        for image, label in self.annotation.items():
            self.annotation[image] = self.label2id[label]

        # Read image-labels as mappable object
        label2images = {key: [] for key in self.label2id.values()}
        for image, label in self.annotation.items():
            read_image = np.fromfile(images_dir + image, dtype=np.uint8)
            label2images[label].append(read_image)

        self._data = sum(list(label2images.values()), [])
        self._label = sum([[i] * len(label2images[i]) for i in label2images.keys()], [])

    # make class ImageClsDataset a mappable object
    def __getitem__(self, index):
        return self._data[index], self._label[index]

    def __len__(self):
        return len(self._data)


# take aircraft dataset as an example
annotation_dir = "./aircraft/data/images_variant_trainval.txt"
images_dir = "./aircraft/data/images/"
dataset = ImageClsDataset(annotation_dir, images_dir)
dataset_train = GeneratorDataset(source=dataset, column_names=["image", "label"], shuffle=True)
