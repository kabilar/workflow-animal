# dependencies: pip install pytest pytest-cov
# run all tests: pytest -sv --cov-report term-missing --cov=workflow-array-ephys -p no:warnings tests/
# run one test, debug: pytest [above options] --pdb tests/tests_name.py -k function_name

import os
import pytest
import pandas as pd
import pathlib
import numpy as np
import datajoint as dj

import workflow_session
from workflow_session.paths import get_root_data_dir
import element_data_loader.utils


# ------------------- SOME CONSTANTS -------------------

_tear_down = True

test_user_data_dir = pathlib.Path('./tests/user_data')
test_user_data_dir.mkdir(exist_ok=True)

# ------------------- FIXTURES -------------------

@pytest.fixture(autouse=True)
def dj_config():
    """ If dj_local_config exists, load"""
    if pathlib.Path('./dj_local_conf.json').exists():
        dj.config.load('./dj_local_conf.json')
    dj.config['safemode'] = False
    dj.config['custom'] = {
        'database.prefix': (os.environ.get('DATABASE_PREFIX')
                            or dj.config['custom']['database.prefix']),
        'root_data_dir': (os.environ.get('ROOT_DATA_DIR')
                          or dj.config['custom']['root_data_dir'])
    }
    return


@pytest.fixture
def pipeline():
    from workflow_session import pipeline

    yield {'subject':           pipeline.subject,
           'lab':               pipeline.lab,
           'session':           pipeline.session,
           'get_root_data_dir': pipeline.get_root_data_dir}

    if _tear_down:
        pipeline.subject.Subject.delete()

@pytest.fixture
def lab_csv():
    input_lab = pd.DataFrame(columns=['lab', 'lab_name','institution',
                                      'address','time_zone','location',
                                      'location_description'])
    input_lab.lab = ['LabA','LabB']
    input_lab.lab_name = ['The Example Lab','The Other Lab']
    input_lab.institution = ['Example Uni','Other Uni']
    input_lab.address = ['221B Baker St,London NW1 6XE,UK','Oxford OX1 2JD, United Kingdom']
    input_lab.time_zone = ['UTC+0','UTC+0']
    input_lab.location = ['Example Building','Other Building']
    input_lab.location_description = ['2nd floor lab dedicated to all fictional experiments.',
                                      'fictional campus dedicated to imaginary experiments.']
    lab_csv_path = pathlib.Path('./tests/user_data/lab/labs.csv')
    input_lab.to_csv(lab_csv_path)  # write csv file
    yield input_lab, lab_csv_path
    lab_csv_path.unlink()  # delete csv file after use

@pytest.fixture
def lab_proj_csv():
    input_lab_proj = pd.DataFrame(columns=['project','project_description','repositoryurl','repositoryname','pharmacology','viruses','slices','stimulus','surgery','codeurl'])
    input_lab_proj.project = ['ProjA','ProjB']
    input_lab_proj.project_description = ['Example project to populate element-lab',
                                          'Other example project to populate element-lab']
    input_lab_proj.repositoryurl = ['https://github.com/datajoint/element-lab/',
                                    'https://github.com/datajoint/element-session/']
    input_lab_proj.repositoryname = ['element-lab','element-session']
    input_lab_proj.pharmacology = ['Subjects were administered 10ul sedative prior to surgery','']
    input_lab_proj.viruses = ['Exemplarvirus administered 10d before experimental session',
                              'Exemplarvirus administered 8d study']
    input_lab_proj.slices = ['','']
    input_lab_proj.stimulus = ['videos generated programmatically see repository','']
    input_lab_proj.surgery = ['Craniotomy performed by session experimenter','']
    input_lab_proj.codeurl = ['https://github.com/datajoint/element-lab/tree/main/element_lab',
                              'https://github.com/datajoint/element-session/tree/main/element_session']
    lab_proj_csv_path = pathlib.Path('./tests/user_data/lab/projects.csv')
    input_lab_proj.to_csv(lab_proj_csv_path)  # write csv file
    yield input_lab_proj, lab_proj_csv_path
    lab_proj_csv_path.unlink()

