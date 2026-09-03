# lohan-desilva-portfolio

Source for [lohandesilva.github.io/lohan-desilva-portfolio](https://lohandesilva.github.io/lohan-desilva-portfolio/).

A static site — no build step, no framework, no dependencies. Five analytics
projects, each linking to its own repository, executive summary and technical
appendix.

## Layout

```
index.html              landing page and the work list
cv.html                 CV
projects/*.html         one case study per project
assets/style.css        the whole stylesheet
assets/figures/         figures copied from each project's outputs/
build_pages.py          generates projects/*.html from one template
```

The project pages share a structure, so the layout lives in `build_pages.py`
once rather than in five files that drift apart. Editing a case study means
editing the content dictionary in that script and re-running it:

```bash
python build_pages.py
```

`index.html` and `cv.html` are hand-written; they are one-offs and templating
them would cost more than it saves.

## Figures

Every figure under `assets/figures/` is produced by the corresponding project's
analysis pipeline, not drawn by hand. To refresh them, run `make analysis` in
the project repository and copy the contents of its `outputs/figures/`
directory across.

## The numbers on these pages

Every figure quoted on the site comes from a `metrics.json` written by the
relevant pipeline. Where a number changes, it changes in the pipeline first.

## Deployment

GitHub Pages, served from the default branch root. `.nojekyll` is present so
Pages serves the directory as-is rather than running it through Jekyll.

## Projects

| Project | Repository |
|---|---|
| Churn and retention economics | [customer-churn-analysis](https://github.com/Lohandesilva/customer-churn-analysis) |
| Sales performance and discount policy | [sales-performance-analytics](https://github.com/Lohandesilva/sales-performance-analytics) |
| S&P 500 profitability and valuation | [financial-performance-analysis](https://github.com/Lohandesilva/financial-performance-analysis) |
| Credit portfolio risk | [credit-portfolio-risk](https://github.com/Lohandesilva/credit-portfolio-risk) |
| Clinic capacity and non-attendance | [healthcare-operations-analytics](https://github.com/Lohandesilva/healthcare-operations-analytics) |
