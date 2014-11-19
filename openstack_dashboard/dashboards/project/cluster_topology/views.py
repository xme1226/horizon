# Copyright 2012 United States Government as represented by the
# Administrator of the National Aeronautics and Space Administration.
# All Rights Reserved.
#
# Copyright 2013 NTT MCL Inc.
#
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

import logging
import json

from django.utils.translation import ugettext_lazy as _

from django.conf import settings
from django.core.urlresolvers import reverse
from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponse  # noqa
from django.views.generic import TemplateView  # noqa
from django.views.generic import View  # noqa

from horizon import exceptions
from horizon import tables

from openstack_dashboard import api

import openstack_dashboard.dashboards.project.data_processing.jobs.views \
	as dp_views
import openstack_dashboard.dashboards.project.cluster_topology. \
    workflows.launch as launch_flow

LOG = logging.getLogger(__name__)


class ClusterTopologyView(TemplateView):
    template_name = 'project/cluster_topology/topology.html'

    def get_jobs(self):
	jobs = []
	try:
	    jobs = api.sahara.job_list(self.request)
	except Exception:
	    exceptions.handle(self.request, _("Unable to fetch jobs."))

	return jobs

    def get_context_data(self, **kwargs):
	context = super(ClusterTopologyView, self).get_context_data(**kwargs)
	context["jobs"] = self.get_jobs()
	context["job_execution_id"] = kwargs.get("job_execution_id", None) 

	return context


class ClusterListJSONView(View):
    def _get_clusters(self, request):
        # Get cluster list
        clusters = {}
        try:
	    console_type = getattr(settings, "CONSOLE_TYPE", "AUTO")
	    if console_type == "SPICE":
		console = "spice"
	    else:
		console = "vnc"

            clusters = api.sahara.cluster_list(self.request)
        except Exception:
            exceptions.handle(self.request,
                              _("Unable to fetch cluster list."))
	for cluster in clusters:
	    cluster.url = reverse("horizon:project:data_processing.clusters:details", None, [cluster.id])
	    for node_group in cluster.node_groups:
		node_group["url"] = reverse("horizon:project:data_processing.nodegroup_templates:details", None, [node_group["node_group_template_id"]])
		for instance in node_group["instances"]:
		    instance["url"] = reverse("horizon:project:instances:detail", None, [instance["instance_id"]])
		    instance["console"] = console

	return clusters;

    def get(self, request, *args, **kwargs):
        data = { "clusters": [{"name": cluster.name,
			       "node_groups": cluster.node_groups,
			       "id": cluster.id,
			       "url": cluster.url,
			       "status": cluster.status}
			      for cluster in self._get_clusters(request)] }
        json_string = json.dumps(data, ensure_ascii=False)
        return HttpResponse(json_string, content_type='text/json')

class WorkflowJSONView(View):
    def _get_model(self, request):
        # Get workflow data
        model = {}
        try:
            job_execution_id = self.kwargs["job_execution_id"]
            job_execution = api.sahara.job_execution_get(request,
                                                       job_execution_id)

            model = job_execution.info
        except Exception:
            exceptions.handle(self.request, _("Unable to fetch job execution."))
        return model

    def get(self, request, *args, **kwargs):
        data = { "model": self._get_model(request) }
        json_string = json.dumps(data, ensure_ascii=False)
        return HttpResponse(json_string, content_type='text/json')

class LaunchJobView(dp_views.LaunchJobView):
    workflow_class = launch_flow.LaunchJob
    success_url = "horizon:project:cluster_topology"
