'''
fresh docker:
    docker run --name wf-sess -p 3306:3306 -e MYSQL_ROOT_PASSWORD=tutorial datajoint/mysql
dependencies: pip install pytest pytest-cov
run all tests:
    pytest -sv --cov-report term-missing --cov=workflow-session -p no:warnings tests/
run one test, debug:
    pytest [above options] --pdb tests/tests_name.py -k function_name
'''

import os
import pytest
import pathlib
import datajoint as dj

import workflow_session


# ------------------- SOME CONSTANTS -------------------

_tear_down = True

test_user_data_dir = pathlib.Path('./tests/user_data')
test_user_data_dir.mkdir(exist_ok=True)

# ------------------ GENERAL FUCNTION ------------------

def write_csv(content,path):
    """
    General function for writing strings to lines in CSV
    :param path: pathlib PosixPath
    :param content: list of strings, each as row of CSV
    """
    with open(path,'w') as f:
        for line in content:
            f.write(line+'\n')

# ------------------- FIXTURES -------------------

@pytest.fixture(autouse=True)
def dj_config():
    """ If dj_local_config exists, load"""
    if pathlib.Path('./dj_local_conf.json').exists():
        dj.config.load('./dj_local_conf.json')
    dj.config['safemode'] = False
    dj.config['custom'] = {
        'database.prefix': (os.environ.get('DATABASE_PREFIX')
                            or dj.config['custom']['database.prefix'])}
    return

@pytest.fixture
def pipeline():
    """ Loads workflow_session.pipeline lab, session, subject"""
    from workflow_session import pipeline

    yield {'subject': pipeline.subject,
           'session': pipeline.session,
           'lab': pipeline.lab}

    if _tear_down:
        pipeline.subject.Subject.delete()
        pipeline.session.Session.delete()
        pipeline.lab.Lab.delete()

@pytest.fixture
def lab_csv():
    """ Create a 'labs.csv' file"""
    lab_content = ["lab,lab_name,institution,address,time_zone,location,location_description",
                   "LabA,The Example Lab,Example Uni,'221B Baker St,London NW1 6XE,UK',UTC+0,Example Building,'2nd floor lab dedicated to all fictional experiments.'",
                   "LabB,The Other Lab,Other Uni,'Oxford OX1 2JD, United Kingdom',UTC+0,Other Building,'fictional campus dedicated to imaginary experiments.'"]
    lab_csv_path = pathlib.Path('./tests/user_data/lab/labs.csv')
    write_csv(lab_content,lab_csv_path)

    yield lab_content, lab_csv_path
    lab_csv_path.unlink()

@pytest.fixture
def lab_project_csv():
    """ Create a 'projects.csv' file"""
    lab_project_content = ["project,project_description,repositoryurl,repositoryname,pharmacology,viruses,slices,stimulus,surgery,codeurl",
                           "ProjA,Example project to populate element-lab,https://github.com/datajoint/element-lab/,element-lab,Subjects were administered 10ul sedative prior to surgery,Exemplarvirus administered 10d before experimental session,,videos generated programmatically see repository,Craniotomy performed by session experimenter,https://github.com/datajoint/element-lab/tree/main/element_lab",
                           "ProjB,Other example project to populate element-lab,https://github.com/datajoint/element-session/,element-session,,Exemplarvirus administered 8d study,,,,https://github.com/datajoint/element-session/tree/main/element_session"]
    lab_project_csv_path = pathlib.Path('./tests/user_data/lab/projects.csv')
    write_csv(lab_project_content,lab_project_csv_path)

    yield lab_project_content, lab_project_csv_path
    lab_project_csv_path.unlink()

