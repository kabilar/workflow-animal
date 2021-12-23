import sys
import pathlib

import workflow_session
from . import (dj_config, pipeline,
               lab_csv, lab_proj_csv, lab_projusers_csv,
               lab_pubs_csv, lab_keyw_csv, lab_prot_csv,
               lab_user_csv, ingest_lab,
               subjects_csv, ingest_subjects,
               sessions_csv, ingest_sessions)


def test_ingest_lab(pipeline,ingest_lab):
    """Check length of various lab schema tables"""
    lab = pipeline['lab']
    assert len(lab.Lab()) == 2
    assert len(lab.LabMembership()) == 3
    assert len(lab.User()) == 3
    assert len(lab.UserRole()) == 2
    assert len(lab.Location()) == 2
    assert len(lab.Project()) == 2
    assert len(lab.ProjectUser()) == 4
    assert len(lab.Protocol()) == 2
    assert len(lab.ProtocolType()) == 2

    ## Does not have example data:
    # assert len(lab.Source()) == 0

def test_ingest_subjects(pipeline, ingest_subjects):
    """Check length of subject.Subject"""
    subject = pipeline['subject']
    assert len(subject.Subject()) == 2

    ## Does not have example data:
    # assert len(genotyping.Sequence()) == 0

def test_ingest_sessions(pipeline, sessions_csv, ingest_sessions):
    """Check length/contents of Session.SessionDirectory"""
    session = pipeline['session']

    assert len(session.Session()) == 2

    sessions, _ = sessions_csv
    sess = sessions.iloc[0]

    assert (session.SessionDirectory
            & {'subject': sess.name}).fetch1('session_dir') == sess.session_dir