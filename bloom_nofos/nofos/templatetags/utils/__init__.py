from bs4 import BeautifulSoup, NavigableString

# HTML tables


def _add_class_if_not_exists_to_tag(element, classname, tag_name):
    """
    Adds the given class to the element if it does not already exist.
    Checks if the classname exists in the element's "class" attribute
    and adds it if missing. Also checks if tag_name matches the element's name.
    """
    if classname not in element.get("class", []):
        if tag_name and element.name == tag_name:
            element["class"] = element.get("class", []) + [classname]


def _add_class_if_not_exists_to_tags(element, classname, tag_names):
    """
    Adds the given class to the element if it does not already exist.
    Checks if the classname exists in the element's "class" attribute
    and adds it if missing. Also checks if tag_name matches the element's name.
    """
    for tag_name in tag_names.split("|"):
        _add_class_if_not_exists_to_tag(element, classname, tag_name)


def add_caption_to_table(table):
    """
    Adds a caption to a BeautifulSoup table element.

    Searches previous sibling elements for a paragraph starting with "table: ",
    extracts it and inserts it as a <caption> element inside the table.
    If a caption is added, it also adds a class to the table.

    Args:
        table: A BeautifulSoup table element
    """
    caption = None
    # we want to look for paragraphs that start with "table: "
    caption_text = "table: "

    for s in table.previous_siblings:
        if s.name and s.name != "table" and len(s.text):
            if s.text.lower().startswith(caption_text):
                s.string = s.text  # strip spans
                caption = s.extract()  # remove element from the tree
            break

    if caption:
        caption.name = "caption"  # reassign tag to <caption>
        table.insert(0, caption)
        _add_class_if_not_exists_to_tag(table, "table--with-caption", "table")


def add_class_to_list(html_list):
    # Get the last list item
    final_list_item = html_list.find_all("li")[-1] if html_list.find_all("li") else None
    if final_list_item:
        # Check if the text length is less than 85 characters
        if len(final_list_item.get_text(strip=True)) < 85:
            # Add the classname
            _add_class_if_not_exists_to_tag(
                final_list_item, "avoid-page-break-before", "li"
            )


def _get_total_word_count(table_cells):
    word_count = 0

    for cell in table_cells:
        cell_text = cell.get_text()
        # Split the text into words based on whitespace and count them
        words = cell_text.split()
        word_count += len(words)

    return word_count


def add_class_to_table(table):
    """
    Adds a size class to a BeautifulSoup table based on column and row count.

    Counts the columns in the first row and the number of rows:
     - "table--small": 3 columns or less
     - "table--large": 4 columns or more
    """

    def _get_table_class(num_cols):
        if num_cols >= 3:
            return "table--large"

        return "table--small"

    if is_callout_box_table_markdown(table):
        return "table--callout-box"

    rows = table.find_all("tr")
    cols = rows[0].find_all("th") + rows[0].find_all("td")

    if table.find("th", string="Recommended For"):
        return "table--large"

    word_count = _get_total_word_count(table.find_all("td"))

    if word_count == 0 and len(cols) < 4:
        return "table--small"
    elif word_count > 120:
        return "table--large"

    return _get_table_class(len(cols))


def add_class_to_table_rows(table_row):
    """
    Adds a size class to a BeautifulSoup table cell based on if the row is empty.
    """

    word_count = _get_total_word_count(table_row.find_all(["td", "th"]))

    if word_count == 0:
        return "table-row--empty"


def convert_paragraph_to_searchable_hr(p):
    def _create_hr_and_span(hr_class, span_text):
        hr_html = '<hr class="{} page-break--hr">'.format(hr_class)
        span_html = '<span class="page-break--hr--text">{}</span>'.format(span_text)
        return BeautifulSoup(hr_html, "html.parser"), BeautifulSoup(
            span_html, "html.parser"
        )

    if p.name == "p" and p.string in [
        "page-break-before",
        "page-break-after",
        "column-break-before",
        "column-break-after",
    ]:
        # Change the tag name from 'p' to 'div'
        p.name = "div"

        if p.string == "page-break-before":
            p["class"] = "page-break--hr--container page-break-before--container"
            hr, span = _create_hr_and_span(
                "page-break-before", "[ ↑ page-break-before ↑ ]"
            )

        if p.string == "page-break-after":
            p["class"] = "page-break--hr--container page-break-after--container"
            hr, span = _create_hr_and_span(
                "page-break-after", "[ ↓ page-break-after ↓ ]"
            )

        if p.string == "column-break-before":
            p["class"] = "page-break--hr--container column-break-before--container"
            hr, span = _create_hr_and_span(
                "column-break-before", "[ ← column-break-before ← ]"
            )

        if p.string == "column-break-after":
            p["class"] = "page-break--hr--container column-break-after--container"
            hr, span = _create_hr_and_span(
                "column-break-after", "[ → column-break-after → ]"
            )

        p.clear()
        p.append(hr)
        p.append(span)