@pytest.fixture
def lab_project_users_csv():
    """ Create a 'project_users.csv' file"""
    lab_project_user_content = ["user,project",
                                "Sherlock,ProjA",
                                "Sherlock,ProjB",
                                "Watson,ProjB",
                                "Dr. Candace Pert,ProjA"]
    lab_project_user_csv_path = pathlib.Path('./tests/user_data/lab/project_users.csv')
    write_csv(lab_project_user_content,lab_project_user_csv_path)

    yield lab_project_user_content, lab_project_user_csv_path
    lab_project_user_csv_path.unlink()

@pytest.fixture
def lab_publications_csv():
    """ Create a 'publications.csv' file"""
    lab_publication_content = ["project,publication",
                               "ProjA,arXiv:1807.11104",
                               "ProjA,arXiv:1807.11104v1"]
    lab_publication_csv_path = pathlib.Path('./tests/user_data/lab/publications.csv')
    write_csv(lab_publication_content, lab_publication_csv_path)

    yield lab_publication_content, lab_publication_csv_path
    lab_publication_csv_path.unlink()

@pytest.fixture
def lab_keywords_csv():
    """ Create a 'keywords.csv' file"""
    lab_keyword_content = ["project,keyword",
                           "ProjA,Study",
                           "ProjA,Example",
                           "ProjB,Alternate"]
    lab_keyword_csv_path = pathlib.Path('./tests/user_data/lab/keywords.csv')
    write_csv(lab_keyword_content,lab_keyword_csv_path)

    yield lab_keyword_content, lab_keyword_csv_path
    lab_keyword_csv_path.unlink()

@pytest.fixture
def lab_protocol_csv():
    """ Create a 'protocols.csv' file"""
    lab_protocol_content = ["protocol,protocol_type,protocol_description",
                            "ProtA,IRB expedited review,Protocol for managing data ingestion",
                            "ProtB,Alternative Method,Limited protocol for piloting only"]
    lab_protocol_csv_path = pathlib.Path('./tests/user_data/lab/protocols.csv')
    write_csv(lab_protocol_content,lab_protocol_csv_path)

    yield lab_protocol_content, lab_protocol_csv_path
    lab_protocol_csv_path.unlink()

@pytest.fixture
def lab_user_csv():
    """ Create a 'users.csv' file"""
    lab_user_content = ["lab,user,user_role,user_email,user_cellphone",
                        "LabA,Sherlock,PI,Sherlock@BakerSt.com,+44 20 7946 0344",
                        "LabA,Watson,Dr,DrWatson@BakerSt.com,+44 73 8389 1763",
                        "LabB,Dr. Candace Pert,PI,Pert@gmail.com,+44 74 4046 5899"]
    lab_user_csv_path = pathlib.Path('./tests/user_data/lab/users.csv')
    write_csv(lab_user_content,lab_user_csv_path)

    yield lab_user_content, lab_user_csv_path
    lab_user_csv_path.unlink()

@pytest.fixture
def ingest_lab(pipeline, lab_csv, lab_project_csv, lab_publications_csv,
               lab_keywords_csv, lab_protocol_csv, lab_user_csv,
               lab_project_users_csv):
    """ From workflow_session ingest.py, import ingest_lab, run """
    from workflow_session.ingest import ingest_lab
    _, lab_csv_path = lab_csv
    _, lab_project_csv_path = lab_project_csv
    _, lab_publication_csv_path = lab_publications_csv
    _, lab_keyword_csv_path = lab_keywords_csv
    _, lab_protocol_csv_path = lab_protocol_csv
    _, lab_user_csv_path = lab_user_csv
    _, lab_project_user_csv_path = lab_project_users_csv
    ingest_lab(lab_csv_path=lab_csv_path,
               project_csv_path=lab_project_csv_path,
               publication_csv_path=lab_publication_csv_path,
               keyword_csv_path=lab_keyword_csv_path,
               protocol_csv_path=lab_protocol_csv_path,
               users_csv_path=lab_user_csv_path,
               project_user_csv_path=lab_project_user_csv_path)
    return

