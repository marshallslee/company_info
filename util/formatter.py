from collections import defaultdict


def format_company_search_result(query_result):
    res = defaultdict(list)
    for x in query_result:
        res[x[0]].append(x[1:])

    result = {'companies_list': [{'company_group_id': x, 'name': dict(res[x])} for x in res]}
    return result
