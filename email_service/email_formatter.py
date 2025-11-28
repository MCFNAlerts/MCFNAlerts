import json
from datetime import date, timedelta
from string import Template


def format_email(json_path, template_path="email_service/email_template.html"):
    with open(json_path, "r") as f:
        data = json.load(f)

    contributions = [item for item in data if item["Source"] == "contributions"]
    expenditures = [item for item in data if item["Source"] == "expenditures"]

    # Load HTML template
    with open(template_path, "r") as f:
        template_str = f.read()

    # Inline mini templating (simple but effective)
    from jinja2 import Template as JinjaTemplate
    tmpl = JinjaTemplate(template_str)
    dateToday = date.today() - timedelta(days=1)
    dateToday = dateToday.strftime("%B %d, %Y")
    html = tmpl.render(
        DATE=str(dateToday),
        contributions=contributions,
        expenditures=expenditures,
        DONATION_MIN="1000",
        EXPENDITURE_MIN="5000"
    )

    return html


if __name__ == "__main__":
    html = format_email("filtered_combined.json")
    print(html)  # preview the beginning of the email
