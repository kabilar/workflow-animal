import pathlib
import csv
import re

from workflow_session.pipeline import lab, subject, session

from workflow_session.paths import get_root_data_dir
import element_data_loader.utils

def ingest_general(csvs, tables,               # take list of csvs/dj tables
                   skip_duplicates=True):
    """
    Inserts data from a series of csvs into their corresponding table:
        e.g., ingest_general(['./lab_data.csv', './proj_data.csv'],
                                 [lab.Lab(),lab.Project()]
    ingest_general(csvs, tables, skip_duplicates=True, ignore_extra_fields=True)
        :param csvs: list of relative paths to CSV files
        :param tables: list of datajoint tables with ()
    """
    for insert, table in zip(csvs, tables):    # loop through lists
        with open(insert, newline='') as f:    # read csvs
            data = list(csv.DictReader(f, delimiter=','))
        prev_len = len(table)                  # measure prev length
        table.insert(data, skip_duplicates=skip_duplicates, # insert
              ignore_extra_fields=True)        # must be true for csvs w/mult tables
        insert_len = len(table) - prev_len     # report length change
        print(f'\n---- Inserting {insert_len} entry(s) into {table.table_name} ----')

    # TODO: permit embedded lists

def ingest_lab(lab_csv_path='./user_data/lab/labs.csv',
                project_csv_path='./user_data/lab/projects.csv',
                pubs_csv_path='./user_data/lab/publications.csv',
                keyw_csv_path='./user_data/lab/keywords.csv',
                protocol_csv_path='./user_data/lab/protocols.csv',
                skip_duplicates=True):
    """
    Inserts data from a series of csvs into their corresponding lab schema tables.
    By default, uses data from workflow_session/user_data/lab/
    :param lab_csv_path:      relative path of lab csv
    :param project_csv_path:  relative path of project csv
    :param pubs_csv_path:     relative path of publication csv
    :param keyw_csv_path:     relative path of keyword csv
    :param protocol_csv_path: relative path of protocol csv
    :param skip_duplicates=True: datajoint insert function param
    """

    # List with repeats for when mult dj.tables fed by same CSV
    csvs = [lab_csv_path, lab_csv_path,
            project_csv_path, pubs_csv_path, keyw_csv_path,
            protocol_csv_path, protocol_csv_path]
    tables=[lab.Lab(), lab.Location(),
            lab.Project(), lab.Project.Publication(), lab.Project.Keywords(),
            lab.Protocol(), lab.ProtocolType()]

    ingest_general(csvs, tables, skip_duplicates=skip_duplicates)

def ingest_subjects(subject_csv_path='./user_data/animal/subjects.csv',
                    skip_duplicates=True):
    """
    Inserts data from a subject csv into corresponding subject schema tables
    By default, uses data from workflow_session/user_data/animal/
    :param subject_csv_path:     relative path of subject csv
    :param skip_duplicates=True: datajoint insert function param
    """
    csvs = [subject_csv_path, subject_csv_path, subject_csv_path]
    tables=[subject.Subject(),subject.SubjectDeath(),
            subject.SubjectCullMethod()]

    ingest_general(csvs, tables, skip_duplicates=skip_duplicates)

    # TODO: add allele and genotyping data

def ingest_sessions(session_csv_path='./user_data/session/sessions.csv',
                    skip_duplicates=True):
    """
    Inserts data from a sessions csv into corresponding session schema tables
    By default, uses data from workflow_session/user_data/session/
    :param session_csv_path:     relative path of subject csv
    :param skip_duplicates=True: datajoint insert function param
    """
    csvs = [session_csv_path,session_csv_path,session_csv_path]
    tables=[session.Session(),session.SessionDirectory(),session.SessionNote()]

    ingest_general(csvs, tables, skip_duplicates=skip_duplicates)

if __name__ == '__main__':
    ingest_lab()
    ingest_subjects()
    ingest_sessions()
