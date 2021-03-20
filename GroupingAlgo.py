import numpy as np
import OverlapAlgo
import ClassMap
import ResolveAlgo

KEY_BOXES = "detection_boxes"
KEY_CLASSES = "detection_classes"
KEY_SCORES = "detection_scores"
KEY_CLASS_NAMES = "detection_class_names"
KEY_BOX_AREAS = "detection_box_areas"
KEY_CLASSES_COUNT = "classes_count"
ROOT_ID = "root"
APPBAR_ID = "appBar"
BOTTOMNAV_ID = "bottomNavigation"
CONTENT_ID = "layoutContent"


def test_algo(detections):
    ResolveAlgo.resolve_appbar(detections)
    ResolveAlgo.resolve_overlaping_layouts(detections)
    ResolveAlgo.resolve_icon_and_bottomnav(detections)


def resolve_all(detections):
    ResolveAlgo.resolve_appbar(detections)
    ResolveAlgo.resolve_overlaping_layouts(detections)
    ResolveAlgo.resolve_icon_and_bottomnav(detections)


def group_all(detections, ui_dict, class_by_no):
    if (
        APPBAR_ID in ui_dict and BOTTOMNAV_ID in ui_dict
    ):  # check if Appbar and BottomNav available
        print("AppBar and BottomNav both available")
        group_appbar_bottomnav(detections, ui_dict)
        prepare_widgets_for_container(ui_dict[APPBAR_ID], class_by_no)
        prepare_widgets_for_container(ui_dict[CONTENT_ID], class_by_no)
        prepare_widgets_for_container(ui_dict[BOTTOMNAV_ID], class_by_no)

    elif APPBAR_ID in ui_dict:  # Check if only Appbar available
        print("Only AppBar available")
        group_only_appbar(detections, ui_dict)
        prepare_widgets_for_container(ui_dict[APPBAR_ID], class_by_no)
        prepare_widgets_for_container(ui_dict[CONTENT_ID], class_by_no)

    elif BOTTOMNAV_ID in ui_dict:  # Check if only bottom nav available
        print("Only BottomNav available")
        group_only_bottomnav(detections, ui_dict)
        prepare_widgets_for_container(ui_dict[CONTENT_ID], class_by_no)
        prepare_widgets_for_container(ui_dict[BOTTOMNAV_ID], class_by_no)

    else:  # Else only root available
        print("Only root available")
        group_only_content(detections, ui_dict)
        prepare_widgets_for_container(ui_dict[CONTENT_ID], class_by_no)


def group_and_resolve(detections, ui_dict, class_by_no):
    extract_main_layout(detections, ui_dict)
    create_content_box(ui_dict)
    resolve_all(detections)
    group_all(detections, ui_dict, class_by_no)
    layout_grouping(ui_dict[CONTENT_ID]["content"])


def convert_list_to_nparray(container_dict):
    container_dict[KEY_BOXES] = np.array(container_dict[KEY_BOXES])
    container_dict[KEY_SCORES] = np.array(container_dict[KEY_SCORES])
    container_dict[KEY_CLASSES] = np.array(container_dict[KEY_CLASSES])


def prepare_widget_dict(widget_id, class_no, box, score):
    widget_dict = dict()
    widget_dict["id"] = widget_id
    widget_dict["class"] = class_no
    widget_dict["box"] = box
    widget_dict["score"] = score
    return widget_dict


def prepare_widgets_for_container(container_dict, class_by_no):
    container_copy = container_dict.copy()
    parent_id = container_dict["id"]
    widget_id_format = "{parentID}_{className}{no}"
    count = dict()
    container_dict["content"] = dict()

    for index, class_no in enumerate(container_copy[KEY_CLASSES]):
        box = container_copy[KEY_BOXES][index]
        score = container_copy[KEY_SCORES][index]

        # Check for Widget counts saved
        if class_no in count:
            count[class_no] = count[class_no] + 1
        else:
            count[class_no] = 1

        widget_id = widget_id_format.format(
            parentID=parent_id,
            className=class_by_no[class_no]["name"],
            no=count[class_no],
        )
        container_dict["content"][widget_id] = prepare_widget_dict(
            widget_id, class_no, box, score
        )


