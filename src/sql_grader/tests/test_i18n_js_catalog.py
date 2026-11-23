"""
Tests for loading the block's namespaced JavaScript translation catalog
"""

import unittest
from unittest.mock import Mock

from xblock.field_data import DictFieldData

from sql_grader.xblocks import SqlGrader


class I18nJsCatalogTest(unittest.TestCase):
    """
    Tests for loading the block's namespaced JavaScript translation catalog
    """

    def _js_urls(self, i18n_service):
        """
        Build a fragment with the block's JS and return its JavaScript URLs in order
        """
        runtime = Mock(
            service=Mock(return_value=i18n_service),
            local_resource_url=Mock(side_effect=lambda _block, path: f"/resource/{path}"),
        )
        block = SqlGrader(runtime, DictFieldData({}), Mock())
        fragment = block.build_fragment(js_files=["view.js"])
        return [r.data for r in fragment.resources if r.mimetype == "application/javascript"]

    def test_namespace(self):
        assert SqlGrader.get_i18n_js_namespace() == "XBlockSqlGraderI18N"

    def test_catalog_loads_before_block_js(self):
        i18n_service = Mock()
        i18n_service.get_javascript_i18n_catalog_url.return_value = "/static/catalog.js"

        assert self._js_urls(i18n_service) == ["/static/catalog.js", "/resource/static/view.js"]

    def test_no_catalog_without_url(self):
        """
        No catalog is added when there is none or the i18n service can't provide one
        """
        no_catalog = Mock()
        no_catalog.get_javascript_i18n_catalog_url.return_value = None
        for i18n_service in (no_catalog, Mock(spec=[])):
            with self.subTest(i18n_service=i18n_service):
                assert self._js_urls(i18n_service) == ["/resource/static/view.js"]
