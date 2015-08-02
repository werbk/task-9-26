from suds.client import Client
from suds import WebFault
from test.project_lib import Project


class SoapHelper:

    def __init__(self, app):
        self.app = app

    def can_login(self, username, password):
        client = Client("http://localhost/mantisbt-1.2.19/api/soap/mantisconnect.php?wsdl")
        try:
            client.service.mc_login(username, password)
            return True
        except WebFault:
            return False

    def get_project_list(self, username, password):
        client = Client("http://localhost/mantisbt-1.2.19/api/soap/mantisconnect.php?wsdl")
        self.project_list = []

        try:
            for project in client.service.mc_projects_get_user_accessible(username, password):

                self.project_list.append((Project(id=str(project.id), name=str(project.name),
                                                  status=str(project.status.name),
                                                  view_status=str(project.view_state.name),
                                                  description=str(project.description),
                                                  enabled=self.convert_enabled_status(project.enabled))))

            return list(self.project_list)
        except WebFault:
            return False

    def convert_enabled_status(self, enabled):
        status = None
        if enabled is True:
            status = "X"
        if enabled is False:
            status = ""
        return status
