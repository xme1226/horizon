#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

from openstack_dashboard.test.integration_tests import basewebobject


class PageObject(basewebobject.BaseWebObject):
    """Base class for page objects."""
    def __init__(self, driver, conf):
        """Constructor."""
        super(PageObject, self).__init__(driver, conf)
        self.login_url = self.conf.dashboard.login_url
        self._page_title = None

    @property
    def page_title(self):
        return self.driver.title

    def is_the_current_page(self):
        if self._page_title not in self.page_title:
            raise AssertionError(
                "Expected to find %s in page title, instead found: %s"
                % (self._page_title, self.page_title))
        return True

    def get_url_current_page(self):
        return self.driver.current_url()

    def close_window(self):
        return self.driver.close()

    def return_to_previous_page(self):
        self.driver.back()

    def go_to_login_page(self):
        self.driver.get(self.login_url)
        self.is_the_current_page()