@pytest.fixture
def lab_pubs_csv():
    input_lab_pubs = pd.DataFrame(columns=['project','publication'])
    input_lab_pubs.project = ['ProjA','ProjA']
    input_lab_pubs.publication = ['arXiv:1807.11104','arXiv:1807.11104v1']
    lab_pubs_csv_path = pathlib.Path('./tests/user_data/lab/publications.csv')
    input_lab_X.to_csv(lab_X_csv_path)  # write csv file
    yield input_lab_pubs, lab_pubs_csv_path
    lab_pubs_csv_path.unlink()

@pytest.fixture
def lab_keyw_csv():
    input_lab_keyw = pd.DataFrame(columns=['project','keyword'])
    input_lab_keyw.project = ['ProjA','ProjA','ProjB']
    input_lab_keyw.keyword = ['Study','Example','Alternate']
    lab_keyw_csv_path = pathlib.Path('./tests/user_data/lab/keywords.csv')
    input_lab_keyw.to_csv(lab_keyw_csv_path)  # write csv file
    yield input_lab_keyw, lab_keyw_csv_path
    lab_keyw_csv_path.unlink()

@pytest.fixture
def lab_prot_csv():
    input_lab_prot = pd.DataFrame(columns=['protocol','protocol_type','protocol_description'])
    input_lab_prot.protocol = ['ProtA','ProtB']
    input_lab_prot.protocol_type = ['IRB expedited review','Alternative Method']
    input_lab_prot.protocol_description = ['Protocol for managing data ingestion','Limited protocol for piloting only']
    lab_prot_csv_path = pathlib.Path('./tests/user_data/lab/protocols.csv')
    input_lab_prot.to_csv(lab_prot_csv_path)  # write csv file
    yield input_lab_prot, lab_prot_csv_path
    lab_prot_csv_path.unlink()

@pytest.fixture
def subjects_csv():
    """ Create a 'subjects.csv' file"""
    input_subjects = pd.DataFrame(columns=['subject', 'sex',
                                           'subject_birth_date',
                                           'subject_description',
                                           'death_date','cull_method'])
    input_subjects.subject = ['subject5', 'subject6']
    input_subjects.sex = ['F', 'M']
    input_subjects.subject_birth_date = ['2020-01-01 00:00:01', '2020-01-01 00:00:01']
    input_subjects.subject_description = ['rich', 'manuel']
    input_sessions.death_date= ['2020-10-02 00:00:01', '2020-10-03 00:00:01']
    input_sessions.cull_method = ['natural causes', 'natural causes']
    input_subjects = input_subjects.set_index('subject')

    subjects_csv_path = pathlib.Path('./tests/user_data/animal/subjects.csv')
    input_subjects.to_csv(subjects_csv_path)  # write csv file

    yield input_subjects, subjects_csv_path

    subjects_csv_path.unlink()  # delete csv file after use


@pytest.fixture
def ingest_subjects(pipeline, subjects_csv):
    from workflow_session.ingest import ingest_subjects
    _, subjects_csv_path = subjects_csv
    ingest_subjects(subject_csv_path=subjects_csv_path)
    return


@pytest.fixture
def sessions_csv(test_data):
    """ Create a 'sessions.csv' file"""
    input_sessions = pd.DataFrame(columns=['subject', 'session_dir'])
    input_sessions.subject = ['subject1', 'subject2', 'subject2',
                              'subject3', 'subject4', 'subject5',
                              'subject6']
    input_sessions.session_dir = sessions_dirs
    input_sessions = input_sessions.set_index('subject')

    sessions_csv_path = pathlib.Path('./tests/user_data/sessions.csv')
    input_sessions.to_csv(sessions_csv_path)  # write csv file

    yield input_sessions, sessions_csv_path

    sessions_csv_path.unlink()  # delete csv file after use


@pytest.fixture
def ingest_sessions(ingest_subjects, sessions_csv):
    from workflow_session.ingest import ingest_sessions
    _, sessions_csv_path = sessions_csv
    ingest_sessions(sessions_csv_path)
    return