def extract_main_layout(detections, ui_dict):

    # copy filtered detections dict
    copy_of_detection = detections.copy()
    # Create filter for detections
    filter_extract = np.full((len(copy_of_detection[KEY_CLASSES])), True)

    for index, class_no in enumerate(copy_of_detection[KEY_CLASSES]):
        if class_no == 26:
            # It is main Layout
            root_dict = dict()
            root_dict["id"] = ROOT_ID
            root_dict["class"] = class_no
            root_dict["box"] = copy_of_detection[KEY_BOXES][index]
            root_dict["score"] = copy_of_detection[KEY_SCORES][index]
            root_dict["content"] = dict()
            # Adding root to UI dictionary
            ui_dict[ROOT_ID] = root_dict
            # Delete Main Layout from detections
            filter_extract[index] = False

        elif class_no == 7:
            # It is AppBar
            appbar_dict = dict()
            appbar_dict["id"] = APPBAR_ID
            appbar_dict["class"] = class_no
            appbar_dict["box"] = copy_of_detection[KEY_BOXES][index]
            appbar_dict["score"] = copy_of_detection[KEY_SCORES][index]
            appbar_dict["content"] = dict()
            appbar_dict[KEY_BOXES] = list()
            appbar_dict[KEY_SCORES] = list()
            appbar_dict[KEY_CLASSES] = list()
            ui_dict[APPBAR_ID] = appbar_dict
            # Delete AppBar from detections
            filter_extract[index] = False

        elif class_no == 19:
            # It is BottomNavBar
            bottomnavbar_dict = dict()
            bottomnavbar_dict["id"] = BOTTOMNAV_ID
            bottomnavbar_dict["class"] = class_no
            bottomnavbar_dict["box"] = copy_of_detection[KEY_BOXES][index]
            bottomnavbar_dict["score"] = copy_of_detection[KEY_SCORES][index]
            bottomnavbar_dict["content"] = dict()
            bottomnavbar_dict[KEY_BOXES] = list()
            bottomnavbar_dict[KEY_SCORES] = list()
            bottomnavbar_dict[KEY_CLASSES] = list()
            ui_dict[BOTTOMNAV_ID] = bottomnavbar_dict
            # Delete BottomNavBar from detections
            filter_extract[index] = False

    # Change detection dict
    detections[KEY_CLASSES] = detections[KEY_CLASSES][filter_extract]
    detections[KEY_SCORES] = detections[KEY_SCORES][filter_extract]
    detections[KEY_BOXES] = detections[KEY_BOXES][filter_extract]


def group_appbar_bottomnav(detections, ui_dict):
    detections_copy = detections.copy()
    content_box = ui_dict[CONTENT_ID]["box"]
    appbar_box = ui_dict[APPBAR_ID]["box"]
    bottomnav_box = ui_dict[BOTTOMNAV_ID]["box"]

    for index, class_no in enumerate(detections_copy[KEY_CLASSES]):
        # get box of component
        box = detections_copy[KEY_BOXES][index]
        score = detections_copy[KEY_SCORES][index]

        if OverlapAlgo.is_inside_by_full_overlap(
            content_box, box
        ) or OverlapAlgo.is_inside_by_partial_overlap(
            content_box, box
        ):  # Check box is inside content
            trimed_box = OverlapAlgo.trim_inside_stable_box(content_box, box)
            add_widget_to_container(
                container_dict=ui_dict[CONTENT_ID],
                box=trimed_box,
                score=score,
                class_no=class_no,
            )

        elif OverlapAlgo.is_inside_by_full_overlap(
            appbar_box, box
        ) or OverlapAlgo.is_inside_by_partial_overlap(
            appbar_box, box
        ):  # Check box inside app bar
            trimed_box = OverlapAlgo.trim_inside_stable_box(appbar_box, box)
            add_widget_to_container(
                container_dict=ui_dict[APPBAR_ID],
                box=trimed_box,
                score=score,
                class_no=class_no,
            )

        elif OverlapAlgo.is_inside_by_full_overlap(
            bottomnav_box, box
        ) or OverlapAlgo.is_inside_by_partial_overlap(
            bottomnav_box, box
        ):  # Check box inside bottom Navbar
            trimed_box = OverlapAlgo.trim_inside_stable_box(bottomnav_box, box)
            add_widget_to_container(
                container_dict=ui_dict[BOTTOMNAV_ID],
                box=trimed_box,
                score=score,
                class_no=class_no,
            )


def group_only_appbar(detections, ui_dict):
    detections_copy = detections.copy()
    content_box = ui_dict[CONTENT_ID]["box"]
    appbar_box = ui_dict[APPBAR_ID]["box"]

    for index, class_no in enumerate(detections_copy[KEY_CLASSES]):
        # get box of component
        box = detections_copy[KEY_BOXES][index]
        score = detections_copy[KEY_SCORES][index]

        if OverlapAlgo.is_inside_by_full_overlap(
            content_box, box
        ) or OverlapAlgo.is_inside_by_partial_overlap(
            content_box, box
        ):  # Check box is inside content
            trimed_box = OverlapAlgo.trim_inside_stable_box(content_box, box)
            add_widget_to_container(
                container_dict=ui_dict[CONTENT_ID],
                box=trimed_box,
                score=score,
                class_no=class_no,
            )

        elif OverlapAlgo.is_inside_by_full_overlap(
            appbar_box, box
        ) or OverlapAlgo.is_inside_by_partial_overlap(
            appbar_box, box
        ):  # Check box inside app bar
            trimed_box = OverlapAlgo.trim_inside_stable_box(appbar_box, box)
            add_widget_to_container(
                container_dict=ui_dict[APPBAR_ID],
                box=trimed_box,
                score=score,
                class_no=class_no,
            )


def group_only_bottomnav(detections, ui_dict):
    detections_copy = detections.copy()
    content_box = ui_dict[CONTENT_ID]["box"]
    bottomnav_box = ui_dict[BOTTOMNAV_ID]["box"]

    for index, class_no in enumerate(detections_copy[KEY_CLASSES]):
        # get box of component
        box = detections_copy[KEY_BOXES][index]
        score = detections_copy[KEY_SCORES][index]

        if OverlapAlgo.is_inside_by_full_overlap(
            content_box, box
        ) or OverlapAlgo.is_inside_by_partial_overlap(
            content_box, box
        ):  # Check box is inside content
            trimed_box = OverlapAlgo.trim_inside_stable_box(content_box, box)
            add_widget_to_container(
                container_dict=ui_dict[CONTENT_ID],
                box=trimed_box,
                score=score,
                class_no=class_no,
            )

        elif OverlapAlgo.is_inside_by_full_overlap(
            bottomnav_box, box
        ) or OverlapAlgo.is_inside_by_partial_overlap(
            bottomnav_box, box
        ):  # Check box inside bottom Navbar
            trimed_box = OverlapAlgo.trim_inside_stable_box(bottomnav_box, box)
            add_widget_to_container(
                container_dict=ui_dict[BOTTOMNAV_ID],
                box=trimed_box,
                score=score,
                class_no=class_no,
            )


def group_only_content(detections, ui_dict):
    detections_copy = detections.copy()
    content_box = ui_dict[CONTENT_ID]["box"]

    for index, class_no in enumerate(detections_copy[KEY_CLASSES]):
        # get box of component
        box = detections_copy[KEY_BOXES][index]
        score = detections_copy[KEY_SCORES][index]
        if OverlapAlgo.is_inside_by_full_overlap(
            content_box, box
        ) or OverlapAlgo.is_inside_by_partial_overlap(
            content_box, box
        ):  # Check box is inside content
            trimed_box = OverlapAlgo.trim_inside_stable_box(content_box, box)
            add_widget_to_container(
                container_dict=ui_dict[CONTENT_ID],
                box=trimed_box,
                score=score,
                class_no=class_no,
            )


def add_widget_to_container(container_dict, box, score, class_no):
    if KEY_BOXES in container_dict:
        boxes_list = container_dict[KEY_BOXES]
        boxes_list.append(box)
    else:
        boxes_list = list()
        boxes_list.append(box)
        container_dict[KEY_BOXES] = boxes_list

    if KEY_SCORES in container_dict:
        scores_list = container_dict[KEY_SCORES]
        scores_list.append(score)
    else:
        scores_list = list()
        scores_list.append(score)
        container_dict[KEY_SCORES] = scores_list

    if KEY_CLASSES in container_dict:
        class_list = container_dict[KEY_CLASSES]
        class_list.append(class_no)
    else:
        class_list = list()
        class_list.append(class_no)
        container_dict[KEY_CLASSES] = class_list


def create_content_box(ui_dict):
    if ROOT_ID in ui_dict:
        ymin, xmin, ymax, xmax = ui_dict[ROOT_ID]["box"]
        if APPBAR_ID in ui_dict:
            yomin, xomin, yomax, xomax = ui_dict[APPBAR_ID]["box"]
            ymin = yomax

        if BOTTOMNAV_ID in ui_dict:
            yomin, xomin, yomax, xomax = ui_dict[BOTTOMNAV_ID]["box"]
            ymax = yomin

        ui_dict[CONTENT_ID] = dict()
        ui_dict[CONTENT_ID]["id"] = CONTENT_ID
        ui_dict[CONTENT_ID]["box"] = np.array([ymin, xmin, ymax, xmax])
        ui_dict[CONTENT_ID]["content"] = dict()
    else:
        print("No root key in ui_dict")


# Grouping
def group_components_appbar_bottomnav(detections, ui_dict):
    detections_copy = detections.copy()
    root_box = ui_dict[ROOT_ID]["box"]
    appbar_box = ui_dict[APPBAR_ID]["box"]
    bottomnav_box = ui_dict[BOTTOMNAV_ID]["box"]

    for index, class_no in enumerate(detections_copy[KEY_CLASSES]):
        # Check for Widget counts saved
        if class_no in ui_dict[KEY_CLASSES_COUNT]:
            ui_dict[KEY_CLASSES_COUNT][class_no] = (
                ui_dict[KEY_CLASSES_COUNT][class_no] + 1
            )
        else:
            ui_dict[KEY_CLASSES_COUNT][class_no] = 1

        # get box of component
        box = detections_copy[KEY_BOXES][index]
        score = detections_copy[KEY_SCORES][index]
        widget_id = ClassMap.get_name_for_class(class_no) + str(
            ui_dict[KEY_CLASSES_COUNT][class_no]
        )

        # Check box is inside root
        if OverlapAlgo.is_inside_by_full_overlap(
            root_box, box
        ) or OverlapAlgo.is_inside_by_partial_overlap(root_box, box):
            root_trimed_box = OverlapAlgo.trim_inside_stable_box(root_box, box)
            # Check box inside app bar
            if OverlapAlgo.is_inside_by_full_overlap(
                appbar_box, root_trimed_box
            ) or OverlapAlgo.is_inside_by_partial_overlap(appbar_box, root_trimed_box):
                trimed_box = OverlapAlgo.trim_inside_stable_box(
                    appbar_box, root_trimed_box
                )
                ui_dict[APPBAR_ID]["content"][widget_id] = prepare_widget_dict(
                    widget_id, class_no, trimed_box, score
                )

            # Check box inside BottomNav bar
            elif OverlapAlgo.is_inside_by_full_overlap(
                bottomnav_box, root_trimed_box
            ) or OverlapAlgo.is_inside_by_partial_overlap(
                bottomnav_box, root_trimed_box
            ):
                trimed_box = OverlapAlgo.trim_inside_stable_box(
                    bottomnav_box, root_trimed_box
                )
                ui_dict[BOTTOMNAV_ID]["content"][widget_id] = prepare_widget_dict(
                    widget_id, class_no, trimed_box, score
                )
            # add box inside content
            else:
                ui_dict[ROOT_ID]["content"][widget_id] = prepare_widget_dict(
                    widget_id, class_no, root_trimed_box, score
                )
        else:
            print("component outside root")


def group_components_only_bottomnav(detections, ui_dict):
    detections_copy = detections.copy()
    root_box = ui_dict[ROOT_ID]["box"]
    bottomnav_box = ui_dict[BOTTOMNAV_ID]["box"]
    for index, class_no in enumerate(detections_copy[KEY_CLASSES]):
        # Check for Widget counts saved
        if class_no in ui_dict[KEY_CLASSES_COUNT]:
            ui_dict[KEY_CLASSES_COUNT][class_no] = (
                ui_dict[KEY_CLASSES_COUNT][class_no] + 1
            )
        else:
            ui_dict[KEY_CLASSES_COUNT][class_no] = 1
        # get box of component
        box = change_box(detections_copy[KEY_BOXES][index])
        score = detections_copy[KEY_SCORES][index]
        widget_id = category_index[class_no]["name"] + str(
            ui_dict[KEY_CLASSES_COUNT][class_no]
        )

        # Check box is inside root
        if OverlapAlgo.is_inside_by_full_overlap(
            root_box, box
        ) or OverlapAlgo.is_inside_by_partial_overlap(root_box, box):
            root_trimed_box = OverlapAlgo.trim_inside_stable_box(root_box, box)

            # Check box inside BottomNav bar
            if OverlapAlgo.is_inside_by_full_overlap(
                bottomnav_box, root_trimed_box
            ) or OverlapAlgo.is_inside_by_partial_overlap(
                bottomnav_box, root_trimed_box
            ):
                trimed_box = OverlapAlgo.trim_inside_stable_box(
                    bottomnav_box, root_trimed_box
                )
                ui_dict[BOTTOMNAV_ID]["content"][widget_id] = prepare_widget_dict(
                    widget_id, class_no, trimed_box, score
                )
            # add box inside content
            else:
                ui_dict[ROOT_ID]["content"][widget_id] = prepare_widget_dict(
                    widget_id, class_no, root_trimed_box, score
                )
        else:
            print("component outside root")


def group_components_only_appbar(detections, ui_dict):
    detections_copy = detections.copy()
    root_box = ui_dict[ROOT_ID]["box"]
    appbar_box = ui_dict[APPBAR_ID]["box"]
    for index, class_no in enumerate(detections_copy[KEY_CLASSES]):
        # Check for Widget counts saved
        if class_no in ui_dict[KEY_CLASSES_COUNT]:
            ui_dict[KEY_CLASSES_COUNT][class_no] = (
                ui_dict[KEY_CLASSES_COUNT][class_no] + 1
            )
        else:
            ui_dict[KEY_CLASSES_COUNT][class_no] = 1
        # get box of component
        box = change_box(detections_copy[KEY_BOXES][index])
        score = detections_copy[KEY_SCORES][index]
        widget_id = category_index[class_no]["name"] + str(
            ui_dict[KEY_CLASSES_COUNT][class_no]
        )

        # Check box is inside root
        if OverlapAlgo.is_inside_by_full_overlap(
            root_box, box
        ) or OverlapAlgo.is_inside_by_partial_overlap(root_box, box):
            root_trimed_box = OverlapAlgo.trim_inside_stable_box(root_box, box)
            # Check box inside app bar
            if OverlapAlgo.is_inside_by_full_overlap(
                appbar_box, root_trimed_box
            ) or OverlapAlgo.is_inside_by_partial_overlap(appbar_box, root_trimed_box):
                trimed_box = OverlapAlgo.trim_inside_stable_box(
                    appbar_box, root_trimed_box
                )
                ui_dict[APPBAR_ID]["content"][widget_id] = prepare_widget_dict(
                    widget_id, class_no, trimed_box, score
                )
            # add box inside content
            else:
                ui_dict[ROOT_ID]["content"][widget_id] = prepare_widget_dict(
                    widget_id, class_no, root_trimed_box, score
                )
        else:
            print("component outside root")


def group_components_only_root(detections, ui_dict):
    detections_copy = detections.copy()
    root_box = ui_dict[ROOT_ID]["box"]
    for index, class_no in enumerate(detections_copy[KEY_CLASSES]):
        # Check for Widget counts saved
        if class_no in ui_dict[KEY_CLASSES_COUNT]:
            ui_dict[KEY_CLASSES_COUNT][class_no] = (
                ui_dict[KEY_CLASSES_COUNT][class_no] + 1
            )
        else:
            ui_dict[KEY_CLASSES_COUNT][class_no] = 1
        # get box of component
        box = change_box(detections_copy[KEY_BOXES][index])
        score = detections_copy[KEY_SCORES][index]
        widget_id = category_index[class_no]["name"] + str(
            ui_dict[KEY_CLASSES_COUNT][class_no]
        )

        # Check box is inside root
        if OverlapAlgo.is_inside_by_full_overlap(
            root_box, box
        ) or OverlapAlgo.is_inside_by_partial_overlap(root_box, box):
            trimed_box = OverlapAlgo.trim_inside_stable_box(root_box, box)
            ui_dict[ROOT_ID]["content"][widget_id] = prepare_widget_dict(
                widget_id, class_no, trimed_box, score
            )
        else:
            print("component outside root")


# Loop through detections other than MainLayout(root), AppBar, BottomNavBar
def group_gui_components_into_root_appbar_bottomnav(detections, ui_dict):
    if ROOT_ID in ui_dict:
        ui_dict[CONTENT_ID] = dict()

        if (
            APPBAR_ID in ui_dict and BOTTOMNAV_ID in ui_dict
        ):  # check if Appbar and BottomNav available
            print("AppBar and BottomNav both available")
            group_components_appbar_bottomnav(detections, ui_dict)

        elif APPBAR_ID in ui_dict:  # Check if only Appbar available
            print("Only AppBar available")
            group_components_only_appbar(detections, ui_dict)

        elif BOTTOMNAV_ID in ui_dict:  # Check if only bottom nav available
            print("Only BottomNav available")
            group_components_only_bottomnav(detections, ui_dict)

        else:  # Else only root available
            print("Only root available")
            group_components_only_root(detections, ui_dict)
    else:
        print("No root key in ui_dict")


def group_contents(content_dict):
    pass


def group_layouts():
    pass


def group_cardview():
    pass


def layout_grouping(content_dict):
    content_copy = content_dict.copy()
    layouts = list()
    cardviews = list()
    other_widgets = list()

    # Extract Layouts from content
    for widget_id in content_copy:
        if content_copy[widget_id]["class"] == 24:
            layouts.append(widget_id)
        elif content_copy[widget_id]["class"] == 13:
            cardviews.append(widget_id)
        else:
            other_widgets.append(widget_id)

    if len(layouts) < 1 and len(cardviews) < 1:
        return

    # resolve layout and cardview
    for layout_id in layouts:
        if len(cardviews) < 1:
            break
        layout_box = content_copy[layout_id]["box"]
        ids_to_remove = list()  # Cardview ids to be removed
        for cardview_id in cardviews:
            cardview_box = content_copy[cardview_id]["box"]
            if (
                OverlapAlgo.is_inside_by_full_overlap(layout_box, cardview_box)
                or OverlapAlgo.is_inside_by_partial_overlap(layout_box, cardview_box)
                or check_if_box_cover(layout_box, cardview_box)
            ):
                content_dict[layout_id]["alt"] = ["CardView"]
                content_dict.pop(cardview_id)
                ids_to_remove.append(cardview_id)
        for id_to_remove in ids_to_remove:
            cardviews.remove(id_to_remove)

    # Merge Cardview and Layout
    layouts.extend(cardviews)

    # Group Layouts
    for layout_id in layouts:
        if len(other_widgets) < 1:
            break
        content_dict[layout_id]["content"] = dict()
        layout_box = content_copy[layout_id]["box"]
        ids_to_remove = list()  # other widget Id's to be removed
        for widget_id in other_widgets:
            widget_box = content_copy[widget_id]["box"]
            if OverlapAlgo.is_inside_by_full_overlap(
                layout_box, widget_box
            ) or OverlapAlgo.is_inside_by_partial_overlap(layout_box, widget_box):
                content_dict[layout_id]["content"][widget_id] = content_dict[widget_id]
                content_dict.pop(widget_id)
                ids_to_remove.append(widget_id)
        for id_to_remove in ids_to_remove:
            other_widgets.remove(id_to_remove)


def cardview_grouping():
    pass


def tab_grouping():
    pass


def listview_grouping(content_dict):
    content_copy = content_dict.copy()
    listviews = list()
    h_list = list()
    v_list = list()
    layouts = list()
    recycler = list()

    # Resolve ListView, horizontal and vertical list view as Recycler view
    for widget_id in content_copy:
        if content_copy[widget_id]["class"] == 14:
            listviews.append(widget_id)
        elif content_copy[widget_id]["class"] == 27:
            h_list.append(widget_id)
        elif content_copy[widget_id]["class"] == 28:
            v_list.append(widget_id)
        elif content_copy[widget_id]["class"] == 24:
            layouts.append(widget_id)
        elif (
            content_copy[widget_id]["class"] == 13
        ):  # change made for cardview grouping
            layouts.append(widget_id)

    # Resolve for Horizontal listview
    for hlist_id in h_list:
        # If no listviews box break the loop
        if len(listviews) < 1:
            break
        hlist_box = content_copy[hlist_id]["box"]
        ids_to_remove = list()  # Listview ids to be removed

        # Loop through listviews list()
        for listview_id in listviews:
            listview_box = content_copy[listview_id]["box"]
            if (
                OverlapAlgo.is_inside_by_full_overlap(hlist_box, listview_box)
                or OverlapAlgo.is_inside_by_partial_overlap(hlist_box, listview_box)
                or check_if_box_cover(hlist_box, listview_box)
            ):
                recycler.append(hlist_id)  # add horizontal list view id
                content_dict.pop(listview_id)  # remove listview from dictionary
                ids_to_remove.append(listview_id)
        for id_to_remove in ids_to_remove:
            listviews.remove(id_to_remove)

    # Resolve for Vertical listview
    for vlist_id in v_list:
        # If no listviews box break the loop
        if len(listviews) < 1:
            break
        vlist_box = content_copy[vlist_id]["box"]
        ids_to_remove = list()  # Listview ids to be removed

        # Loop through listviews list()
        for listview_id in listviews:
            listview_box = content_copy[listview_id]["box"]
            if (
                OverlapAlgo.is_inside_by_full_overlap(vlist_box, listview_box)
                or OverlapAlgo.is_inside_by_partial_overlap(vlist_box, listview_box)
                or check_if_box_cover(vlist_box, listview_box)
            ):
                recycler.append(vlist_id)  # add horizontal list view id
                content_dict.pop(listview_id)  # remove listview from dictionary
                ids_to_remove.append(listview_id)
        for id_to_remove in ids_to_remove:
            listviews.remove(id_to_remove)

    # check if recycler list is not empty
    if len(recycler) < 1:
        print("No List views")
    else:
        listview_name = "ListView"
        for index, list_id in enumerate(recycler):
            list_key = listview_name + str(index + 1)
            content_dict[list_key] = dict()
            content_dict[list_key]["id"] = list_key
            content_dict[list_key]["class"] = 14
            content_dict[list_key]["box"] = content_dict[list_id]["box"]
            content_dict[list_key]["score"] = content_dict[list_id]["score"]
            content_dict[list_key]["content"] = dict()
            # Orientation Horizontal = 0 ,Vertical = 1
            if content_copy[list_id]["class"] == 27:
                content_dict[list_key]["orientation"] = 0
            elif content_copy[list_id]["class"] == 28:
                content_dict[list_key]["orientation"] = 1
            else:
                content_dict[list_key]["orientation"] = 1

            # remove listview from content dict
            content_dict.pop(list_id)

            listview_box = content_dict[list_key]["box"]
            ids_to_remove = list()  # other widget Id's to be removed
            # Group Layouts inside list dict
            for layout_id in layouts:
                layout_box = content_copy[layout_id]["box"]
                if OverlapAlgo.is_inside_by_full_overlap(
                    listview_box, layout_box
                ) or OverlapAlgo.is_inside_by_partial_overlap(listview_box, layout_box):
                    content_dict[list_key]["content"][layout_id] = content_dict[
                        layout_id
                    ]
                    content_dict[list_key]["content"][layout_id][
                        "box"
                    ] = trim_inside_stable_box(listview_box, layout_box)
                    content_dict.pop(layout_id)
                    ids_to_remove.append(layout_id)
            for id_to_remove in ids_to_remove:
                layouts.remove(id_to_remove)


def radio_grouping():
    pass


def appbar_grouping():
    pass


def print_test():
    print("HI ")