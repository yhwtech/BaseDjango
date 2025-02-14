def calc_range_pages(current_page, size_page, pages):
    start_range = max(0, current_page - 2)
    end_range = min(start_range + size_page, pages)

    if end_range - start_range < size_page:
        start_range = max(0, end_range - size_page)

    return range(start_range, end_range)
