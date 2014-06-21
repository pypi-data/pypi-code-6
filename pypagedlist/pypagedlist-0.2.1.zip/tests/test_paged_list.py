# -*- coding: utf-8 -*-
import pytest

from pagedlist import SimplePagedList


def test_none_data_doesnt_thrown_exception():
    SimplePagedList(None, 1, 10)


def test_page_number_below_one_throws_index_error_exception():
    data = [1, 2, 3]
    with pytest.raises(IndexError):
        SimplePagedList(data, 0, 1)


def test_page_number_above_record_count_returns_empty_list():
    data = [1, 2, 3]
    paged_list = SimplePagedList(data, 2, 3)
    assert len(paged_list) == 0


def test_page_size_less_than_one_throws_index_error_exception():
    data = [1, 2, 3]
    with pytest.raises(IndexError):
        SimplePagedList(data, 1, 0)


def test_none_data_set_doesnt_return_none():
    paged_list = SimplePagedList(None, 1, 10)
    assert paged_list is not None


def test_none_data_set_returns_zero_pages():
    paged_list = SimplePagedList(None, 1, 10)
    assert paged_list.page_count == 0


def test_zero_item_data_set_returns_zero_pages():
    paged_list = SimplePagedList([], 1, 10)
    assert paged_list.page_count == 0


def test_dataset_of_one_through_five_page_size_of_two_page_number_of_two_first_item_is_three():
    data = [1, 2, 3, 4, 5]
    paged_list = SimplePagedList(data, 2, 2)
    assert paged_list[0] == 3


def test_total_count_is_preserved():
    data = [1, 2, 3, 4, 5]
    paged_list = SimplePagedList(data, 2, 2)
    assert paged_list.total_item_count == len(data)


def test_page_size_is_preserved():
    data = [1, 2, 3, 4, 5]
    paged_list = SimplePagedList(data, 2, 2)
    assert len(paged_list) == 2

    paged_list = SimplePagedList(data, 3, 2)
    assert len(paged_list) == 1


def test_dataset_one_through_six_page_size_three_page_number_one_first_value_is_one():
    data = list(range(1, 7))
    paged_list = SimplePagedList(data, 1, 3)
    assert paged_list[0] == 1


def test_dataset_one_through_three_page_size_one_page_number_three_has_next_page_false():
    data = [1, 2, 3]
    paged_list = SimplePagedList(data, 3, 1)
    assert not paged_list.has_next_page


def test_dataset_one_through_three_page_size_one_page_number_three_is_last_page_true():
    data = [1, 2, 3]
    paged_list = SimplePagedList(data, 3, 1)
    assert paged_list.is_last_page


def test_dataset_one_and_two_page_size_one_page_number_two_first_value_is_two():
    data = [1, 2]
    paged_list = SimplePagedList(data, 2, 1)
    assert paged_list[0] == 2


def test_dataset_one_through_ten_page_size_five_page_number_one_first_item_on_page_is_one():
    data = list(range(1, 11))
    paged_list = SimplePagedList(data, 1, 5)
    assert paged_list.first_item_on_page == 1


def test_dataset_one_through_ten_page_size_five_page_number_two_first_item_on_page_is_six():
    data = list(range(1, 11))
    paged_list = SimplePagedList(data, 2, 5)
    assert paged_list.first_item_on_page == 6


def test_dataset_one_through_ten_page_size_five_page_number_one_last_item_on_page_is_five():
    data = list(range(1, 11))
    paged_list = SimplePagedList(data, 1, 5)
    assert paged_list.last_item_on_page == 5


def test_dataset_one_through_ten_page_size_five_page_number_two_last_item_on_page_is_ten():
    data = list(range(1, 11))
    paged_list = SimplePagedList(data, 2, 5)
    assert paged_list.last_item_on_page == 10


def test_dataset_one_through_eight_page_size_five_page_number_two_last_item_on_page_is_eight():
    data = list(range(1, 9))
    paged_list = SimplePagedList(data, 2, 5)
    assert paged_list.last_item_on_page == 8


@pytest.mark.parametrize(
    'integers, page_number, page_size, expected_has_previous, expected_has_next', [
        ([1, 2, 3], 1, 1, False, True),
        ([1, 2, 3], 2, 1, True, True),
        ([1, 2, 3], 3, 1, True, False),
    ])
def test_has_previous_page_and_has_next_page_are_correct(
        integers, page_number, page_size, expected_has_previous,
        expected_has_next):
    paged_list = SimplePagedList(integers, page_number, page_size)
    assert paged_list.has_previous_page == expected_has_previous
    assert paged_list.has_next_page == expected_has_next


@pytest.mark.parametrize(
    'integers, page_number, page_size, expected_is_first_page, expected_is_last_page', [
        ([1, 2, 3], 1, 1, True, False),
        ([1, 2, 3], 2, 1, False, False),
        ([1, 2, 3], 3, 1, False, True),
    ])
def test_is_first_page_and_is_last_page_are_correct(
        integers, page_number, page_size, expected_is_first_page,
        expected_is_last_page):
    paged_list = SimplePagedList(integers, page_number, page_size)
    assert paged_list.is_first_page == expected_is_first_page
    assert paged_list.is_last_page == expected_is_last_page


@pytest.mark.parametrize(
    'integers, page_size, expected_number_of_pages', [
        ([1, 2, 3], 1, 3),
        ([1, 2, 3], 3, 1),
        ([1], 1, 1),
        ([1, 2, 3], 2, 2),
        ([1, 2, 3, 4], 2, 2),
        ([1, 2, 3, 4, 5], 2, 3),
    ])
def test_page_count_is_correct(integers, page_size, expected_number_of_pages):
    paged_list = SimplePagedList(integers, 1, page_size)
    assert paged_list.page_count == expected_number_of_pages
