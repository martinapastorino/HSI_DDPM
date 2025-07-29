# HSI_DDPM
Hyperspectral Image Synthesis through Deep Diffusion Models


This repository contains the code related to the CVPRW25 and IGARSS25 papers:  

M. Pastorino, M. Alibani, N. Acito, and G. Moser, "Deep Diffusion Models and Unsupervised Hyperspectral Unmixing for Realistic Abundance Map Synthesis," in Proceedings of the Computer Vision and Pattern Recognition Conference Workshops, 3038-3046, 2025: [https://openaccess.thecvf.com/content/CVPR2025W/MORSE/papers/Pastorino_Deep_Diffusion_Models_and_Unsupervised_Hyperspectral_Unmixing_for_Realistic_Abundance_CVPRW_2025_paper.pdf](https://openaccess.thecvf.com/content/CVPR2025W/MORSE/papers/Pastorino_Deep_Diffusion_Models_and_Unsupervised_Hyperspectral_Unmixing_for_Realistic_Abundance_CVPRW_2025_paper.pdf)


M. Pastorino, M. Alibani, N. Acito, and G. Moser, "Synthesis of abundance maps through blind hyperspectral unmixing and deep diffusion models," in Proceedings of IEEE Geoscience and Remote Sensing Symposium (IGARSS), 2025.


When using this work, please cite our CVPRw25 paper:

M. Pastorino, M. Alibani, N. Acito, and G. Moser, "Deep Diffusion Models and Unsupervised Hyperspectral Unmixing for Realistic Abundance Map Synthesis," in Proceedings of the Computer Vision and Pattern Recognition Conference, 3038-3046, 2025. 

```
@ARTICLE{cvprw25_dm_abu,
  author={Pastorino, Martina and Alibani, Michael and Acito, Nicola and Moser, Gabriele},
  journal={IEEE/CVF Computer Vision and Pattern Recognition Conference Workshops}, 
  title={Deep Diffusion Models and Unsupervised Hyperspectral Unmixing for Realistic Abundance Map Synthesis}, 
  year={2025},
  volume={},
  number={},
  pages={3038-3046},
  url={https://openaccess.thecvf.com/content/CVPR2025W/MORSE/papers/Pastorino_Deep_Diffusion_Models_and_Unsupervised_Hyperspectral_Unmixing_for_Realistic_Abundance_CVPRW_2025_paper.pdf}
}

```


## :gear: Installation

The code was built on a virtual environment running on Python 3.10

### Step :one:: Clone the repository

```
git clone --recursive https://github.com/martinapastorino/HSI_DDPM.git
```

### Step :two:: Install the dependencies

```
cd HSI_DDPM

pip install -r requirements.txt
```

### Step :three:: Run the code

1. Train the model on a scarce GT set 

```
python main.py -r -g conncomp
```
2. Infer on data

```
python main.py -g full
```

## :rainbow: Blind Hyperspectral Unmixing

This model works with a dictionary of unmixing methods (any method can be chosen). You can apply any method of your preference to extract endmembers and abundances. For this project, some methods presented in "B. Rasti, A. Zouaoui, J. Mairal, J. Chanussot, Image Processing and Machine Learning for Hyperspectral Unmixing: An Overview and the HySUPP Python Package, _IEEE TGRS_" [https://ieeexplore.ieee.org/document/10508406](https://ieeexplore.ieee.org/document/10508406) and implemented in [https://github.com/BehnoodRasti/HySUPP/tree/main](https://github.com/BehnoodRasti/HySUPP/tree/main) where employed. The model is trained on the PRISMA dataset, but it can be applied to any hyperspectral dataset. 

Once the unmixing is performed, the data should have the following structure:

```
dataset
├── unmixing_abundances
    └── {}_UNMIXING_METHOD_NAME.mat 
```

The `.mat` file should contain a field called 'Abu', where the abundance map is stored with shapes $N \times N \times p$ with $N$ the patch size and $p$ the number of endmembers (in the case selected here as an example, $N=256$ and $p=9$).

The name of the unmixing methods selected must be inserted in the file `config\PRISMA_256_DDPM.json` under the field `"unmixing_methods"`

## :cyclone: Classifier-free Guided Diffusion Model

### :running: DM Training

Input: abundances obtained by the blind hyperspectral unmixing dictionary of your choice

`python Diffusion.py -p train -c config/PRISMA_256_DDPM.json`

### :





For synthesizing abundance maps, please modify the 'resume_state' in the json file, and run:

python Diffusion.py -p val -c config/Chikusei_256_DDPM.json

After that, we can obtain the synthesized abundance in ./experiments/ddpm/\*/mat_results/.

Here you can substitute the 

## :new_moon_with_face: License

The code is released under the GPL-3.0-only license. See `LICENSE.md` for more details.

## :eyes: Acknowledgements

...
