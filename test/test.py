import random
import string

from fixture.project import Project


def random_string (prefix, maxlen):
    symbols = string.digits
    return prefix + "".join([random.choice(symbols) for i in range(random.randrange(maxlen))])


def test_add_project(app):
    """Validation of add project"""
    old_projects_list = app.project.get_mantis_project_list()
    project = Project(name=random_string("test", 2), status="development", view_status="public",
                      description="description")

    app.project.add_project(project)
    old_projects_list.append(project)
    new_project_list = app.project.get_mantis_project_list()

    assert sorted(new_project_list, key=Project.if_or_max) == sorted(old_projects_list, key=Project.if_or_max)


def test_delete_some_project(app):
    """Validation of delete project"""
    old_projects_list = app.project.get_mantis_project_list()

    if len(old_projects_list) == 0:
        app.project.add_project(Project(name="test"))

    project = random.choice(old_projects_list)
    app.project.delete_project_by_id(project.id)

    old_projects_list.remove(project)
    new_project_list = app.project.get_mantis_project_list()
    assert sorted(new_project_list, key=Project.if_or_max) == sorted(old_projects_list, key=Project.if_or_max)
