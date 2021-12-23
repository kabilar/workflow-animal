import workflow_session
from . import dj_config, pipeline


def test_generate_pipeline(pipeline):
    session = pipeline['session']
    subject = pipeline['subject']
    lab     = pipeline['lab']

    # test connection from lab to lab/subject
    lab_membership, loc_tbl, subjlab_tbl = lab.Lab.children(as_objects=True)
    # assert lab_tbl.full_table_name      == lab.Lab.full_table_name
    assert loc_tbl.full_table_name      == lab.Location.full_table_name
    assert subjlab_tbl.full_table_name  == subject.Subject.Lab.full_table_name

    # test connection from lab to lab/subject
    subject_tbl, *_ = session.Session.parents(as_objects=True)
    assert subject_tbl.full_table_name == subject.Subject.full_table_name