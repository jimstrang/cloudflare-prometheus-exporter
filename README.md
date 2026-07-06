# Prometheus Cloudflare Exporter

Prometheus exporter powered by Cloudflare GraphQL API.

<p align="left">
<a href="https://github.com/transferwise/cloudflare-prometheus-exporter/actions"><img alt="Actions Status" src="https://github.com/transferwise/cloudflare-prometheus-exporter/workflows/Build & Test/badge.svg"></a>
<a href="https://github.com/transferwise/cloudflare-prometheus-exporter/actions"><img alt="Actions Status" src="https://github.com/transferwise/cloudflare-prometheus-exporter/workflows/CodeQL/badge.svg"></a>
</p>

## Quickstart

Examples:

    $ export CLOUDFLARE_TOKEN='YOUR_CLOUDFLARE_API_TOKEN'
    $ mkdir playground
    $ cp example.config.yaml playground/
    # fill in the zones info in playground/example.config.yaml
    $ cfexpose export playground/example.config.yaml

## Docker

This fork publishes a homelab image to GHCR:

    ghcr.io/jimstrang/cloudflare-prometheus-exporter:<tag>

The container defaults to `cfexpose export /config/config.yaml`, runs the exporter on port `9199`, and expects the Cloudflare token as the raw token value. Do not add the `Bearer` prefix; the exporter adds that header internally.

Example `compose.yaml`:

```yaml
services:
  cloudflare-exporter:
    image: ghcr.io/jimstrang/cloudflare-prometheus-exporter:latest
    restart: unless-stopped
    environment:
      CLOUDFLARE_TOKEN: ${CLOUDFLARE_TOKEN}
      CLOUDFLARE_ACCOUNT_TAG: 78dea29edd5c9bfebff5bc5ba363fbac
      EXPORTER_PORT: 9199
    volumes:
      - ./config.yaml:/config/config.yaml:ro
    ports:
      - "9199:9199"
```

Example `/config/config.yaml` for Cloudflare Free-plan HTTP analytics. Replace the zone name and `zone_id` for your own zones:

```yaml
---
api: httpRequests1hGroups
scrape_shift_seconds: 120
timerange_seconds: 3600
zones:
  couchgate.dev:
    zone_id: d79f1ed19dc9e8f036132ce118342c5b
    timerange_seconds: 3600
    scrape_shift_seconds: 120
    scrape_interval_seconds: 300
accounts: {}
```

## Example Dashboards
![Grafana 1](static/images/dashboard_1.png?raw=true "Grafana 1")
![Grafana 2](static/images/dashboard_2.png?raw=true "Grafana 2")

# Configuration options

Required environment variables:
* CLOUDFLARE_TOKEN - raw API token value, without the `Bearer` prefix
* CLOUDFLARE_ACCOUNT_TAG

Optional environment variables:
* EXPORTER_PORT - defaults to `9199` in the Docker image

Required permissions for the token:

![Analytics](static/images/APIKey.png?raw=true "Analytics: Read")

# Limits

For up-to-date information, please refer Cloudflare [documentation](https://developers.cloudflare.com/analytics/graphql-api/limits) on APL limits.

GraphQL API access restrictions by license:

    free:
      zones:
        browserPerf1mGroups
        firewallEventsAdaptive
        firewallEventsAdaptiveByTimeGroups
      accounts/zones:
        httpRequests1hGroups
        httpRequests1dGroups
    pro:
      firewallEventsAdaptiveGroups
      healthCheckEvents
      healthCheckEventsGroups
      httpRequests1mGroups
      loadBalancingRequests
      loadBalancingRequestsGroups
    business:
      -
    enterprise:
      firewallRulePreviewGroups
      httpRequests1mByColoGroups
      httpRequests1dByColoGroups
      synAvgPps1mGroups
