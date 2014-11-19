# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from django.core.urlresolvers import reverse

from openstack_dashboard.api import sahara as saharaclient
import openstack_dashboard.dashboards.project.data_processing.jobs. \
    workflows.launch as launch_flow

class LaunchJob(launch_flow.LaunchJob):
	#success_url = "horizon:project:cluster_topology:index"
	def handle(self, request, context):
            job_execution = saharaclient.job_execution_create(
            request,
            context["job_general_job"],
            context["job_general_cluster"],
            context["job_general_job_input"],
            context["job_general_job_output"],
            context["job_config"])

	    self.success_url = reverse("horizon:project:cluster_topology:index", None, [job_execution.id])

            return True
