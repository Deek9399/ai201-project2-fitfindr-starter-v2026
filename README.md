# FitFindr

> ### 👋 Start here**

>

> ****New to this repo? Read [RUNNING.md](**RUNNING.md**) first**** — setup, every

> command, and what to do when something breaks.

>

> Once `python test.py` passes:

>

> ```bash

> python app.py listings --full -n 6      # read the data (Milestone 1)

> python app.py fields                    # what you can filter on

> python app.py ask 'vintage graphic tee under $30'

> ```

>

> All three tools are stubs, so that last command will do nothing useful yet.

> That's the starting position.

>

> ****The rest of this file is your submission.**** Fill it in as you go.

---

<!-- ─────────────────────────────────────────────────────────────────────────

     HOW TO USE THIS FILE

     This is your submission. Fill each section in as you finish the milestone

     it belongs to — don't leave it all to the end.

     Unit 3 asks for the first five sections. Unit 4 adds the five below them.

     Leave the unit 4 sections alone until then; they're here so you know

     what's coming.

     Everything is pasted as TEXT. No screenshots, no images, no video links.

     A typed block of output gets full credit; a picture of the same output

     gets none.

     ───────────────────────────────────────────────────────────────────────── -->

<!-- ═══════════════════════ UNIT 3 — THE BUILD ═══════════════════════ -->

## What This Does

<!-- Three or four sentences: what a user asks for, and what they get back. -->

FitFindr is a thrift-fashion assistant that helps a user find secondhand clothing within a budget and optional size constraint. It searches local listing data, selects a matching item, generates two outfit ideas using the user's wardrobe when available, and creates a social-media-ready fit card. The agent follows a planning loop and calls its listing search through MCP. If no listings match, it stops before generating outfits or a card.

---

## Tool Inventory

<!-- Four lines per tool. This is worth 2 points and it's the single most

     common place students lose them.

     "Returns a list" earns NOTHING. The description has to say what is IN

     the list.

     The empty case isn't optional either — it's the thing your loop branches

     on, and if you don't decide it here you'll discover it as a crash in

     Milestone 5. -->

### `search_listings`

- **What it does:** Searches thrift listings with weighted keyword relevance and optional price/size filters, returning the best matches first. The search is exposed through MCP.
- **Inputs:** `description: str`, `size: str | None = None`, `max_price: float | None = None`.
- **Returns:** `list[dict]` of at most `config.SEARCH_RESULT_LIMIT` listing records, each with `id`, `title`, `description`, `category`, `style_tags`, `size`, `condition`, `price`, `colors`, `brand`, and `platform`. Exact phrase/title matches have higher ranking weight.
- **When it has nothing:** Returns `[]`, not `None`; the planning loop stops without calling the other tools. Size matching uses extracted size tokens rather than naive substring matching.

### `suggest_outfit`

- **What it does:** Uses a model to propose two ways to style the selected thrift item, drawing from the supplied wardrobe when available.
- **Inputs:** `new_item: dict`, `wardrobe: dict`.
- **Returns:** `str` containing two outfit suggestions.
- **When it has nothing:** An empty wardrobe is allowed; it proposes generic styling combinations rather than claiming the user owns specific pieces. If search returns no item, the agent does not call this tool.

### `create_fit_card`

- **What it does:** Uses a model to write a short, social-ready caption for the selected thrift item and outfit.
- **Inputs:** `outfit: str`, `new_item: dict`.
- **Returns:** `str` containing the fit-card caption, including listing price and platform in the observed runs.
- **When it has nothing:** The agent skips this tool when there is no matching listing or no generated outfit; model failures are handled by the agent's error path.

---

## Planning Loop

<!-- Your branch rule, stated as a rule — the condition AND both paths — plus

     the file and function that holds it.

     Like this:

       "If search_listings returns an empty list, put a message in the session

        and stop. Otherwise take the first result and go to suggest_outfit."

        — agent.py::run_agent

     The grader checks your code against what you claim here, so the file and

     function have to be real. -->

**Branch rule:**

****Where it lives:**** `agent.py::run_agent`

****How the query is parsed:**** <!-- regex, string splitting, or asking the model — say which -->

****What moves through the session:**** <!-- which fields, in what order -->

**Branch rule:** If `search_listings()` returns `[]`, the agent records an actionable no-match message and stops without calling `suggest_outfit()` or `create_fit_card()`. Otherwise it selects the first ranked listing, generates outfit suggestions, and creates the fit card.

**Where it lives:** `agent.py::run_agent`

**How the query is parsed:** Regex-based extraction separates the requested clothing description from size and maximum price before search.

**What moves through the session:** Parsed `description`, `size`, and `max_price` lead to `search_results`, then `selected_item`, then the generated `outfit` text and `fit_card`; trace steps record the tool sequence.

---

## Sample Run

<!-- Two things go here.

     1. One FULL query and its output, pasted as text.

     2. Your three per-tool terminal tests — the command and what it printed. -->

**One full query**

```

$ python app.py ask '...'

```

**The three tools, tested one at a time**

