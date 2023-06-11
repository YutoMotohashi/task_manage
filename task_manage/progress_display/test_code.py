from . import progress_json_manage as pjm
import pytest


def test_validate_progress_element_format_1():
    data = {
        "category": "test",
        "children": None,
        "name": "name",
        "number": "number",
        "progress": 0,
        "summary": "summary",
        "todo": "todo",
        "comment": "comment"}
    assert pjm.validate_progress_element_format(data)


def test_validate_progress_element_format_2():
    data = {
        "category": "test",
        "children": [],
        "name": "name",
        "number": "number",
        "progress": 0,
        "summary": "summary",
        "todo": "todo",
        "comment": "comment"}
    assert pjm.validate_progress_element_format(data)


def test_validate_progress_element_format_value_1():
    data = [1, 2, 3]
    with pytest.raises((ValueError)):
        pjm.validate_progress_element_format(data)


def test_validate_progress_element_format_value_2():
    data = {
        "category": None,  # here is the problem
        "children": None,
        "name": "name",
        "number": "number",
        "progress": 0,
        "summary": "summary",
        "todo": "todo",
        "comment": "comment"}
    with pytest.raises((ValueError)):
        pjm.validate_progress_element_format(data)


def test_validate_progress_element_format_value_3():
    data = {
        "category": "test",
        "children": {},  # here is the problem
        "name": "name",
        "number": "number",
        "progress": 0,
        "summary": "summary",
        "todo": "todo",
        "comment": "comment"}
    with pytest.raises((ValueError)):
        pjm.validate_progress_element_format(data)


def test_validate_progress_element_format_value_4():
    data = {
        "category": "test",
        "children": None,
        "name": 1,  # here is the problem
        "number": "number",
        "progress": 0,
        "summary": "summary",
        "todo": "todo",
        "comment": "comment"}
    with pytest.raises((ValueError)):
        pjm.validate_progress_element_format(data)


def test_validate_progress_element_format_value_5():
    data = {
        "category": "test",
        "children": None,
        "name": "name",
        "number": [],  # here is the problem
        "progress": 0,
        "summary": "summary",
        "todo": "todo",
        "comment": "comment"}
    with pytest.raises((ValueError)):
        pjm.validate_progress_element_format(data)


def test_validate_progress_element_format_value_6():
    data = {
        "category": "test",
        "children": None,
        "name": "name",
        "number": "number",
        "progress": "test",  # here is the problem
        "summary": "summary",
        "todo": "todo",
        "comment": "comment"}
    with pytest.raises((ValueError)):
        pjm.validate_progress_element_format(data)


def test_validate_progress_element_format_value_7():
    data = {
        "category": "test",
        "children": None,
        "name": "name",
        "number": "number",
        "progress": [],  # here is the problem
        "summary": "summary",
        "todo": "todo",
        "comment": "comment"}
    with pytest.raises((ValueError)):
        pjm.validate_progress_element_format(data)


def test_validate_progress_element_format_value_8():
    data = {
        "category": "test",
        "children": None,
        "name": "name",
        "number": "number",
        "progress": None,
        "summary": "summary",
        "todo": "todo",
        "comment": "comment"}
    with pytest.raises((ValueError)):
        pjm.validate_progress_element_format(data)


def test_validate_progress_element_format_value_9():
    data = {
        "category": "test",
        "children": None,
        "name": "name",
        "number": "number",
        "progress": 0,
        "summary": [],
        "todo": "todo",
        "comment": "comment"}
    with pytest.raises((ValueError)):
        pjm.validate_progress_element_format(data)


def test_validate_progress_element_format_value_10():
    data = {
        "category": "test",
        "children": None,
        "name": "name",
        "number": "number",
        "progress": 0,
        "summary": "summary",
        "todo": 1,
        "comment": "comment"}
    with pytest.raises((ValueError)):
        pjm.validate_progress_element_format(data)


def test_validate_progress_element_format_value_11():
    data = {
        "category": "test",
        "children": None,
        "name": "name",
        "number": "number",
        "progress": 0,
        "summary": "summary",
        "todo": "todo",
        "comment": pjm}
    with pytest.raises((ValueError)):
        pjm.validate_progress_element_format(data)


def test_validate_progress_element_format_assert_1():
    data = {
        "category": "test",
        "children": None,
        "name": "name",
        "number": "number",
        "progress": -1,
        "summary": "summary",
        "todo": "todo",
        "comment": "comment"}
    with pytest.raises((AssertionError)):
        pjm.validate_progress_element_format(data)


def test_validate_progress_element_format_assert_2():
    data = {
        "category": "test",
        "children": None,
        "name": "name",
        "number": "number",
        "progress": 1000,
        "summary": "summary",
        "todo": "todo",
        "comment": "comment"}
    with pytest.raises((AssertionError)):
        pjm.validate_progress_element_format(data)


def test_validate_progress_data_format_1():
    data = {
        "category": "test",
        "children": None,
        "name": "name",
        "number": "number",
        "progress": 0,
        "summary": "summary",
        "todo": "todo",
        "comment": "comment"}
    assert pjm.validate_progress_data_format(data)


def test_validate_progress_data_format_2():
    data = {
        "category": "test",
        "children": [{
            "category": "test",
            "children": None,
            "name": "name",
            "number": "number",
            "progress": 0,
            "summary": "summary",
            "todo": "todo",
            "comment": "comment"}, {
            "category": "test",
            "children": None,
            "name": "name",
            "number": "number",
            "progress": 0,
            "summary": "summary",
            "todo": "todo",
            "comment": "comment"}],
        "name": "name",
        "number": "number",
        "progress": 0,
        "summary": "summary",
        "todo": "todo",
        "comment": "comment"}
    assert pjm.validate_progress_data_format(data)


def test_validate_progress_data_format_3():
    data = {
        "category": "test",
        "children": {
            "category": "test",
            "children": None,
            "name": "name",
            "number": "number",
            "progress": 0,
            "summary": "summary",
            "todo": "todo",
            "comment": "comment"},
        "name": "name",
        "number": "number",
        "progress": 0,
        "summary": "summary",
        "todo": "todo",
        "comment": "comment"}
    with pytest.raises((ValueError)):
        pjm.validate_progress_data_format(data)


def test_create_empty_progress_data():
    assert pjm.validate_progress_data_format(pjm.create_empty_progress_data())
