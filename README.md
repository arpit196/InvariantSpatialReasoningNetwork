# Learning Invariant Representations with Spatial Reasoning Network

In this work, a new neural network architecture is described, the Spatial Reasoning Network, which is invariant to affine transformations including, scaling and shearing, than the standard CNN models.
The model consists of Multi-Scale Convolutions in its lower layers, to learn invariant representations of local patches. The output of these layers are passed to the Spatial Reasoning module that learns the invariant
geometric arrangements of the local features to discriminate between object classes, thus taking into account the object shape into context along with its appearance features (which are learned by CNNs)

To train and test the model and its invariance to different affine transformations, run
```
python run-mnist.py
```
