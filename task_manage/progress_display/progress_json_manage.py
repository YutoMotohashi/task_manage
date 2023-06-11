import numpy as np
from box import BoxList


def get_progress_from_children(data):
    if data["children"] is None:
        ret_val = float(
            data["progress"]) if data["progress"] is not None else 0
    else:
        progress = []
        for i in data["children"]:
            progress.append(get_progress_from_children(i))
        # print(progress)
        ret_val = np.average(progress)
    data["progress"] = ret_val
    return ret_val


def update_progress(filename):
    progress_data = BoxList.from_json(filename=filename)

    for i in progress_data:
        get_progress_from_children(i)

    progress_data.to_json(filename=filename)
    return progress_data


def validate_progress_element_format(data):
    if not isinstance(data, (dict)):
        raise ValueError(f"Data is not a dict: {data}")

    if "category" not in data:
        raise AssertionError(f"category is not in data: {data}")
    if "children" not in data:
        raise AssertionError(f"children is not in data: {data}")
    if "comment" not in data:
        raise AssertionError(f"comment is not in data: {data}")
    if "name" not in data:
        raise AssertionError(f"name is not in data: {data}")
    if "number" not in data:
        raise AssertionError(f"number is not in data: {data}")
    if "progress" not in data:
        raise AssertionError(f"progress is not in data: {data}")
    if "summary" not in data:
        raise AssertionError(f"summary is not in data: {data}")
    if "todo" not in data:
        raise AssertionError(f"todo is not in data: {data}")
    if "comment" not in data:
        raise AssertionError(f"comment is not in data: {data}")

    if not isinstance(data["category"], (str)):
        raise ValueError(f"category is not a string: {data['category']}")
    if not (isinstance(data["children"], (list)) or data["children"] is None):
        raise ValueError(
            f"children is not a list nor None: {data['children']}")
    if not isinstance(data["name"], (str)):
        raise ValueError(f"name is not a string: {data['name']}")
    if not isinstance(data["number"], (str, int)):
        raise ValueError(f"number is not a string or int: {data['number']}")
    if not isinstance(data["progress"], (int, float)):
        raise ValueError(f"progress is not a int or float: {data['progress']}")
    if not data["progress"] >= 0:
        raise AssertionError(f"progress is not >= 0: {data['progress']}")
    if not data["progress"] <= 100:
        raise AssertionError(f"progress is not <= 100: {data['progress']}")
    if not (isinstance(data["summary"], (str)) or data["summary"] is None):
        raise ValueError(f"summary is not a string: {data['summary']}")
    if not (isinstance(data["todo"], (str)) or data["todo"] is None):
        raise ValueError(f"todo is not a string: {data['todo']}")
    if not (isinstance(data["comment"], (str)) or data["comment"] is None):
        raise ValueError(f"comment is not a string: {data['comment']}")

    return True


def validate_progress_data_format(data):
    try:
        validate_progress_element_format(data)
        try:
            if (data["children"] is None) or (data["children"] == []):
                validate_progress_element_format(data)
            else:
                for child in data["children"]:
                    validate_progress_data_format(child)
            return True
        except ValueError as e:
            raise ValueError(
                f"Data is not a valid progress data: {data}") from e
        except AssertionError as e:
            raise AssertionError(
                f"Data is not a valid progress data: {data}") from e
    except ValueError as e:
        raise ValueError(f"Data is not a valid progress data: {data}") from e
    except AssertionError as e:
        raise AssertionError(
            f"Data is not a valid progress data: {data}") from e


def create_empty_progress_data():
    data = {
        "category": "category",
        "children": None,
        "name": "title",
        "number": "0",
        "progress": 0,
        "summary": "summary",
        "todo": "todo",
        "comment": "comment"}
    return data
