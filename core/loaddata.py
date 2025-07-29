import numpy as np
import torch.utils.data as data
import scipy.io as sio
import torch
import os
import cv2

def is_mat_file(filename):
    return any(filename.endswith(extension) for extension in [".mat"])

def datanorm(input):
    output = (input - input.min()) / (input.max() - input.min())
    return output


def data_transform(input,min_max=(-1, 1)):
    input = input - input.min()
    input = input / (input.max() + 1e-8)
    input = input * (min_max[1] - min_max[0]) + min_max[0]
    return input


def get_random_m():
    M = 5
    m_idx = np.random.randint(0,M)
    m_one_hot = np.zeros((M,256,256), dtype=np.float32)
    m_one_hot[m_idx,:,:] += 1

    return torch.tensor([m_one_hot], dtype=torch.float32).cuda()


# CFG TRAINING
class AbuDataset(data.Dataset):
    def __init__(self, image_dir, unmix_met_list, augment=None, use_3D=False):
        self.image_folders = os.listdir(image_dir)        
        self.image_files = []
        self.em_type_dict = {method: idx for idx, method in enumerate(unmix_met_list)}
        for i in self.image_folders:
            if is_mat_file(i):
                full_path = os.path.join(image_dir, i)
                self.image_files.append(full_path)
        self.augment = augment
        self.use_3Dconv = use_3D
        if self.augment:
            self.factor = 8
        else:
            self.factor = 1
            
        self.length = len(self.image_files)*self.factor
        
    def __getitem__(self, index):
        file_index = index
        aug_num = 0
        if self.augment:
            file_index = index // self.factor
            aug_num = int(index % self.factor)
        load_dir = self.image_files[file_index]
        data = sio.loadmat(load_dir)
        em_type_str = self.image_folders[file_index].split('_')[1].split('.')[0]
        em_type = self.em_type_dict[em_type_str]
        gt = np.array(data['Abu'][...], dtype=np.float32)
        gt[np.isnan(gt)] = 0
        if (np.any(gt) < 0 ):
            print("HERE")
        #gt = (gt - np.min(gt)) / (np.max(gt) - np.min(gt)) 
        gt = data_transform(gt)

        if self.use_3Dconv:
            gt = gt[np.newaxis, :, :, :]
            gt = torch.from_numpy(gt.copy()).permute(0, 3, 1, 2)
        else:
            gt = torch.from_numpy(gt.copy()).permute(2, 0, 1)


        # embedding the one-hot-encoded em_type to have the same shape of the Abu
        embedded_em = np.zeros(gt.shape, dtype=np.float32)[:len(self.em_type_dict)]
        embedded_em[em_type,:,:] += 1
        # print(embedded_em.shape)

        return {'Abu': gt, 'em': embedded_em}

    def __len__(self):
        return len(self.image_files)*self.factor