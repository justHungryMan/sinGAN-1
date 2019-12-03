# sinGAN Pytorch Implementation

## Paper

[SinGAN: Learning a Generative Model from a Single Natural Image](https://arxiv.org/abs/1905.01164), ICCV 2019, Best Paper Award


## Getting Started

### Prerequisite - Very Critical
- This repository has huge dependency on my custom module, [chanye](https://github.com/bocharm/chanye). I highly recommend to `git clone` this repo and add to your `PYTHON PATH`
- Your data should be inside of `get_dataset_path()` methods. [Reference](https://github.com/bocharm/chanye/blob/master/_settings.py)
- `get_dataset_path()` determine the path through `os.environ()` and environment variable is set through `-- location` flag in `main.py`. 

### Installation
- Clone this repo:
```bash
git clone https://github.com/bocharm/sinGAN.git
cd sinGAN
```
- Install PyTorch and dependencies from http://pytorch.org   

### Model Training
- Train a model:
```
python main.py --location server
```

### Datasets


## Results of this implementation

#### Random samples
- Train Image

![](assets/inputs/birds.png)
- Model Output (Random Sampled)

![](assets/samples/birds_randomsample.jpg)

#### paint to image
- Train Image 

![](assets/inputs/cows.png)

![](assets/inputs/cows_naive.png)

- Model Output (image order : from coarsest scale to finest scale)

![](assets/samples/cows_paint2image.png)

#### Harmonization
- Train Image 

![](assets/inputs/starry_night.png)

- Naive Image

![](assets/inputs/starry_night_naive.png)

- Model Output (image order : from coarsest scale to finest scale)

![](assets/samples/starry_night_harmonization.png)

#### Editing
- Train Image 

![](assets/inputs/stone.png)

- Naive Image

![](assets/inputs/stone_edit.png)

- Model Output (image order : from coarsest scale to finest scale)

![](assets/samples/stone_editing.png)


## TODO
- Other task in paper - Paint to img, Editing, Harmonization, SR, Animation
- Arbitrary aspect ratio, resolution

## Reference 
[sinGAN](https://github.com/tamarott/SinGAN) (Author Implementation)
