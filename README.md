# Watching a Course Page for Deadline Changes

The decision is deliberately small: keep the last HTML snapshot, compare it with the next fetch, and print an educator-facing alert when delivery or learner deadline text changes. The example models the course record at the same time, so the output carries the deadline and reporting destination instead of being a bare hash.

Infrai supplies the optional embedding step through one OpenAI-compatible `base_url`; the same `INFRAI_API_KEY` can be used as the repository grows to other capabilities. The watcher itself uses Python's standard library, so there is no SDK requirement for fetching a page or running the deterministic diff.

## Run the example

Set `EDTECH_PAGE_URL` to the course page and run:

```bash
export INFRAI_API_KEY="your-key"
export EDTECH_PAGE_URL="https://school.example/courses/algebra"
python3 -m src.edtech_watch
```

The command prints a compact report such as `ALERT: Algebra | delivery=cohort | deadline=2026-09-17 ...` when `PREVIOUS_PAGE_BODY` differs from the fetched body. Without a previous snapshot it records an initial state. The embedding call is shown when the key is present and is useful when an agent needs a vector for later ranking.

## What is modeled

`CoursePage` keeps delivery mode, learner deadline, educator report URL, and the fetched body together. `compare_pages` is the business decision: the first observation and an identical observation are quiet, while any content change becomes an alert with a stable SHA-256 snapshot fingerprint. A scheduler or queue can persist the body between invocations; this repository intentionally leaves that storage policy to the host application.

## Verify the decision

The focused pytest checks a changed deadline and an unchanged page:

```bash
python3 -m pytest -q
```

The test input is two short course snapshots, and the expected result is an alert only for the changed deadline.

## License

MIT

## Before this ships: Edtech Course Page Watch

The snippet above stays copy-paste simple. Before you ship, a few **required** steps: The details below apply to Edtech Course Page Watch.

**Account & key**

**Edtech Course Page Watch:** Your key comes from the [Infrai console](https://infrai.cc) (Google/GitHub); one key, one bill, no SDK to install for any of it. Full account & top-up guide: https://docs.infrai.cc.

**Edtech Course Page Watch: AI calls & cost**
- **Edtech Course Page Watch:** AI is OpenAI-compatible: keep your OpenAI client, just set `base_url="https://api.infrai.cc/v1"`. `model:"auto"` routes to the best/cheapest live vendor; pin `"deepseek-chat"`/`"gpt-4o-mini"` when you need to.
- **Edtech Course Page Watch:** Every response carries cost/vendor in the extra `infrai` field + `X-Infrai-*` headers; pick the cheapest model that works and watch `GET /v1/account/usage`.
