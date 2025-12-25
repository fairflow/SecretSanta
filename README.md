# Secret Santa

A small Secret Santa helper that generates assignments with **no self-assignments** (a *derangement*).

## Math background (derangements)

A *derangement* is a permutation of `n` items with **no fixed points**.

The number of derangements is traditionally written as the **subfactorial** `!n` (distinct from the factorial `n!`).

Using inclusion–exclusion, one obtains:

$$
!n = n!\sum_{k=0}^{n}\frac{(-1)^k}{k!}
$$

and therefore the probability that a uniformly random permutation of size `n` is a derangement is:

$$
\Pr(\text{derangement}) = \frac{!n}{n!} = \sum_{k=0}^{n}\frac{(-1)^k}{k!} \xrightarrow[n\to\infty]{} e^{-1}.
$$

### Will this render on GitHub?

Yes: GitHub supports LaTeX-style math in Markdown files (including `README.md`) using `$...$` for inline math and `$$...$$` for display math.

If you view this file somewhere that *doesn't* support math rendering, the formulas will still be readable as plain text.

## Run the Streamlit app

```bash
source .venv/bin/activate
streamlit run streamlit_app.py --server.port 6701 &
```
