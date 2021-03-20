import numpy as np


def sort_horizontal_by_distance(horizontal_list):
    # Traverse through 1 to len(arr)
    for i in range(1, len(horizontal_list)):
        widget = horizontal_list[i]
        distance = widget["dist"]
        # Move elements of arr[0..i-1], that are
        # greater than key, to one position ahead
        # of their current position
        j = i - 1
        while j >= 0 and distance < horizontal_list[j]["dist"]:
            horizontal_list[j + 1] = horizontal_list[j]
            j -= 1
        horizontal_list[j + 1] = widget


def position_widgets_inside_container(container_dict):
    levels = list()
    container_copy = container_dict.copy()
    container_content = container_copy["content"]

    ypmin, xpmin, ypmax, xpmax = container_copy["box"]

    for widget_id in container_content:
        top, start, bottom, end = container_content[widget_id]["box"]
        distance_from_parent = start - xpmin
        level_widget_item = {"id": widget_id, "dist": distance_from_parent}

        if len(levels) == 0:
            level_dict = dict()
            level_dict["lmin"] = top
            level_dict["lmax"] = bottom
            level_dict["widgets"] = [{"id": widget_id, "dist": distance_from_parent}]
            levels.append(level_dict)
            continue

        loop_level = levels.copy()
        # Loop through level
        for index, level in enumerate(loop_level):
            lmin = level["lmin"]
            lmax = level["lmax"]

            if top >= lmax:  # check widget below the level
                if index + 1 < len(loop_level):  # check if a level available below this
                    # Go to next level that mean continue
                    continue
                else:  # No level below this, this last level so create a new level below this append level
                    level_dict = dict()
                    level_dict["lmin"] = top
                    level_dict["lmax"] = bottom
                    level_dict["widgets"] = [
                        {"id": widget_id, "dist": distance_from_parent}
                    ]
                    levels.append(level_dict)
                    break  # widget added to the level so go for next widget

            elif lmin >= bottom:  # check widget above the level
                # If widget is above the level then need to create new level above this level and below before this level
                level_dict = dict()
                level_dict["lmin"] = top
                level_dict["lmax"] = bottom
                level_dict["widgets"] = [
                    {"id": widget_id, "dist": distance_from_parent}
                ]
                levels.insert(index, level_dict)
                break  # widget added to the level so go for next widget
            elif lmin <= top < bottom <= lmax:  # check widget inside level
                level_widgets = levels[index]["widgets"]
                level_widgets.append({"id": widget_id, "dist": distance_from_parent})
                break  # widget added to the level so go for next widget
            elif top < lmin < lmax < bottom:  # level is inside widget
                # If level inside widget then expand level to the widget and add widget
                levels[index]["lmin"] = top
                levels[index]["lmax"] = bottom
                level_widgets = levels[index]["widgets"]
                level_widgets.append({"id": widget_id, "dist": distance_from_parent})
                break  # widget added to the level so go for next widget
            elif top < lmin < bottom < lmax:  # Partial scenario 1 : bottom inside level
                interaction = bottom - lmin / bottom - top
                # if the widgets height interaction is greater than 0.5 or 0.55
                if interaction > 0.5:
                    if (
                        bottom - top > lmax - lmin
                    ):  # if height of widget is greater than level height then move and expand
                        # Move down inside level
                        height = bottom - top
                        top = lmin
                        bottom = lmin + height
                        # expand
                        # Add to the level
                        level_widgets = levels[index]["widgets"]
                        level_widgets.append(level_widget_item)
                        break  # widget added to the level so go for next widget

                    else:  # Else just move widget inside the level and add to the level
                        # Move down inside level
                        height = bottom - top
                        top = lmin
                        bottom = lmin + height
                        # Add to the level
                        level_widgets = levels[index]["widgets"]
                        level_widgets.append(level_widget_item)
                        break  # widget added to the level so go for next widget

                else:  # Else move outside above the current level and create a new level
                    height = bottom - top
                    bottom = lmin
                    top = lmin - height

                    level_dict = dict()
                    level_dict["lmin"] = top
                    level_dict["lmax"] = bottom
                    level_dict["widgets"] = [
                        {"id": widget_id, "dist": distance_from_parent}
                    ]
                    levels.insert(index, level_dict)
                    break  # widget added to the level so go for next widget

            elif lmin < top < lmax < bottom:  # Partial scenario 2 : top inside level
                interaction = lmax - top / bottom - top
                # if the widgets height interaction is greater than 0.5 or 0.55
                if interaction > 0.5:

                    if (
                        bottom - top > lmax - lmin
                    ):  # if height of widget is greater than level height then move and expand
                        # Move down inside level
                        height = bottom - top
                        bottom = lmax
                        top = lmax - height
                        # expand
                        # Add to the level
                        level_widgets = levels[index]["widgets"]
                        level_widgets.append(level_widget_item)
                        break  # widget added to the level so go for next widget

                    else:  # Else just move widget inside the level
                        level_widgets = levels[index]["widgets"]
                        level_widgets.append(level_widget_item)
                        break  # widget added to the level so go for next widget

                else:  # Else move outside down and check for next level
                    height = bottom - top
                    top = lmax
                    bottom = lmax + height

                    if index + 1 < len(
                        loop_level
                    ):  # If next level available go to next level
                        # Go to next level that mean continue
                        continue
                    else:  # else if it is last level then create new level below it
                        level_dict = dict()
                        level_dict["lmin"] = top
                        level_dict["lmax"] = bottom
                        level_dict["widgets"] = [
                            {"id": widget_id, "dist": distance_from_parent}
                        ]
                        levels.append(level_dict)
                        break  # widget added to the level so go for next widget

    print("Levels length : " + str(len(levels)))
    for i in range(len(levels)):
        print(levels[i])

    for i in range(len(levels)):
        sort_horizontal_by_distance(levels[i]["widgets"])
    print("After sorting")
    for i in range(len(levels)):
        print(levels[i])

    print("\nContainer\n")
    print(container_dict["content"])

    return levels


