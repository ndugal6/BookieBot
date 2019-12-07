# launching point https://pytorch.org/tutorials/beginner/data_loading_tutorial.html

from __future__ import print_function, division
import os
import torch
import pandas as pd
from skimage import io, transform
import numpy as np
import matplotlib.pyplot as plt
from torch.utils.data import Dataset, DataLoader
from torchvision import transforms, utils
from pathlib import Path

# Ignore warnings
import warnings

from source.Predicting.datasets import FaceLandmarksDataset
from source.Predicting.transforms import RandomCrop, Rescale, ToTensor

warnings.filterwarnings("ignore")

plt.ion()  # interactive mode

DATA_FOLDER = Path(".").resolve() / 'dummyData'


def show_landmarks(image, landmarks):
    """Show image with landmarks"""
    plt.imshow(image)
    plt.scatter(landmarks[:, 0], landmarks[:, 1], s=10, marker='.', c='r')
    plt.pause(0.001)  # pause a bit so that plots are updated


def main():
    '''quickly read the CSV and get the annotations in an (N, 2) array where N is the number of landmarks.'''
    landmarks_frame = pd.read_csv(DATA_FOLDER / 'faces/face_landmarks.csv')

    n = 65
    img_name = landmarks_frame.iloc[n, 0]
    landmarks = landmarks_frame.iloc[n, 1:].as_matrix()
    landmarks = landmarks.astype('float').reshape(-1, 2)  # from (136,) to (-1,2); -1 w/e needed to form to 2.. see docs

    print('Image name: {}'.format(img_name))
    print('Landmarks shape: {}'.format(landmarks.shape))
    print('First 4 Landmarks: {}'.format(landmarks[:4]))

    plt.figure()
    show_landmarks(io.imread(DATA_FOLDER / str('faces/' + img_name)),
                   landmarks)
    plt.show()


def dataset_classes():
    """ iterate through the data samples. We will print the sizes of first 4 samples and show their landmarks."""
    face_dataset = FaceLandmarksDataset(csv_file='dummyData/faces/face_landmarks.csv',
                                        root_dir='dummyData/faces/')
    fig = plt.figure()

    for i in range(len(face_dataset)):
        sample = face_dataset[i]

        print(i, sample['image'].shape, sample['landmarks'].shape)

        ax = plt.subplot(1, 4, i + 1)
        plt.tight_layout()
        ax.set_title('Sample #{}'.format(i))
        ax.axis('off')
        show_landmarks(**sample)

        if i == 3:
            plt.show()
            break

def compose_transforms():
    """Let’s say we want to rescale the shorter side of the image to 256 and then randomly crop a square of size 224 from it. i.e, we want to compose Rescale and RandomCrop transforms. torchvision.transforms.Compose is a simple callable class which allows us to do this."""
    scale = Rescale(256)
    crop = RandomCrop(128)
    composed = transforms.Compose([Rescale(256),
                                   RandomCrop(224)])
    face_dataset = FaceLandmarksDataset(csv_file='dummyData/faces/face_landmarks.csv',
                                        root_dir='dummyData/faces/')

    # Apply each of the above transforms on sample.
    fig = plt.figure()
    sample = face_dataset[65]
    for i, tsfrm in enumerate([scale, crop, composed]):
        transformed_sample = tsfrm(sample)

        ax = plt.subplot(1, 3, i + 1)
        plt.tight_layout()
        ax.set_title(type(tsfrm).__name__)
        show_landmarks(**transformed_sample)

    plt.show()

if __name__ == '__main__':
    pass


