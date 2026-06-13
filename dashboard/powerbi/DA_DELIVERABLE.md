# Power BI — DA Portfolio Deliverable

This project uses a **screenshots + CSV export** approach for the Data Analyst portfolio layer. A `.pbix` file is optional and built locally in Power BI Desktop.

## Official DA artifacts (in repo)

| Artifact | Location | Purpose |
|----------|----------|---------|
| Dashboard screenshots | [screenshots/](screenshots/) | Executive views for README & resume |
| KPI CSV exports | [data/](data/) | Source data for optional Power BI build |
| Streamlit live demo | [../streamlit/app.py](../streamlit/app.py) | Interactive GitHub-friendly dashboard |

## Why no `.pbix` in git?

- Power BI files are large, binary, and require Desktop to edit
- Screenshots prove the same KPIs recruiters expect on a DA resume
- CSV exports let anyone rebuild the report in ~15 minutes

## Resume wording (DA)

> Built executive dashboards on **100K+** marketplace orders tracking revenue growth, cohort retention, and regional churn; surfaced **89%** 90-day churn in top category **health_beauty**. Dashboard screenshots and KPI exports in GitHub repo.

## Refresh exports

After running the pipeline:

```bash
python scripts/export_powerbi_csvs.py
python scripts/generate_dashboard_screenshots.py
```

Optional `.pbix` build: [BUILD_GUIDE.md](BUILD_GUIDE.md)
