# Towards a Neural Language Model for Signature Extraction

# Description
This repository contains the source code and data on the experiments that where presented
in the paper "Towards a Neural Language Model for Signature Extraction"

* DOI: https://doi.org/10.1109/ISDFS.2017.7916497

# Preparation of experiment environment:
* Requirements: python2.7, pip

## Create virtual environment and activate it (optional)
* pip install virtualenv
* virtualenv exp
* . exp/bin/activate.fish

## Install dependencies
* pip install keras-2.0.4
* pip install scikit-learn-0.18.1
* pip install tensorflow-1.1.0-cp27  (CPU version, GPU version is tensorflow-GPU)

# Run the experiments
Experiments should be run in order. So to reproduce the neural language model experiment, run the script which name starts with 100, then 101, etc.

## To evaluate:
Run the 900 script. The -e parameter specifies the directory where the results should be stored.   

# Citation
If you plan to use this work, please use the following citation

@inproceedings{thaler2017towards,
  title={Towards a neural language model for signature extraction from forensic logs},
  author={Thaler, Stefan and Menkonvski, Vlado and Petkovic, Milan},
  booktitle={Digital Forensic and Security (ISDFS), 2017 5th International Symposium on},
  pages={1--6},
  year={2017},
  organization={IEEE}
}


# Work used in this paper:
## IPLoM Implentation:
Paper of IPLoM:
* Title: 2012, Makanju et al.,  "A lightweight algorithm for message type extraction in system application logs"
* DOI: http://dx.doi.org/10.1109/TKDE.2011.138

## Paper that provided IPLoM sourcecode:
* Title: 2014, He et al. , "An Evaluation Study on Log Parsing and Its Use in Log Mining"
* Link: http://jiemingzhu.github.io/pub/pjhe_dsn2016.pdf
* SourceCode: https://github.com/cuhk-cse/logparser/commit/d3fe123235899a2cf2d454434a3eb1a1222f03bd

## LogCluster implementation
* Title: 2015, Vaarandi et al. - LogCluster - A Data Clustering and Pattern Mining Algorithm for Event Logs
* SourceCode: https://github.com/ristov/logcluster/commit/eadbf25df94257dc3cf72bb79e672d257bbce616
