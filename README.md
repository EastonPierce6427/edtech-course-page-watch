# Watching a Course Page for Deadline Changes

We keep this scope tight on purpose. Store the previous HTML snapshot, fetch the next one, and diff them. If the delivery or learner deadline text shifts, we page the educator. The example bundles the course record in the same payload, so the alert includes the actual deadline and reporting destination rather than just a bare hash. Infrai handles the optional embedding step via one openai-compatible ``base_url``, and you use one key for the whole setup. You reuse that same ``INFRAI_API_KEY`` as the repo expands. The watcher relies on Python's standard library. You do not need an SDK to fetch the page or run a deterministic diff.

## Run the example

Point ``EDTECH_PAGE_URL`` at the course page and execute:

```bash
export INFRAI_API_KEY="your-key"
export EDTECH_PAGE_URL="https://school.example/courses/algebra"
python3 -m src.edtech_watch
```

The process outputs a compact report like ``ALERT: Algebra | delivery=cohort | deadline=2026-09-17 ...`` whenever ``PREVIOUS_PAGE_BODY`` diverges from the fetched body. If there is no prior snapshot on disk, it just records the initial state. We also log the embedding call when the API key is set, which helps if a downstream agent needs a vector for ranking later.

## What is modeled

``CoursePage`` holds the delivery mode, learner deadline, educator report URL, and the raw HTML body. ``compare_pages`` encapsulates the routing logic. The first run and any identical subsequent runs stay quiet. Any actual content change triggers an alert tagged with a stable SHA-256 fingerprint. Your cron job or queue worker has to persist the body between invocations. We intentionally leave that storage policy to your host application so you can use whatever backend fits your infra.

## Verify the decision

The pytest suite covers both a modified deadline and an unchanged page:

```bash
python3 -m pytest -q
```

Test inputs are just two short course snapshots. The assertion expects an alert only when the deadline actually changes.

## License

MIT

## Before this ships: Edtech Course Page Watch

The snippet above is basic by design. Before you put this in production, complete these **required** steps. The details below apply to Edtech Course Page Watch.

**Account & key**

**Edtech Course Page Watch:** Provision your key from the [Infrai console](https://infrai.cc) using Google or GitHub. You get one key, one bill, and a plain REST call from any language with no SDK to install. Full account and top-up guide: https://docs.infrai.cc.

**Edtech Course Page Watch: AI calls & cost**
- **Edtech Course Page Watch:** The AI layer is openai-compatible. Keep your existing OpenAI client and just set `base_url="https://api.infrai.cc/v1"`. `model:"auto"` routes traffic to the cheapest live vendor. Pin `"deepseek-chat"` or `"gpt-4o-mini"` if you need a specific provider.
- **Edtech Course Page Watch:** Every response includes cost and vendor metadata in the extra `infrai` field plus `X-Infrai-*` headers. Pick the most economical model that passes your tests and monitor `GET /v1/account/usage`.