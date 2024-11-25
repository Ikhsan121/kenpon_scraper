def jaccard_similarity(str1, str2):
    set1 = set(str1)
    set2 = set(str2)
    intersection = len(set1.intersection(set2))
    union = len(set1.union(set2))
    return intersection / union


def similarity_test(arena_dict, team_arena_dict):
    similarity_list = []
    for i in arena_dict:
        for j in team_arena_dict:
            if i == j:
                filtered_arena = [x for x in arena_dict[j] if x != '']
                for k in filtered_arena:
                    similarity = float(jaccard_similarity(k,
                                                    team_arena_dict[j]))
                    if similarity > 0.68:
                        similarity_list.append(similarity)
                    else:
                        similarity_list.append(0)
            else:
                similarity_list.append(0)
    return max(similarity_list)

def similiarity_test_json(arena_json, team_city_arena):
    similarity_list = []
    for i in arena_json:
        for j in team_city_arena:
            if i == j and arena_json[i][1] == team_city_arena[j][1]:
                similarity = jaccard_similarity(arena_json[i][0],
                                                team_city_arena[j][0])
                similarity_list.append(similarity)
            else:
                similarity_list.append(0)

    return max(similarity_list)