def start_structuring():
    pass


# level format {'lmin': 207, 'lmax': 312, 'widgets': [{'id': 'CardView2', 'dist': 21}]}
def set_positions_for_container(container_dict):
    container_content = container_dict["content"]
    levels = position_widgets_inside_container(container_dict)
    no_of_levels = len(levels)
    print("No oflevels " + str(no_of_levels))
    for level_no in range(len(levels)):
        level = levels[level_no]  # get the level to arrange widgets in level
        widgets_in_level = level["widgets"]

        for widget_position in range(
            len(widgets_in_level)
        ):  # Loop throught widgets to position
            # get widget
            widget = widgets_in_level[widget_position]
            widget_id = widget["id"]
            # check if it is the 1st level then top to top of parent
            if (
                widget_position == 0 and level_no == 0
            ):  # It is first level and first widget
                container_content[widget_id]["position"] = dict()
                container_content[widget_id]["position"]["top"] = "parent"
                container_content[widget_id]["position"]["start"] = "parent"
                if level_no == no_of_levels - 1:  # Only one level in container
                    container_content[widget_id]["position"]["bottom"] = "parent"
            elif (
                widget_position == 0
            ):  # It is not first level but it is first widget in the level
                container_content[widget_id]["position"] = dict()
                container_content[widget_id]["position"]["top"] = levels[level_no - 1][
                    "widgets"
                ][0]["id"]
                container_content[widget_id]["position"]["start"] = "parent"
                # check if this is last level first widget
                if level_no == no_of_levels - 1:  # It is first widget of last level
                    container_content[widget_id]["position"]["bottom"] = "parent"
            else:  # It may be widget after first widget
                container_content[widget_id]["position"] = dict()
                # container_content[widget_id]['position']['top'] = levels[level_no-1]['widgets'][0]['id']
                container_content[widget_id]["position"]["start"] = widgets_in_level[
                    widget_position - 1
                ]["id"]
                # check if it is last widget in a level
                if (
                    widget_position == len(widgets_in_level) - 1
                ):  # it is last widget in level so end is connected with parent
                    container_content[widget_id]["position"]["end"] = "parent"

    print("\nCurrent container postions \n")
    print(container_dict)


def structure_and_position_listview(listview_dict):
    pass
