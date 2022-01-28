# Workflow for lab, subject and session management

This directory provides an example workflow to save the information related to lab, subject, and session metadata data management, using the following datajoint elements
+ [element-lab](https://github.com/datajoint/element-lab)
+ [element-animal](https://github.com/datajoint/element-animal)
+ [element-session](https://github.com/datajoint/element-session)

This repository provides demonstrations for:
Setting up a workflow using different elements (see [pipeline.py](workflow_session/pipeline.py))

## Workflow architecture
The lab and experiment subject management workflow presented here uses components from two DataJoint elements (element-lab, element-animal and element-session) assembled together into a functional workflow.

### element-lab

![element-lab](
https://github.com/datajoint/element-lab/raw/main/images/element_lab_diagram.svg)

### element-animal

![element-animal](
https://github.com/datajoint/element-animal/blob/main/images/subject_diagram.svg)

`genotyping` is designed for labs that handle animal care and genetic information themselves, which is optional.
![genotyping](https://github.com/datajoint/element-animal/blob/main/images/genotyping_diagram.svg)

### element-session
`session` is designed to handle metadata related to data collection, including collection date-time, file paths, and notes. Most workflows will include element-session as a starting point for further data entry.
![session](https://github.com/datajoint/element-session/blob/main/images/session_diagram.svg)

### This workflow
This workflow serves as an example of the upstream part of a typical data workflow, for examples using these elements in tandem with other data collection modalities, refer to:

+ [workflow-array-ephys](https://github.com/datajoint/workflow-array-ephys)
+ [workflow-calcium-imaging](https://github.com/datajoint/workflow-calcium-imaging)


## Installation instructions

+ The installation instructions can be found at [datajoint-elements/install.md](
     https://github.com/datajoint/datajoint-elements/blob/main/install.md).

## Interacting with the DataJoint workflow

+ Please refer to the following workflow-specific
[Jupyter notebooks](/notebooks) for an in-depth explanation of how to run the
workflow ([1-Explore_Workflow.ipynb](notebooks/1_Explore_Workflow.ipynb).
