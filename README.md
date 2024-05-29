
# SolarSAM
A Comprehensive BIPV potential assessment method for emerging city with SAM and satellite imagery 
![SolarSAM](https://github.com/AI4RELab/SolarSAM/assets/105758272/d28be072-bf72-4e15-a245-fcfbb7935206)

## 1. Introduction

SolarSAM is a city-scale potential assessment model for building-integrated photovoltaic.

This model is based on Segment Anything Model and Satellite imagery data.

In this script, a demo for an emerging city is provided.

## 2. Data Preparation

The data are collected Google Earth. For more details, please refer to the following link: [Google Earth](https://earth.google.com/web/)

and our paper.

## 3. Model Implementation

To run this model, you need to install the following packages:

samgeo

CV2

numpy

in python environment.

You can download these with
```shell
git clone https://github.com/AI4RELab/SolarSAM.git
```
or just download with Github GUI

## 4. Files

### Ablation/ 
|

| --prompt engineering.py

|

| In this file, the prompt engineering and visualization are provided.

|

| --Ablation.py

|

| In this file, the ablation study is provided.

### Inference/ 
|

| --inference.py

|

| In this file, the inference of SAM with the optimal parameters is provided.

|

| And the area of the rooftop is calcualted in this script.

## 5. Citation

If you use this model, please cite our paper.

The DOI:

The BibTex:
