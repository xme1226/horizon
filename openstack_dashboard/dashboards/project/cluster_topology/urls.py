# Copyright 2012 United States Government as represented by the
# Administrator of the National Aeronautics and Space Administration.
# All Rights Reserved.
#
# Copyright 2013 NTT MCL, Inc.
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


from django.conf.urls import patterns
from django.conf.urls import url

from openstack_dashboard.dashboards.project.cluster_topology import views


urlpatterns = patterns(
    'openstack_dashboard.dashboards.project.cluster_topology.views',
    url(r'^$', views.ClusterTopologyView.as_view(), name='index'),
    url(r'^json$', views.ClusterListJSONView.as_view(), name='cluster-json'),
    url(r'^json/(?P<job_execution_id>[^/]+)$', views.WorkflowJSONView.as_view(), name='workflow-json'),
    url(r'launch-job$', views.LaunchJobView.as_view(), name='launch-job'),
    url(r'^(?P<job_execution_id>[^/]+)$', views.ClusterTopologyView.as_view(), name='index')
)