def find_elements_with_character(element, container, character="~"):
    # Recursively searches the element and its children for any strings containing the given character.
    # Any elements containing the character are added to the given container.
    # Parameters:
    #   element: The element to search through
    #   container: The list to add any found elements to
    #   character: The character to search for in strings
    if isinstance(element, NavigableString):
        if character in element:
            container.append(element.parent)
    else:
        for child in element.children:
            find_elements_with_character(child, container, character)


def get_parent_td(element):
    """
    Gets the parent <td> element for a given element, which may include itself.

    Traverses up the element's parents looking for a <td> tag.
    Returns the first parent <td> found, or False if none exists.
    """
    if element.name == "td":
        return element

    for parent in element.parents:
        if parent.name == "td":
            return parent

    return False


def is_callout_box_table_markdown(table):
    rows = table.find_all("tr")
    cols = rows[0].find_all("th") + rows[0].find_all("td")
    tds = table.find_all("td")

    return (
        len(cols) == 1  # 1 column
        and len(rows) == 2  # 2 rows (thead and tbody generated automatically)
        and len(tds) == 1  # 1 cell
        and tds[0]
        and tds[0].get_text().strip() == ""  # the cell is empty
    )


# Footnotes


def is_footnote_ref(a_tag):
    """
    Checks if the given a_tag is a footnote reference link
    by verifying it matches the expected footnote link format: eg, "[1]" or "[10]", or "↑"
    """
    text = a_tag.get_text().strip()
    if text == "↑":
        return True

    return (
        len(text) >= 3  # at least 3 characters
        and text.startswith("[")
        and text.endswith("]")
        and text[1:-1].isdigit()
    )


def get_footnote_type(a_tag):
    href = a_tag.get("href", "").strip()

    # HTML
    # Inline footnote links look like "<a href="#ref10">[10]</a>"
    # Endnote footnote links look like "<a href="#ftnt_ref10">[10]</a>"
    if href.startswith("#ref") or href.startswith("#ftnt"):
        return "html"

    # DOCX
    # Inline footnote links look like "<a href="#footnote-1">[2]</a>"
    # Endnote footnote links look like "<a href="#footnote-ref-1">↑</a>"
    if href.startswith("#footnote"):
        return "docx"

    return None


def format_footnote_ref_html(a_tag):
    """
    Formats a footnote reference link tag to have the expected ID and href attributes
    based on whether it is an endnote or inline footnote reference.

    Inline footnote links look like "<a href="#ref10">[10]</a>"
    Endnote footnote links look like "<a href="#ftnt_ref10">[10]</a>"
    """
    footnote_text = a_tag.get_text().strip()
    footnote_number = footnote_text[1:-1]
    footnote_href = a_tag.get("href").strip()

    a_tag.string = footnote_text

    # these are the endnotes references
    if footnote_href.startswith("#ftnt_"):
        a_tag["id"] = "ftnt{}".format(footnote_number)

    # these are in the body of the document
    else:
        a_tag["id"] = "ftnt_ref{}".format(footnote_number)
        a_tag["href"] = "#ftnt{}".format(footnote_number)


def is_floating_callout_box(subsection):
    # maybe not the best idea long-term but it works for now
    floating_subsection_strings = [
        "Key facts",
        "Key dates",
        "Questions?",
        "Have questions?",
        "**Have questions?",
    ]

    if subsection.name:
        return subsection.name.strip() in floating_subsection_strings

    for subsection_string in floating_subsection_strings:
        if subsection.body.strip().startswith(subsection_string):
            return True

    return False
