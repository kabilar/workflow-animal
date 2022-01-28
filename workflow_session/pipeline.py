import datajoint as dj

from element_lab import lab
from element_animal import subject, genotyping
from element_session import session

from element_animal.subject import Subject
# from element_animal.genotyping import Sequence, BreedingPair, Cage,\
#                                       SubjectCaging, GenotypeTest
from element_lab.lab import Source, Lab, Protocol, User, Project, ProjectKeywords,\
                            ProjectPublication, ProjectSourceCode, ProjectUser
from element_session.session import Session

if 'custom' not in dj.config:
    dj.config['custom'] = {}

db_prefix = dj.config['custom'].get('database.prefix', '')

__all__ = ['genotyping', 'session', 'Subject', 'Source', 'Lab', 'Protocol', 'User',
           'Project', 'ProjectKeywords', 'ProjectPublication', 'ProjectSourceCode',
           'ProjectUser', 'Session']

# Activate "lab", "subject", "session" schema -------------

lab.activate(db_prefix + 'lab')

subject.activate(db_prefix + 'subject', linking_module=__name__)

Experimenter = lab.User
session.activate(db_prefix + 'session', linking_module=__name__)

# genotyping.activate(db_prefix + 'genotyping', linking_module=__name__)