```

$ python -c "from tools import search_listings; print(search_listings('graphic tee', max_price=30))"

```

```

$ python -c "from tools import suggest_outfit; ..."

```

```

$ python -c "from tools import create_fit_card; ..."

```

---

## How I Used AI

<!-- Two specific moments. What you asked, what came back, what you changed.

     "I used Claude to help me code" is not enough.

     "I gave Claude my search_listings spec. It returned None on no match

     instead of an empty list, so I changed it" is the level we want. -->

**Moment 1**

- **What I asked for:** Help reviewing the five evaluation scenarios and identifying what the traces could actually prove.
- **What came back:** Suggested acceptance checks for successful tool sequencing, empty-search branching, state consistency, fit-card accuracy, and empty-wardrobe handling.
- **What I changed:** I ran each of the five scenarios five times and compared their recorded behavior against the criteria. I treated abbreviated model outputs as incomplete evidence rather than assuming they prove every content-level requirement.

**Moment 2**

- **What I asked for:** Help diagnosing why a search for `vintage graphic tee under $30` selected a less directly relevant baby tee.
- **What came back:** A suggestion to weight title, category, and style-tag matches more heavily than incidental description and color matches.
- **What I changed:** I updated `tools.py::search_listings` with weighted keyword scoring and reran the same five evaluation scenarios. The selected top item changed from a Y2K Baby Tee to a directly matching Graphic Tee.

<!-- Review these first-person statements and edit them to reflect your own actual AI-use process. -->

<!-- ═══════════════════════ UNIT 4 — THE TEST ═══════════════════════

     Don't fill these in during unit 3.

     ═══════════════════════════════════════════════════════════════════ -->

---

## Run Log — Before

<!-- Five criteria, five tries each, in this exact format.

     Five, because your criteria are written out of five. Mark each try PASS

     or FAIL, count the passes, and read that count against your target — a

     row targeting 4 of 5 with three PASS cells is MISSED (3/5).

     `python run_eval.py --label before` runs everything and writes the table

     into results/. Paste it here and fill in the verdicts. -->

| Criterion | Target | Try 1 | Try 2 | Try 3 | Try 4 | Try 5 | Verdict |
|---|---|---|---|---|---|---|---|
| 1. Matching query completes all three tools | 4/5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 2. Impossible query stops early | 5/5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 3. Selected item consistent across tools | 5/5 | CHECK | CHECK | CHECK | CHECK | CHECK | Not fully verified |
| 4. Fit card price/platform accurate | 4/5 | CHECK | CHECK | CHECK | CHECK | CHECK | Not fully verified |
| 5. Empty wardrobe: two outfits, no invented ownership | 4/5 | CHECK | CHECK | CHECK | CHECK | CHECK | Not fully verified |

****Real output from one try****, pasted as text, naming the file and function

that produced it:

```

```

---

## Verdicts and Diagnoses

<!-- MET or MISSED per criterion against LAST UNIT's target, plus a sentence on

     how you decided.

     Then, for every miss: which of the four places it happened — a tool, the

     loop's branch, the session, or the model's output — AND the mechanism.

     Not a diagnosis:  "The fit card was bad."

     A diagnosis:      "The fit card criterion missed on 2 of 5 items. Both had

                        an empty brand field. My prompt puts the brand in the

                        first sentence, so the card opened with a blank and read

                        like a fragment. The tool worked; the prompt assumed a

                        field that isn't always there."

     Look for a pattern. Three misses on the same tool is one problem, not

     three. -->

| # | Criterion | Target | Verdict | How I decided |

|---|---|---|---|---|

| 1 |  |  |  |  |

| 2 |  |  |  |  |

| 3 |  |  |  |  |

| 4 |  |  |  |  |

| 5 |  |  |  |  |

**Diagnoses**

The baseline runs exposed a search-ranking quality issue even though the two fully observable criteria met their targets. In `tools.py::search_listings`, equal-weight keyword overlap allowed the Y2K Baby Tee — Butterfly Print ($18, Depop) to outrank more directly relevant graphic tees for `vintage graphic tee under $30`. This is a tool-level ranking mechanism, not a failure in the agent's branch or MCP wiring. The change targeted this weakness. For criteria 3–5, the unresolved issue is evaluation visibility: abbreviated traces do not prove exact IDs or the entirety of generated text.

---

## Loop Trace

<!-- One full run, printed step by step, with the MCP call visible in it.

     `python app.py ask '...' --trace` once you've added the trace.step()

     calls in Milestone 2.

     Worth pasting BOTH the happy path and the empty-search path. The empty

     one should be visibly shorter, because it stops. If your two traces are

     the same length, your branch isn't working — and this is the fastest way

     anyone will ever find that out. -->

**Happy path**

```text
[1] parse_query
    out: dict with keys: description, size, max_price
[2] search_listings (via MCP)
    out: 10 items: Graphic Tee — 2003 Tour Bootleg Style, Vintage Band Tee — Faded Grey ...
    → called through mcp_client.call_tool → mcp_server.py
[3] suggest_outfit
    in: Graphic Tee — 2003 Tour Bootleg Style ($24.0, depop)
[4] create_fit_card
    out: Scored this ultimate Graphic Tee — 2003 Tour Bootleg Style for just $24.00 on Depop ...
try 1: completed — fit card 349 chars
```