# Subject data and ingestion
@pytest.fixture
def subjects_csv():
    """ Create a 'subjects.csv' file"""
    subject_content = ["subject,sex,subject_birth_date,subject_description,death_date,cull_method",
                       "subject5,F,2020-01-01 00:00:01,rich,2020-10-02 00:00:01,natural causes",
                       "subject6,M,2020-01-01 00:00:01,manuel,2020-10-03 00:00:01,natural causes"]
    subject_csv_path = pathlib.Path('./tests/user_data/subject/subjects.csv')
    write_csv(subject_content,subject_csv_path)

    yield subject_content, subject_csv_path
    subject_csv_path.unlink()


@pytest.fixture
def ingest_subjects(pipeline, subjects_csv):
    """From workflow_session ingest.py, import ingest_subjects, run"""
    from workflow_session.ingest import ingest_subjects
    _, subject_csv_path = subjects_csv
    ingest_subjects(subject_csv_path=subject_csv_path)
    return


# Session data and ingestion
@pytest.fixture
def sessions_csv():
    """ Create a 'sessions.csv' file"""
    session_csv_path = pathlib.Path('./tests/user_data/session/sessions.csv')
    session_content = ["subject,session_datetime,session_dir,session_note",
                       "subject5,2020-04-15 11:16:38,/subject5/session1,'Successful data collection, no notes'",
                       "subject6,2021-06-02 14:04:22,/subject6/session1,'Ambient temp abnormally low'"]
    write_csv(session_content,session_csv_path)

    yield session_content, session_csv_path
    session_csv_path.unlink()


@pytest.fixture
def ingest_sessions(ingest_subjects, sessions_csv):
    """From workflow_session ingest.py, import ingest_sessions, run"""
    from workflow_session.ingest import ingest_sessions
    _, session_csv_path = sessions_csv
    ingest_sessions(session_csv_path=session_csv_path)
    return

"""
# FUTURE FIXTURES, pending sharable example data
lab_sources_content=["source, source_name, contact_details, source_description"]
lab_sources_csv_path = pathlib.Path('./tests/user_data/lab/sources.csv')
write_csv(lab_sources_content,lab_sources_csv_path)
yeild lab_sources_content,lab_sources_csv_path
lab_sources_csv_path.unlink()
subject_allele_content=["allele, allele_standard_name,zygosity"]
subject_allele_csv_path = pathlib.Path('./tests/user_data/subject/allele.csv')
write_csv(subject_allele_content,subject_allele_csv_path)
yeild subject_allele_content,subject_allele_csv_path
subject_allele_csv_path.unlink()
subject_genotyping_content=[]
subject_genotyping_csv_path = pathlib.Path('./tests/user_data/subject/genotyping.csv')
write_csv(subject_genotyping_content,subject_genotyping_csv_path)
yeild subject_genotyping_content,subject_genotyping_csv_path
subject_genotyping_csv_path.unlink()
subject_line_content=["line, line_description, target_phenotype, is_active"]
subject_line_csv_path = pathlib.Path('./tests/user_data/subject/line.csv')
write_csv(subject_line_content,subject_line_csv_path)
yeild subject_line_content,subject_line_csv_path
subject_line_csv_path.unlink()
subject_source_content=["allele, source_identifier, source_url, expression_data_url"]
subject_source_csv_path = pathlib.Path('./tests/user_data/subject/source.csv')
write_csv(subject_source_content,subject_source_csv_path)
yeild subject_source_content,subject_source_csv_path
subject_source_csv_path.unlink()
subject_strain_content=["strain, strain_standard_name, strain_desc"]
subject_strain_csv_path = pathlib.Path('./tests/user_data/subject/strain.csv')
write_csv(subject_strain_content,subject_strain_csv_path)
yeild subject_strain_content,subject_strain_csv_path
subject_strain_csv_path.unlink()
subject_subjects_csv_path = pathlib.Path('./tests/user_data/subject/subjects.csv')
"""