# Copyright 2016 NEC Corporation.  All rights reserved.
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

from tempest.lib.services.image.v2 import namespaces_client
from tempest.tests.lib import fake_auth_provider
from tempest.tests.lib.services import base


class TestNamespacesClient(base.BaseServiceTest):
    FAKE_CREATE_SHOW_NAMESPACE = {
        "namespace": "OS::Compute::Hypervisor",
        "visibility": "public",
        "description": "Tempest",
        "display_name": u"\u2740(*\xb4\u25e1`*)\u2740",
        "protected": True
    }

    FAKE_LIST_NAMESPACES = {
        "first": "/v2/metadefs/namespaces?sort_key=created_at&sort_dir=asc",
        "namespaces": [
            {
                "created_at": "2014-08-28T17:13:06Z",
                "description": "OS::Compute::Libvirt",
                "display_name": "libvirt Driver Options",
                "namespace": "OS::Compute::Libvirt",
                "owner": "admin",
                "protected": True,
                "resource_type_associations": [
                    {
                        "created_at": "2014-08-28T17:13:06Z",
                        "name": "OS::Glance::Image",
                        "updated_at": "2014-08-28T17:13:06Z"
                    }
                ],
                "schema": "/v2/schemas/metadefs/namespace",
                "self": "/v2/metadefs/namespaces/OS::Compute::Libvirt",
                "updated_at": "2014-08-28T17:13:06Z",
                "visibility": "public"
            },
            {
                "created_at": "2014-08-28T17:13:06Z",
                "description": "OS::Compute::Quota",
                "display_name": "Flavor Quota",
                "namespace": "OS::Compute::Quota",
                "owner": "admin",
                "protected": True,
                "resource_type_associations": [
                    {
                        "created_at": "2014-08-28T17:13:06Z",
                        "name": "OS::Nova::Flavor",
                        "updated_at": "2014-08-28T17:13:06Z"
                    }
                ],
                "schema": "/v2/schemas/metadefs/namespace",
                "self": "/v2/metadefs/namespaces/OS::Compute::Quota",
                "updated_at": "2014-08-28T17:13:06Z",
                "visibility": "public"
            }
        ],
        "schema": "/v2/schemas/metadefs/namespaces"
    }

    FAKE_UPDATE_NAMESPACE = {
        "namespace": "OS::Compute::Hypervisor",
        "visibility": "public",
        "description": "Tempest",
        "display_name": u"\u2740(*\xb4\u25e2`*)\u2740",
        "protected": True
    }

    def setUp(self):
        super(TestNamespacesClient, self).setUp()
        fake_auth = fake_auth_provider.FakeAuthProvider()
        self.client = namespaces_client.NamespacesClient(fake_auth,
                                                         'image', 'regionOne')

    def _test_show_namespace(self, bytes_body=False):
        self.check_service_client_function(
            self.client.show_namespace,
            'tempest.lib.common.rest_client.RestClient.get',
            self.FAKE_CREATE_SHOW_NAMESPACE,
            bytes_body,
            namespace="OS::Compute::Hypervisor")

    def _test_list_namespaces(self, bytes_body=False):
        self.check_service_client_function(
            self.client.list_namespaces,
            'tempest.lib.common.rest_client.RestClient.get',
            self.FAKE_LIST_NAMESPACES,
            bytes_body)

    def _test_create_namespace(self, bytes_body=False):
        self.check_service_client_function(
            self.client.create_namespace,
            'tempest.lib.common.rest_client.RestClient.post',
            self.FAKE_CREATE_SHOW_NAMESPACE,
            bytes_body,
            namespace="OS::Compute::Hypervisor",
            visibility="public", description="Tempest",
            display_name=u"\u2740(*\xb4\u25e1`*)\u2740", protected=True,
            status=201)

    def _test_update_namespace(self, bytes_body=False):
        self.check_service_client_function(
            self.client.update_namespace,
            'tempest.lib.common.rest_client.RestClient.put',
            self.FAKE_UPDATE_NAMESPACE,
            bytes_body,
            namespace="OS::Compute::Hypervisor",
            display_name=u"\u2740(*\xb4\u25e2`*)\u2740", protected=True)

    def test_show_namespace_with_str_body(self):
        self._test_show_namespace()

    def test_show_namespace_with_bytes_body(self):
        self._test_show_namespace(bytes_body=True)

    def test_list_namespaces_with_str_body(self):
        self._test_list_namespaces()

    def test_list_namespaces_with_bytes_body(self):
        self._test_list_namespaces(bytes_body=True)

    def test_create_namespace_with_str_body(self):
        self._test_create_namespace()

    def test_create_namespace_with_bytes_body(self):
        self._test_create_namespace(bytes_body=True)

    def test_delete_namespace(self):
        self.check_service_client_function(
            self.client.delete_namespace,
            'tempest.lib.common.rest_client.RestClient.delete',
            {}, namespace="OS::Compute::Hypervisor", status=204)

    def test_update_namespace_with_str_body(self):
        self._test_update_namespace()

    def test_update_namespace_with_bytes_body(self):
        self._test_update_namespace(bytes_body=True)
