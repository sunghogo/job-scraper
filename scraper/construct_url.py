from typing import Dict

# Parse search strings and options and to construct indeed url
def construct_indeed_url(search_position: str, search_location: str, search_options: Dict[str, str] = None):
    base_url = 'https://www.indeed.com'

    parsed_search_position = search_position.replace(' ', '+')
    parsed_search_location = search_location.replace(
        ' ', '+') if ',' not in search_location else f"{search_location.split(',')[0].replace(' ', '+')}%2C+{search_location.split(',')[1].strip()}"

    url = f"{base_url}/jobs?q={parsed_search_position}&l={parsed_search_location}"

    if search_options != None:
        for key, value in search_options.items():
            if key == 'experience_level' and value != "ALL":  # "ENTRY_LEVEL", "ALL"
                url += f"&sc=0kf%3Aexplvl({value})%3B"
            elif key == "sort_date":
                url += f"&sort=date"
            elif key == "date_posted":  # "1", "3", "7"
                url += f"&fromage={value}"
            elif key == "filter_dupe":  # "0" to turn off dupe filter, "1"
                url += f"&filter={value}"
            elif key == "page":  # "1", "2", ...
                url += f"&start={str(int(value) * 10 - 10)}"

    return url
