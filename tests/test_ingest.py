import sys
import pathlib

import workflow_session
from . import (dj_config, pipeline, lab_csv,
               lab_project_csv, lab_user_csv, lab_publications_csv,
               lab_keywords_csv, lab_protocol_csv, lab_user_csv,
               lab_project_users_csv, ingest_lab,
               subjects_csv, ingest_subjects,
               sessions_csv, ingest_sessions)


def test_ingest_lab(pipeline, ingest_lab,
                    lab_csv, lab_project_csv, lab_protocol_csv):
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

    labs, _ = lab_csv
    for l in labs[1:]:
        l = l.split(",")
        assert (lab.Lab & {'lab':l[0]}).fetch1('lab_name')==l[1]

    projects, _ = lab_project_csv
    for p in projects[1:]:
        p = p.split(",")
        assert (lab.Project & {'project':p[0]}
                ).fetch1('project_description')==p[1]

    protocols, _ = lab_protocol_csv
    for p in protocols[1:]:
        p = p.split(",")
        assert (lab.Protocol & {'protocol':p[0]}
                ).fetch1('protocol_type')==p[1]

    ## Does not have example data:
    # assert len(lab.Source()) == 0

def test_ingest_subjects(pipeline, subjects_csv, ingest_subjects):
    """Check length of subject.Subject"""
    subject = pipeline['subject']
    assert len(subject.Subject()) == 2

    subjects, _ = subjects_csv
    for s in subjects[1:]:
        s = s.split(",")
        assert (subject.Subject & {'subject':s[0]}
                ).fetch1('subject_description')==s[3]

    ## Does not have example data:
    # assert len(genotyping.Sequence()) == 0

def test_ingest_sessions(pipeline, sessions_csv, ingest_sessions):
    """Check length/contents of Session.SessionDirectory"""
    session = pipeline['session']
    assert len(session.Session()) == 2

    sessions, _ = sessions_csv
    for sess in sessions[1:]:
        sess = sess.split(",")
        assert (session.SessionDirectory
                & {'subject': sess[0]}
                ).fetch1('session_dir') == sess[2]