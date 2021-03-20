import OverlapAlgo
import numpy as np

KEY_BOXES = "detection_boxes"
KEY_CLASSES = "detection_classes"
KEY_SCORES = "detection_scores"


def resolve_overlaping_layouts(detections):
    copy_of_detections = detections.copy()
    # Create filter for detections
    filter_extract = np.full((len(copy_of_detections[KEY_CLASSES])), True)

    for index, class_no in enumerate(copy_of_detections[KEY_CLASSES]):
        score = copy_of_detections[KEY_SCORES][index]
        box = copy_of_detections[KEY_BOXES][index]
        if class_no == 24:  # If it is layout

            for index_child, class_no_child in enumerate(
                copy_of_detections[KEY_CLASSES]
            ):
                score_child = copy_of_detections[KEY_SCORES][index_child]
                box_child = copy_of_detections[KEY_BOXES][index_child]

                if class_no_child == 24:  # If it is layout
                    if OverlapAlgo.is_inside_by_full_overlap(
                        box, box_child
                    ) or OverlapAlgo.is_inside_by_partial_overlap(box, box_child):
                        if score > score_child:
                            filter_extract[index_child] = False
                        else:
                            filter_extract[index] = False

    # Change detection dict
    detections[KEY_CLASSES] = detections[KEY_CLASSES][filter_extract]
    detections[KEY_SCORES] = detections[KEY_SCORES][filter_extract]
    detections[KEY_BOXES] = detections[KEY_BOXES][filter_extract]


def resolve_appbar(appbar_dict):
    resolve_icon_and_action_button(appbar_dict)


def resolve_icon_and_action_button(appbar_dict):
    copy_of_appbar = appbar_dict.copy()
    # Create filter for detections
    filter_extract = np.full((len(copy_of_appbar[KEY_CLASSES])), True)

    for index, class_no in enumerate(copy_of_appbar[KEY_CLASSES]):
        score = copy_of_appbar[KEY_SCORES][index]
        box = copy_of_appbar[KEY_BOXES][index]

        if class_no == 8:  # If it is action button
            for index_child, class_no_child in enumerate(copy_of_appbar[KEY_CLASSES]):
                if index != index_child:
                    score_child = copy_of_appbar[KEY_SCORES][index_child]
                    box_child = copy_of_appbar[KEY_BOXES][index_child]

                    if class_no_child == 8:
                        if OverlapAlgo.is_inside_by_full_overlap(
                            box, box_child
                        ) or OverlapAlgo.is_inside_by_partial_overlap(
                            box, box_child
                        ):  # actionButton actionButton overlap
                            if score > score_child:
                                filter_extract[index_child] = False
                            else:
                                filter_extract[index] = False

                    if class_no_child == 6:
                        if OverlapAlgo.is_inside_by_full_overlap(
                            box, box_child
                        ) or OverlapAlgo.is_inside_by_partial_overlap(
                            box, box_child
                        ):  # actionButton Icon overlap priority to action button
                            filter_extract[index_child] = False

                else:
                    continue

        if class_no == 6:  # If it is Icon
            for index_child, class_no_child in enumerate(copy_of_appbar[KEY_CLASSES]):
                if index != index_child:
                    score_child = copy_of_appbar[KEY_SCORES][index_child]
                    box_child = copy_of_appbar[KEY_BOXES][index_child]

                    if OverlapAlgo.is_inside_by_full_overlap(
                        box, box_child
                    ) or OverlapAlgo.is_inside_by_partial_overlap(box, box_child):
                        if (
                            class_no_child == 8
                        ):  # Action Button Icon Overlapped priority to action button
                            filter_extract[index] = False
                        if class_no_child == 6:  # Icon Overlaped
                            if score > score_child:
                                filter_extract[index_child] = False
                            else:
                                filter_extract[index] = False
                else:
                    continue

    # Change detection dict
    appbar_dict[KEY_CLASSES] = appbar_dict[KEY_CLASSES][filter_extract]
    appbar_dict[KEY_SCORES] = appbar_dict[KEY_SCORES][filter_extract]
    appbar_dict[KEY_BOXES] = appbar_dict[KEY_BOXES][filter_extract]


def resolve_icon_and_bottomnav(bottomnav_dict):
    copy_of_appbar = bottomnav_dict.copy()
    # Create filter for detections
    filter_extract = np.full((len(copy_of_appbar[KEY_CLASSES])), True)

    for index, class_no in enumerate(copy_of_appbar[KEY_CLASSES]):
        score = copy_of_appbar[KEY_SCORES][index]
        box = copy_of_appbar[KEY_BOXES][index]

        if class_no == 25:  # If it is bottomnavItem
            for index_child, class_no_child in enumerate(copy_of_appbar[KEY_CLASSES]):
                if index != index_child:
                    score_child = copy_of_appbar[KEY_SCORES][index_child]
                    box_child = copy_of_appbar[KEY_BOXES][index_child]

                    if class_no_child == 25:  # bottomnavItem - bottomnavItem overlap
                        if OverlapAlgo.is_inside_by_full_overlap(
                            box, box_child
                        ) or OverlapAlgo.is_inside_by_partial_overlap(box, box_child):
                            if score > score_child:
                                filter_extract[index_child] = False
                            else:
                                filter_extract[index] = False

                    if (
                        class_no_child == 6
                    ):  # bottomnavItem -Icon overlap priority to bottom nav
                        if OverlapAlgo.is_inside_by_full_overlap(
                            box, box_child
                        ) or OverlapAlgo.is_inside_by_partial_overlap(box, box_child):
                            filter_extract[index_child] = False

                else:
                    continue

        if class_no == 6:  # If it is Icon
            for index_child, class_no_child in enumerate(copy_of_appbar[KEY_CLASSES]):
                if index != index_child:
                    score_child = copy_of_appbar[KEY_SCORES][index_child]
                    box_child = copy_of_appbar[KEY_BOXES][index_child]

                    if OverlapAlgo.is_inside_by_full_overlap(
                        box, box_child
                    ) or OverlapAlgo.is_inside_by_partial_overlap(box, box_child):
                        if (
                            class_no_child == 25
                        ):  # bottomnav icon Overlapped priority to bottom nav
                            filter_extract[index] = False
                        if class_no_child == 6:  # Icons Overlaped
                            if score > score_child:
                                filter_extract[index_child] = False
                            else:
                                filter_extract[index] = False
                else:
                    continue

    # Change detection dict
    bottomnav_dict[KEY_CLASSES] = bottomnav_dict[KEY_CLASSES][filter_extract]
    bottomnav_dict[KEY_SCORES] = bottomnav_dict[KEY_SCORES][filter_extract]
    bottomnav_dict[KEY_BOXES] = bottomnav_dict[KEY_BOXES][filter_extract]