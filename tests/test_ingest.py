'''Tests ingestion into schema tables: Lab, Subject, Session
    1. Assert length of populating data from __innit__
    2. Assert exact matches of inserted data fore key tables
'''

__all__ = ['dj_config', 'pipeline', 'lab_csv', 'lab_project_csv', 'lab_user_csv',
           'lab_publications_csv',  'lab_keywords_csv',  'lab_protocol_csv',
           'lab_project_users_csv',  'ingest_lab',  'subjects_csv', 'ingest_subjects',
           'sessions_csv', 'ingest_sessions']

from . import (dj_config, pipeline, lab_csv,
               lab_project_csv, lab_user_csv, lab_publications_csv,
               lab_keywords_csv, lab_protocol_csv,
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
    for this_lab in labs[1:]:
        lab_values = this_lab.split(",")
        assert (lab.Lab & {'lab': lab_values[0]}
                ).fetch1('lab_name') == lab_values[1]

    projects, _ = lab_project_csv
    for this_project in projects[1:]:
        project_values = this_project.split(",")
        assert (lab.Project & {'project': project_values[0]}
                ).fetch1('project_description') == project_values[1]

    protocols, _ = lab_protocol_csv
    for this_protocol in protocols[1:]:
        protocol_values = this_protocol.split(",")
        assert (lab.Protocol & {'protocol': protocol_values[0]}
                ).fetch1('protocol_type') == protocol_values[1]

    # Does not have example data:
    # assert len(lab.Source()) == 0


def test_ingest_subjects(pipeline, subjects_csv, ingest_subjects):
    """Check length of subject.Subject"""
    subject = pipeline['subject']
    assert len(subject.Subject()) == 2

    subjects, _ = subjects_csv
    for this_subject in subjects[1:]:
        subject_values = this_subject.split(",")
        assert (subject.Subject & {'subject': subject_values[0]}
                ).fetch1('subject_description') == subject_values[3]

    # Does not have example data:
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
