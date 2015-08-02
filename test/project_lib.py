from selenium.webdriver.support.ui import Select

from fixture.project import Project


class ProjectMantisHelper:

    def __init__(self, app):
        self.app = app

    def open_project_page(self):
        wd = self.app.wd
        if not(wd.current_url.endswith('manage_proj_page.php')):
            wd.find_element_by_xpath("//a[contains(@href,'/mantisbt-1.2.19/manage_overview_page.php')]").click()
            wd.find_element_by_xpath("//a[contains(@href,'/mantisbt-1.2.19/manage_proj_page.php')]").click()

    def add_project(self, project):
        wd = self.app.wd
        self.open_project_page()
        wd.find_element_by_css_selector("input[value='Create New Project']").click()

        self.add_field_value('name', project.name)
        select = Select(wd.find_element_by_name('status'))
        select.select_by_visible_text(project.status)

        select = Select(wd.find_element_by_name('view_state'))
        select.select_by_visible_text(project.view_status)
        self.add_field_value('description', project.description)
        wd.find_element_by_xpath("//input[@value='Add Project']").click()
        self.project_names = None

    project_names = None

    def get_mantis_project_list(self):
        wd = self.app.wd
        self.open_project_page()
        if self.project_names is None:
            self.project_names = []
            table = wd.find_elements_by_css_selector('.width100')[1]
            all_rows = table.find_elements_by_tag_name('tr')
            for row in all_rows[2:len(all_rows)]:
                line = row.find_elements_by_tag_name('td')

                name = None
                status =None
                enabled = None
                view_status = None
                description = None
                if line:
                    name = line[0].find_element_by_tag_name('a').text
                    status = line[1].text
                    enabled = line[2].text
                    view_status = line[3].text
                    description = line[4].text
                else:
                    assert Exception("Element was not found")

                id = None
                id_number = line[0].find_element_by_tag_name('a').get_attribute('href')
                if id_number:
                    id = id_number.split('id=')[1]
                else:
                    assert Exception("Id was not found")

                self.project_names.append(Project(name=name, status=status, id=id, enabled=enabled,
                                                  view_status=view_status, description=description))
        return list(self.project_names)

    def select_project_by_id(self, id):
        wd = self.app.wd
        wd.find_element_by_xpath("//a[contains(@href,'manage_proj_edit_page.php?project_id=%s')]" % id).click()

    def delete_project_by_id(self, id):
        wd = self.app.wd
        self.open_project_page()
        self.select_project_by_id(id)
        wd.find_element_by_xpath("//input[@value='Delete Project']").click()
        wd.find_element_by_xpath("//input[@value='Delete Project']").click()
        self.project_names = None

    def add_field_value(self, field_name, text=None):
        wd = self.app.wd
        if text is not None:
            wd.find_element_by_name(field_name).click()
            wd.find_element_by_name(field_name).clear()
            wd.find_element_by_name(field_name).send_keys(text)