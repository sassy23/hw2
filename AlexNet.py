import numpy as np

import torch.utils.data as data
import torch.nn as nn
import torch.utils.model_zoo as model_zoo

import torchvision.models as models
from torch.hub import load_state_dict_from_url

model_urls = {
        'alexnet': 'https://download.pytorch.org/models/alexnet-owt-4df8aa71.pth',
}


class LocalizerAlexNet(nn.Module):
    def __init__(self, num_classes=20):
        super(LocalizerAlexNet, self).__init__()
        #TODO: Define model
        self.num_classes = num_classes
        self.features = nn.Sequential(nn.Conv2d(3, 64, kernel_size=(11, 11), stride=(4, 4), padding=(2, 2)),
                        nn.ReLU(inplace=True),
                        nn.MaxPool2d(kernel_size=(3, 3), stride=(2, 2), dilation=(1, 1), ceil_mode=False),
                        nn.Conv2d(64, 192, kernel_size=(5, 5), stride=(1, 1), padding=(2, 2)),
                        nn.ReLU(inplace=True),
                        nn.MaxPool2d(kernel_size=(3, 3), stride=(2, 2), dilation=(1, 1), ceil_mode=False),
                        nn.Conv2d(192, 384, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1)),
                        nn.ReLU(inplace=True),
                        nn.Conv2d(384, 256, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1)),
                        nn.ReLU(inplace=True),
                        nn.Conv2d(256, 256, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1)),
                        nn.ReLU(inplace=True))
       
        self.classifier = nn.Sequential(nn.Conv2d(256, 256, kernel_size=(3, 3), stride=(1, 1)),
                        nn.ReLU(inplace=True),
                        nn.Conv2d(256, 256, kernel_size=(1, 1), stride=(1, 1)),
                        nn.ReLU(inplace=True),
                        nn.Conv2d(256, 20, kernel_size=(1, 1), stride=(1, 1)))
        


    def forward(self, x):
        #TODO: Define forward pass
        x = self.features(x)
        x = self.classifier(x)

        return x


class LocalizerAlexNetRobust(nn.Module):
    def __init__(self, num_classes=20):
        super(LocalizerAlexNetRobust, self).__init__()
        #TODO: Define model


    def forward(self, x):
        #TODO: Define fwd pass


        return x


def localizer_alexnet(pretrained=False, **kwargs):
    r"""AlexNet model architecture from the
    `"One weird trick..." <https://arxiv.org/abs/1404.5997>`_ paper.

    Args:
        pretrained (bool): If True, returns a model pre-trained on ImageNet
    """
    model = LocalizerAlexNet(**kwargs)
    #TODO: Initialize weights correctly based on whethet it is pretrained or not
    # if pretrained:
    #     state_dict = load_state_dict_from_url(model_urls["alexnet"], progress=True)
    #     model.load_state_dict(state_dict)

    alexnet_state_dict = load_state_dict_from_url(model_urls["alexnet"], progress=True)
    model_state_dict = model.state_dict()
    print(type(model_state_dict))
    if pretrained:
        
        for name, param in alexnet_state_dict.items():
            if 'features' in name:
                model_state_dict[name] = param
        for name, param in model_state_dict.items():
            if 'classifier' in name and 'weight' in name:
                nn.init.xavier_uniform_(param)
            elif 'classifier' in name and 'bias' in name:
                nn.init.zeros_(param)

    else:
        for name, param in model_state_dict.items():
            if 'features' in name and 'weight' in name:
                nn.init.xavier_uniform_(param)
            if 'classifier' in name and 'weight' in name:
                nn.init.xavier_uniform_(param)
            if 'features' in name and 'bias' in name:
                nn.init.zeros_(param)
            if 'classifier' in name and 'bias' in name:
                nn.init.zeros_(param)

    # print("Count= ", count)        
    return model


def localizer_alexnet_robust(pretrained=False, **kwargs):
    r"""AlexNet model architecture from the
    `"One weird trick..." <https://arxiv.org/abs/1404.5997>`_ paper.

    Args:
        pretrained (bool): If True, returns a model pre-trained on ImageNet
    """
    model = LocalizerAlexNetRobust(**kwargs)
    #TODO: Ignore for now until instructed
    

    return model