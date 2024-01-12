from typing import Dict

base_indeed_url = 'https://www.indeed.com'


def construct_indeed_url(search_position: str, search_location: str, search_options: Dict[str, str] = None) -> str:
    """Constructs indeed search url using the given search strings and options

    Args:
        search_position (str): REQUIRED Job Position Title
        search_location (str): REQUIRED Job Location
        search_options (Dict[str, str], optional): OPTIONAL Additional search options. 
            The available key/value pairs are:
                "experience_level" : None/"ALL", "ENTRY_LEVEL"
                "sort_date" : None/"OFF", "ON"
                "filter_date" : None/"ALL", "1", "7", "14", "30", ...
                "filter_dupe" : None/"OFF", "ON"
                "page" : None/"1", "2", "3", ...

    Returns:
        str: Indeed url with embedded search options
    """

    parsed_search_position = search_position.replace(' ', '+')
    parsed_search_location = search_location.replace(
        ' ', '+') if ',' not in search_location else f"{search_location.split(',')[0].replace(' ', '+')}%2C+{search_location.split(',')[1].strip()}"

    url = f"{base_indeed_url}/jobs?q={parsed_search_position}&l={parsed_search_location}"

    if search_options != None:
        for key, value in search_options.items():
            match key:
                case 'experience_level':
                    if value != "ALL":
                        url += f"&sc=0kf%3Aexplvl({value})%3B"
                case "sort_date":
                    if value != "OFF":
                        url += f"&sort=date"
                case "filter_date":
                    if value != "ALL":
                        url += f"&fromage={value}"
                case "filter_dupe":
                    if value != "OFF":
                        url += f"&filter={value}"
                case"page":
                    url += f"&start={str(int(value) * 10 - 10)}"

    return url
