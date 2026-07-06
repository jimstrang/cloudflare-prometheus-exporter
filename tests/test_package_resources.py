# -*- coding: utf-8 -*-

"""Tests for packaged resource loading."""

import importlib
import sys


def fresh_import(module_name, monkeypatch):
    monkeypatch.delitem(sys.modules, module_name, raising=False)
    parent_name, _, child_name = module_name.rpartition(".")
    parent = sys.modules.get(parent_name)
    if parent is not None and hasattr(parent, child_name):
        monkeypatch.delattr(parent, child_name)
    return importlib.import_module(module_name)


def test_gql_queries_load_outside_repo_cwd(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    gql = fresh_import("cloudflare_exporter.gql", monkeypatch)

    assert "httpRequests1hGroups" in gql.query.zones
    assert "query httpRequests1hGroups" in gql.query.zones["httpRequests1hGroups"]


def test_cli_configures_logging_outside_repo_cwd(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    cli = fresh_import("cloudflare_exporter.cli", monkeypatch)
    cli.configure_logging()

    assert cli.LOGGER.name == "stdout"