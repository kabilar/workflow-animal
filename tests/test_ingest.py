import sys
import pathlib

from . import (dj_config, pipeline, test_data,
               subjects_csv, ingest_subjects,
               sessions_csv, ingest_sessions,
               testdata_paths)


def test_ingest_subjects(pipeline, ingest_subjects):
    """Check length of subject.Subject"""
    subject = pipeline['subject']
    assert len(subject.Subject()) == 6


def test_ingest_sessions(pipeline, sessions_csv, ingest_sessions):
    ephys = pipeline['ephys']
    probe = pipeline['probe']
    session = pipeline['session']
    get_ephys_root_data_dir = pipeline['get_ephys_root_data_dir']

    assert len(session.Session()) == 7

    sessions, _ = sessions_csv
    sess = sessions.iloc[0]

    assert (session.SessionDirectory
            & {'subject': sess.name}).fetch1('session_dir') == sess.session_dir

def test_ingest_lab():
    pass