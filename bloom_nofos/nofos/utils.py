import re

from slugify import slugify


def match_view_url(url):
    """
    Check if the given URL matches the pattern "/nofos/{integer}".

    Args:
    url (str): The URL to be checked.

    Returns:
    bool: True if the URL matches the pattern, False otherwise.
    """
    # Regular expression to match the specified pattern
    pattern = r"^/nofos/\d+$"

    return bool(re.match(pattern, url))


def clean_string(string):
    """Cleans the given string by removing extra whitespace."""
    return re.sub("\s+", " ", string.strip())


def create_subsection_html_id(counter, subsection):
    section_name = subsection.section.name
    return "{}--{}--{}".format(counter, slugify(section_name), slugify(subsection.name))


def get_icon_path_choices(theme):
    if theme == "portrait-acf-white":
        return [
            (
                "nofo--icons--border",
                "(Filled) Color background, white icon, white outline",
            ),
            (
                "nofo--icons--solid",
                "(Standard) White background, color icon, color outline",
            ),
            (
                "nofo--icons--thin",
                "(Thin) White background, color icon, color outline",
            ),
        ]

    return [
        ("nofo--icons--border", "(Filled) Color background, white icon, white outline"),
        (
            "nofo--icons--solid",
            "(Standard) White background, color icon, color outline",
        ),
    ]


class StyleMapManager:
    def __init__(self):
        self.styles = []

    def add_style(self, style_rule, location_in_nofo, note=None):
        self.styles.append(
            {
                "style_rule": style_rule,
                "location_in_nofo": location_in_nofo,
                "note": note if note else None,
            }
        )

    def get_style_map(self):
        # This method will now just join all the individual style rules.
        return "\n".join(style["style_rule"] for style in self.styles)


# Pre-instantiate StyleMapManager and add styles
style_map_manager = StyleMapManager()
style_map_manager.add_style(
    style_rule="p[style-name='Emphasis A'] => strong",
    location_in_nofo="Step 2 > Grants.gov > Need Help?",
    note="Just bold the entire sentence",
)
style_map_manager.add_style(
    style_rule="p[style-name='Table'] => p",
    location_in_nofo="Step 3 > Other required forms > All table cells",
    note="Don't do anything: this is being applied to paragraphs in a table and we don't need special styling for them.",
)
style_map_manager.add_style(
    style_rule="p[style-name='Normal (Web)'] => p",
    location_in_nofo="Step 4 > Risk Review > p",
    note="Don't do anything: not sure why this is formatted differently, but it's just body text.",
)
style_map_manager.add_style(
    style_rule="r[style-name='normaltextrun'] => span",
    location_in_nofo="Step 2 > Grants.gov > You can see && Step 3 > Third party agreements",
    note="Don't do anything: body text + a header",
)
style_map_manager.add_style(
    style_rule="r[style-name='Subtle Emphasis'] => strong.subtle-emphasis",
    location_in_nofo="Step 3 > Required format > Fonts/Spacing",
    note="Bold is safe, but they might possibly be headings.",
)
style_map_manager.add_style(
    style_rule="r[style-name='Intense Reference'] => span.intense-reference",
    location_in_nofo="Step 3 > Required format",
    note="Don't do anything: it's formatted as a header already, go with that.",
)
