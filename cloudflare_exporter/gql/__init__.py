# -*- coding: utf-8 -*-

"""Top-level package for Prometheus Cloudflare Exporter."""

from importlib import resources

__author__ = """Observability :: TransfewrWise"""
__email__ = "observability@transferwise.com"
__version__ = "0.1.12"


class CloudflareGQLQuery:
    def __init__(self):
        self.accounts = {
            "httpRequests1hGroups": read_gql_query(
                "accounts.httpRequests1hGroups.graphql"
            ),
        }
        self.zones = {
            "httpRequests1hGroups": read_gql_query(
                "zones.httpRequests1hGroups.graphql"
            ),
            "httpRequests1mGroups": read_gql_query(
                "zones.httpRequests1mGroups.graphql"
            ),
        }


def read_gql_query(query_file):
    query = resources.files(__package__).joinpath(query_file).read_text(encoding="utf-8")
    return "".join(line.rstrip().lstrip() for line in query.splitlines())


query = CloudflareGQLQuery()