**Empty search**

```text
[1] parse_query
    out: dict with keys: description, size, max_price
[2] search_listings (via MCP)
    out: [] (empty)
    → called through mcp_client.call_tool → mcp_server.py
[3] stop
    → No listings found. Skipping outfit and fit card.
try 1: stopped early — No matching items found. Try increasing your budget ...
```

****On the MCP move:** `search_listings` is invoked using `mcp_client.call_tool` through `mcp_server.py`, as confirmed in both evaluation logs. The after-evaluation continued to show successful MCP calls and correct early stopping, so no regression was observed in the tested workflow.** <!-- what changed in your code, and whether anything

behaved differently afterwards. If the rewire didn't work, say exactly where it

broke — the error text and the last thing that worked. That earns the point in

full. -->

---

## The Improvement

<!-- What you changed, why your diagnosis pointed at it, and the after-run in

     the same table format. One change, measured properly.

     `python run_eval.py --label after` -->

**What I changed:** In `tools.py::search_listings`, replaced equal-weight keyword overlap with weighted relevance: +10 for an exact title phrase, +5 per matching title token, +3 per category token, +2 per style-tag token, and +1 per description/color token. Price and size filters remain in place.

**Which failure it was meant to fix:** The baseline selected `Y2K Baby Tee — Butterfly Print` ($18, Depop) for `vintage graphic tee under $30`, even though `Graphic Tee — 2003 Tour Bootleg Style` was a more direct match. The ranking change prioritized garment-type matches in titles.

### Run Log — After

| Criterion | Target | Try 1 | Try 2 | Try 3 | Try 4 | Try 5 | Verdict |
|---|---|---|---|---|---|---|---|
| 1. Matching query completes all three tools | 4/5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 2. Impossible query stops early | 5/5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 3. Selected item consistent across tools | 5/5 | CHECK | CHECK | CHECK | CHECK | CHECK | Not fully verified |
| 4. Fit card price/platform accurate | 4/5 | CHECK | CHECK | CHECK | CHECK | CHECK | Not fully verified |
| 5. Empty wardrobe: two outfits, no invented ownership | 4/5 | CHECK | CHECK | CHECK | CHECK | CHECK | Not fully verified |

**Did it help, and how do I know:** Yes, for the tested query. The after run (`results/run_2026-10-13_2334_after.md`) selected `Graphic Tee — 2003 Tour Bootleg Style` ($24, Depop) in all five relevant trials, instead of the Y2K Baby Tee selected in the baseline. All 25 after-evaluation trials completed or stopped as intended; 40 model calls were recorded. This supports improved relevance for the tested query, not a claim that all searches are now optimal.

<!-- If it made things worse, say that. Honestly reported, that earns full

     credit and is more interesting than one that worked. -->

---

## What's Still Broken

<!-- For each criterion still missed: what you'd do, and why you stopped where

     you did. "I ran out of time" is fine if it's true. Pretending nothing is

     left is not. -->

Search is still lexical and can include loosely related items (such as hoodies for a graphic-tee query). A future iteration could add garment-category constraints and synonym handling. Criteria 3–5 also need more explicit evidence: item-ID assertions, complete fit-card text checks, and checks that empty-wardrobe suggestions do not claim ownership of nonexistent items. The model-unavailable failure mode has not been demonstrated in the supplied evaluation logs, so it should be tested separately before checking off that submission requirement.


<!-- ═════════════════════════════════════════════════════════════════════

     SUBMISSION CHECKLIST — unit 3

       [ ] criteria.md has five numbered criteria, each with a target

       [ ] Each criterion has a reason underneath it

       [ ] All five unit 3 sections above have real content

       [ ] Tool Inventory: all three tools, inputs WITH TYPES, a specific

           return value, and the empty case

       [ ] Planning Loop names the branch rule and agent.py::run_agent

       [ ] Sample Run: one full query plus the three per-tool tests, as text

       [ ] At least four new commits

       [ ] Repository URL submitted — WRITE IT DOWN, you submit the same one

           next unit

     SUBMISSION CHECKLIST — unit 4

       [ ] mcp_server.py exists with one tool registered

           (or a written record of exactly where the rewire broke)

       [ ] Run Log — Before, five criteria, five tries each

       [ ] Real output pasted underneath, naming file and function

       [ ] A verdict on every criterion

       [ ] A diagnosis for every miss, naming a place AND a mechanism

       [ ] Loop Trace, with the MCP call visible in it

       [ ] All three failure modes triggered and handled

       [ ] One improvement, with Run Log — After in the same format

       [ ] What's Still Broken

       [ ] At least four new commits

       [ ] The SAME repository URL as last unit

     Do not delete and recreate this repository. Your commit history is what

     shows your criteria existed before your results did.

     ═════════════════════════════════════════════════════════════════════ -->

---

📖 ****How to run this project: [RUNNING.md](**RUNNING.md**)****
