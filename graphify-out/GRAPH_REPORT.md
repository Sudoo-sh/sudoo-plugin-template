# Graph Report - sudoo-plugin-template  (2026-11-14)

## Corpus Check
- cluster-only mode — file stats not available

## Summary
- 204 nodes · 239 edges · 15 communities (9 shown, 6 thin omitted)
- Extraction: 97% EXTRACTED · 3% INFERRED · 0% AMBIGUOUS · INFERRED: 8 edges (avg confidence: 0.94)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- with
- plugin/manifest.json
- notification-channel/manifest.json
- google-updates.json
- steps
- test_theme.py
- test_plugin.py
- WebhookAlerts
- example_webhook_alerts/plugin.py
- ci.yml
- release.yml
- sudoo-plugin-midnight-theme
- sudoo-plugin-webhook-alerts

## God Nodes (most connected - your core abstractions)
1. `WebhookAlerts` - 12 edges
2. `channel()` - 10 edges
3. `Recorder` - 9 edges
4. `Midnight` - 8 edges
5. `with` - 8 edges
6. `test_bad_settings_are_refused_at_start()` - 7 edges
7. `plugin` - 7 edges
8. `steps` - 7 edges
9. `test_a_refusal_is_explained()` - 6 edges
10. `steps` - 6 edges

## Surprising Connections (you probably didn't know these)
- `test_dark_is_its_own_palette()` --uses--> `Midnight`  [INFERRED]
  plugin/tests/test_theme.py → plugin/src/example_midnight_theme/plugin.py
- `test_every_theme_check_passes()` --uses--> `Midnight`  [INFERRED]
  plugin/tests/test_theme.py → plugin/src/example_midnight_theme/plugin.py
- `test_only_panel_tokens_are_set()` --uses--> `Midnight`  [INFERRED]
  plugin/tests/test_theme.py → plugin/src/example_midnight_theme/plugin.py
- `test_text_reads_well_in_both_modes()` --uses--> `Midnight`  [INFERRED]
  plugin/tests/test_theme.py → plugin/src/example_midnight_theme/plugin.py
- `channel()` --uses--> `WebhookAlerts`  [INFERRED]
  examples/notification-channel/tests/test_plugin.py → examples/notification-channel/src/example_webhook_alerts/plugin.py

## Import Cycles
- None detected.

## Communities (15 total, 6 thin omitted)

### Community 0 - "with"
Cohesion: 0.08
Nodes (25): run, SUDOO_SDK_TOKEN, plugin, path, defaults, env, runs-on, steps (+17 more)

### Community 1 - "plugin/manifest.json"
Cohesion: 0.09
Nodes (22): author, name, url, description, entry_points, sudoo.themes, icon, id (+14 more)

### Community 2 - "notification-channel/manifest.json"
Cohesion: 0.09
Nodes (21): author, name, url, description, entry_points, sudoo.notifications, id, license (+13 more)

### Community 3 - "google-updates.json"
Cohesion: 0.10
Nodes (20): last_verified, policy, $schema, _schema_doc, unverified[], updates[], secondary_sources, source_of_truth (+12 more)

### Community 4 - "steps"
Cohesion: 0.11
Nodes (19): run, GH_TOKEN, SUDOO_DEVELOPER_TOKEN, SUDOO_SDK_TOKEN, release, defaults, env, runs-on (+11 more)

### Community 5 - "test_theme.py"
Cohesion: 0.14
Nodes (7): Midnight, test_a_theme_asks_for_nothing(), test_dark_is_its_own_palette(), test_every_theme_check_passes(), test_logo_is_safe_and_is_the_icon(), test_only_panel_tokens_are_set(), test_text_reads_well_in_both_modes()

### Community 6 - "test_plugin.py"
Cohesion: 0.27
Nodes (8): channel(), Recorder, test_a_refusal_is_explained(), test_asks_only_for_outbound_network(), test_bad_settings_are_refused_at_start(), test_below_the_minimum_severity_nothing_is_sent(), test_discord_format(), test_sends_a_slack_message()

### Community 9 - "ci.yml"
Cohesion: 0.17
Nodes (11): concurrency, cancel-in-progress, group, jobs, name, on, pull_request, push (+3 more)

### Community 10 - "release.yml"
Cohesion: 0.18
Nodes (10): concurrency, cancel-in-progress, group, jobs, name, on, push, permissions (+2 more)

## Knowledge Gaps
- **2 isolated node(s):** `sudoo-plugin-midnight-theme`, `sudoo-plugin-webhook-alerts`
  These have ≤1 connection - possible missing edges. (Counts symbols only; 126 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **6 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `WebhookAlerts` connect `WebhookAlerts` to `example_webhook_alerts/plugin.py`, `test_plugin.py`?**
  _High betweenness centrality (0.032) - this node is a cross-community bridge._
- **Are the 2 inferred relationships involving `WebhookAlerts` (e.g. with `channel()` and `test_it_is_a_notification_channel()`) actually correct?**
  _`WebhookAlerts` has 2 INFERRED edges - model-reasoned connections that need verification._
- **What connects `sudoo-plugin-midnight-theme`, `sudoo-plugin-webhook-alerts` to the rest of the system?**
  _2 weakly-connected nodes found - possible missing edges._
- **Should `with` be split into smaller, more focused modules?**
  _Cohesion score 0.08 - nodes in this community are weakly interconnected._
- **Why does `plugin` connect `with` to `ci.yml`?**
  _High betweenness centrality (0.023) - this node is a cross-community bridge._
- **Are the 5 inferred relationships involving `Midnight` (e.g. with `test_dark_is_its_own_palette()` and `test_every_theme_check_passes()`) actually correct?**
  _`Midnight` has 5 INFERRED edges - model-reasoned connections that need verification._
- **Should `plugin/manifest.json` be split into smaller, more focused modules?**
  _Cohesion score 0.08695652173913043 - nodes in this community are weakly interconnected._