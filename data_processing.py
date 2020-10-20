"""
The file is used to do the data process.

"""
import os
import torch
import numpy as np
import torchvision.models
from PIL import Image
import random


Alexnet = torchvision.models.alexnet(pretrained=True)

def data_processing(using_data: int, image_folder_path: str, data_entry_csv_path: str,
                    finding_labels: list, train_data_percent: float,
                    val_data_percent: float, test_data_percent: float,
                    output_folder_name="features", direction="PA"):
    """
    data processing
    :param using_data: total data we want to process(the number of images being
                        the sum of training/validation/test data)
    :param image_folder_path: the path of folder used to save image
    :param data_entry_csv_path: the path of csv used to save labels
    :param finding_labels: a list contains (diseases or 'No Finding')
    :param train_data_percent: training data percent
    :param val_data_percent: validation data percent
    :param test_data_percent: test data perent
    :param output_folder_name: the path of folder used to save train/test/val data
    :param direction: the view position
    :return: None
    """
    assert train_data_percent + val_data_percent + test_data_percent == 1, \
    "sum of train, val, test data is not 100% percent"

    image_map_label = get_data_map(using_data, data_entry_csv_path, finding_labels, direction)
    create_output_folder(output_folder_name+'_'+direction, finding_labels)

    first_pivot =  train_data_percent * 100
    second_pivot = (train_data_percent + val_data_percent) * 100
    train_num, val_num, test_num = 0, 0, 0
    for image_name, disease in image_map_label:

        # convert image from (1024 * 1024) to [224, 224], by using np array in float number
        image = np.asarray(Image.open(image_folder_path+'/'+image_name).resize((224, 224))) / 255.0

        # it is possible that image type is rgba, but we can convert to greyscale type
        if (image.shape == (224, 224, 4)):
            image = image[:, :, 0]


        # convert np array shape [224, 224] to tensor [1, 3, 224, 224], read
        # first dimension three times and add one dimension
        rgb_batch = torch.tensor(np.expand_dims(
            np.repeat(image[..., np.newaxis], 3, -1), axis=0)).transpose(1, 3).transpose(2,3).float()


        # put it into alexnet.features, output size should be [1, 256, 6, 6]
        features = Alexnet.features(rgb_batch)
        features_tensor = torch.from_numpy(features.detach().numpy())

        # save into given path
        n = random.randint(1, 100)
        if n < first_pivot: #add to train folder
            torch.save(features_tensor.squeeze(0),
                       output_folder_name + '_' + direction+ '/' + 'train'
                       + '/' + disease + '/' + image_name.split('.')[0] + '.tensor')
            train_num += 1
        elif n < second_pivot: # add to val folder
            torch.save(features_tensor.squeeze(0),
                       output_folder_name + '_' + direction + '/' + 'val'
                       + '/' + disease + '/' + image_name.split('.')[0] + '.tensor')
            val_num += 1
        else: #add to test folder
            torch.save(features_tensor.squeeze(0),
                       output_folder_name + '_' + direction + '/' + 'test'
                       + '/' + disease + '/' + image_name.split('.')[0] + '.tensor')
            test_num += 1
    print("There are {} training data, {} validation data and {} test data".format(
        train_num, val_num, test_num
    ))


def create_output_folder(output_folder_name: str, finding_labels: list):
    """
    create output data folder, and the subfolders
    """
    if not os.path.isdir(output_folder_name):
        os.mkdir(output_folder_name)
    for type in ['/train', '/val', '/test']:
        if not os.path.isdir(output_folder_name + type):
            os.mkdir(output_folder_name + type)
        for disease in finding_labels:
            if not os.path.isdir(output_folder_name + type + '/' + disease):
                os.mkdir(output_folder_name + type + '/' + disease)


def get_data_map(using_data: int,data_entry_csv_path: str,
                 finding_labels: list, direction: str):
    """
    read csv and return a list of tuple, the first element in tuple
    is image name, and second element is diagonized disease, in which
    the length of return list is <using_data> value
    """
    image_map_label = []
    file = open(data_entry_csv_path, 'r')
    title = file.readline() #first line is tile
    line = file.readline()
    n = 0
    while line is not None and line != '' and n != using_data:
        line = line.split(',')
        for finding in line[1].split('|'):
            if finding in finding_labels and line[6] == direction:
                image_map_label.append((line[0], finding))
                n += 1
        line = file.readline()
    file.close()
    return image_map_label




if __name__ == '__main__':
    data_processing(100, './images', './Data_Entry_2017.csv', ['Hernia', 'No Finding'], 0.6,0.2,0.2, 'test', 'PA')
