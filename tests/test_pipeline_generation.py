'''Test pipeline construction
    1. Assert lab link to within-schema children
    2. Assert lab link to subject
    3. Assert subject link to session
'''

from . import pipeline


def test_generate_pipeline(pipeline):
    session = pipeline['session']
    subject = pipeline['subject']
    lab = pipeline['lab']

    # test connection Lab->schema children, and Lab->Subject.Lab
    lab_membership, loc_tbl, subject_lab_tbl = \
        lab.Lab.children(as_objects=True)
    assert lab_membership.full_table_name == lab.LabMembership.full_table_name
    assert loc_tbl.full_table_name == lab.Location.full_table_name
    assert subject_lab_tbl.full_table_name == \
        subject.Subject.Lab.full_table_name

    # test connection Subject->Session
    subject_tbl, *_ = session.Session.parents(as_objects=True)
    assert subject_tbl.full_table_name == subject.Subject.full_table_name
