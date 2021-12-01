import pathlib
import csv
import re

from workflow_session.pipeline import lab, subject, session

from workflow_session.paths import get_root_data_dir
import element_data_loader.utils

def ingest_lab(lab_csv_path='./user_data/lab/labs.csv',
                project_csv_path='./user_data/lab/projects.csv',
                pubs_csv_path='./user_data/lab/publications.csv',
                keyw_csv_path='./user_data/lab/keywords.csv',
                protocol_csv_path='./user_data/lab/protocols.csv'
                ):
    # -------------- Insert new "Lab" --------------
    with open(lab_csv_path, newline= '') as f:
        input_labs = list(csv.DictReader(f, delimiter=','))
    print(f'\n---- Insert {len(input_labs)} entry(s) into lab tables ----')
    lab.Lab.insert(input_labs, skip_duplicates=True, ignore_extra_fields=True)
    lab.Location.insert(input_labs, skip_duplicates=True, ignore_extra_fields=True)
    # -------------- Insert new "Project" --------------
    with open(project_csv_path, newline= '') as f:
        input_projs = list(csv.DictReader(f, delimiter=','))
    print(f'\n---- Insert {len(input_projs)} entry(s) into project table ----')
    lab.Project.insert(input_projs, skip_duplicates=True, ignore_extra_fields=True)
    # -------------- Insert publications + keywords --------------
    with open(pubs_csv_path, newline= '') as f:
        input_pubs = list(csv.DictReader(f, delimiter=','))
    with open(keyw_csv_path, newline= '') as f:
        input_keyw = list(csv.DictReader(f, delimiter=','))
    print(f'\n---- Insert entry(s) into publication/keyword tables ----')
    lab.Project.Publication.insert(input_pubs, skip_duplicates=True, ignore_extra_fields=True)
    lab.Project.Keywords.insert(input_keyw, skip_duplicates=True, ignore_extra_fields=True)

    # -------------- Insert new "Protocol" --------------
    with open(protocol_csv_path, newline= '') as f:
        input_prots = list(csv.DictReader(f, delimiter=','))
    print(f'\n---- Insert {len(input_prots)} entry(s) into protocol tables ----')
    lab.Protocol.insert(input_prots, skip_duplicates=True, ignore_extra_fields=True)
    lab.ProtocolType.insert(input_prots, skip_duplicates=True, ignore_extra_fields=True)

def ingest_subjects(subject_csv_path='./user_data/animal/subjects.csv'):
    # -------------- Insert new "Subject" --------------
    with open(subject_csv_path, newline= '') as f:
        input_subjects = list(csv.DictReader(f, delimiter=','))
    print(f'\n---- Insert {len(input_subjects)} entry(s) into subject tables ----')
    subject.Subject.insert(input_subjects, skip_duplicates=True, ignore_extra_fields=True)
    subject.SubjectDeath.insert(input_subjects, skip_duplicates=True, ignore_extra_fields=True)
    subject.SubjectCullMethod.insert(input_subjects, skip_duplicates=True, ignore_extra_fields=True)
    ## Skipped allele info

def ingest_sessions(session_csv_path='./user_data/session/sessions.csv'):
    with open(session_csv_path, newline= '') as f:
        input_sessions = list(csv.DictReader(f, delimiter=','))

    print(f'\n---- Insert {len(input_sessions)} entry(s) into session.Session ----')
    session.Session.insert(input_sessions, skip_duplicates=True, ignore_extra_fields=True)
    session.SessionDirectory.insert(input_sessions, skip_duplicates=True, ignore_extra_fields=True)
    session.SessionNote.insert(input_sessions, skip_duplicates=True, ignore_extra_fields=True)

if __name__ == '__main__':
    ingest_lab()
    ingest_subjects()
    ingest_sessions()
