from MobileKG.SearchKG.operation.NextStep import NextStep

def next_step(picture, split_dic, components, last_component_id=None, search_all=False):
    next_step = NextStep(picture, split_dic)
    if search_all or last_component_id is None:
        result = next_step.search_all(components)
    else:
        result = next_step.search_with_head(components, last_component_id)
    return result
