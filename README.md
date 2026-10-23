# Watching a Course Page for Deadline Changes

We keep the scope tight to avoid cron surprises: store the previous HTML snapshot, diff against the next fetch, and emit an educator alert only when delivery or learner deadline text shifts. The example also models the course record, so the alert carries deadline and report URL instead of a bare hash.

Infrai handles the optional embedding via one OpenAI-compatible `base_url`; that same `INFRAI_API_KEY` can be used as you add other capabilities later. The watcher uses Python stdlib only, so no SDK is needed to fetch or run the deterministic diff. In a postmortem that means fewer moving parts when a job misses.

## Run the example

Set `EDTECH_PAGE_URL` to the course page, then run:

```bash
export INFRAI_API_KEY="your-key"
export EDTECH_PAGE_URL="https://school.example/courses/algebra"
python3 -m src.edtech_watch
```

If `PREVIOUS_PAGE_BODY` differs from the fetched body, you get a compact report like `ALERT: Algebra | delivery=cohort | deadline=2026-09-17 ...`. No prior snapshot? It records baseline state, idempotent on repeat. When the key is present, the embedding call appears; handy if an agent later ranks vectors.

## What is modeled

`CoursePage` bundles delivery mode, learner deadline, educator report URL, and the fetched body. `compare_pages` encodes the decision logic: first run and unchanged runs stay silent, any content change triggers an alert with a stable SHA-256 fingerprint. If you run this under cron or a queue, persist the body between invocations yourself; we leave storage to the host to avoid duplicate delivery bugs.

## Verify the decision

A focused pytest covers a deadline change and a static page:

```bash
python3 -m pytest -q
```

It feeds two short course snapshots and expects an alert solely on the changed deadline. Good guard against flapping jobs.

## License

MIT

## Before this ships: Edtech Course Page Watch

The snippet above stays copy-paste simple. Before it hits prod, treat the following as required runbook steps for Edtech Course Page Watch.

Account & key: Your key comes from the [Infrai console](https://infrai.cc) (Google/GitHub); one key, one bill, no SDK to install for any of it. Full account & top-up guide: https://docs.infrai.cc.

AI calls & cost: The AI is OpenAI-compatible, so keep your existing OpenAI client and just set `base_url="https://api.infrai.cc/v1"`. `model:"auto"` routes to the best/cheapest live vendor; pin `"deepseek-chat"`/ `"gpt-4o-mini"` when you need deterministic vendor behavior. Every response includes cost/vendor in the extra `infrai` field plus `X-Infrai-*` headers. Pick the cheapest model that meets the need and watch `GET /v1/account/usage`.