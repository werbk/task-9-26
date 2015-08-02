
from test.project_lib import Project
from test.test import random_string
import random


def test_soap(app):
    old_projects_list = app.soap.get_project_list(username=app.config['webadmin']['username'],
                                     password=app.config['webadmin']['password'])
    project = Project(name=random_string("test", 2), status="development", view_status="public",
                      description="description")

    app.project.add_project(project)
    old_projects_list.append(project)
    new_project_list = app.project.get_mantis_project_list()
    assert sorted(new_project_list, key=Project.if_or_max) == sorted(old_projects_list, key=Project.if_or_max)

def test_delete_some_project(app):
    """Validation of delete project"""
    old_projects_list = app.soap.get_project_list(username=app.config['webadmin']['username'],
                                     password=app.config['webadmin']['password'])

    if len(old_projects_list) == 0:
        app.project.add_project(Project(name="test"))

    project = random.choice(old_projects_list)
    app.project.delete_project_by_id(project.id)

    old_projects_list.remove(project)
    new_project_list = app.soap.get_project_list(username=app.config['webadmin']['username'],
                                     password=app.config['webadmin']['password'])
    assert sorted(new_project_list, key=Project.if_or_max) == sorted(old_projects_list, key=Project.if_or_max)