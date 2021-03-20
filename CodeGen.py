# Genearate code for widget
import xml.etree.ElementTree as ET
import numpy as np
import LevelAlgo

xml_tag = '<?xml version="1.0" encoding="utf-8"?>'
android_namespace = 'xmlns:android="http://schemas.android.com/apk/res/android"'
app_namespace = 'xmlns:app="http://schemas.android.com/apk/res-auto"'

default_margin = 10


def create_layout_file(file_name, code):
    myfile = open(file_name, "w")
    myfile.write(code)


def get_code_by_class(widget):
    class_no = widget["class"]
    if class_no == 1:
        return textview_code(widget)
    elif class_no == 2:
        return edittext_code(widget)
    elif class_no == 3:
        return button_code(widget)
    elif class_no == 4:
        return imageview_code(widget)
    elif class_no == 5:
        return fab_code(widget)
    elif class_no == 6:
        return imageview_code(widget)
    elif class_no == 7:
        return appbar_code(widget)
    elif class_no == 8:
        return checkbox_code(widget)
    elif class_no == 9:
        return ""
    elif class_no == 10:
        return radiobutton_code(widget)
    elif class_no == 11:
        return radiogroup_code(widget)
    elif class_no == 12:
        return switch_code(widget)
    elif class_no == 13:
        return cardview_code(widget)
    elif class_no == 14:
        return recycler_code(widget)
    elif class_no == 15:
        return scrollview_code(widget)
    elif class_no == 16:
        return ""
    elif class_no == 17:
        return ""
    elif class_no == 18:
        return imageview_code(widget)
    elif class_no == 19:
        return ""
    elif class_no == 20:
        return ""
    elif class_no == 21:
        return ""
    elif class_no == 22:
        return ""
    elif class_no == 23:
        return ""
    elif class_no == 24:
        return child_constraint_layout_code(widget)
    elif class_no == 25:
        return ""
    elif class_no == 26:
        return ""
    elif class_no == 27:
        return ""
    elif class_no == 28:
        return ""
    elif class_no == 29:
        return ""
    elif class_no == 30:
        return ""
    elif class_no == 31:
        return ""
    elif class_no == 32:
        return ""
    elif class_no == 33:
        return ""
    elif class_no == 34:
        return ""
    elif class_no == 35:
        return ""
    elif class_no == 36:
        return ""
    elif class_no == 37:
        return ""
    elif class_no == 38:
        return ""
    elif class_no == 39:
        return ""
    elif class_no == 40:
        return ""
    elif class_no == 41:
        return ""
    elif class_no == 42:
        return ""


def child_constraint_layout_code(widget, with_namespace=False):
    LevelAlgo.set_positions_for_container(widget)
    cl_code = "<androidx.constraintlayout.widget.ConstraintLayout\n{attributes}>\n{content}\n</androidx.constraintlayout.widget.ConstraintLayout>"
    content_list = list()
    attribute_list = list()
    if with_namespace:
        attribute_list.append(android_namespace)
        attribute_list.append(app_namespace)

    content_dict = widget["content"]
    for key in content_dict:
        child_widget = content_dict[key]
        child_widget_code = get_code_by_class(child_widget)
        content_list.append(child_widget_code)

    attribute_list.extend(get_basic_widget_code(widget))
    attribute_list.extend(get_width_height_code("wrap_content", "wrap_content"))
    attribute_code = "\n".join(attribute_list)
    content_code = "\n".join(content_list)
    return cl_code.format(attributes=attribute_code, content=content_code)


def textview_code(widget):
    txtView_code = "<TextView\n{attributes}/>"
    attribute_list = list()
    attribute_list.extend(get_basic_widget_code(widget))
    attribute_list.extend(get_width_height_code("wrap_content", "wrap_content"))
    attribute_list.append(get_text_code("TextView"))
    attributes_code = "\n".join(attribute_list)
    return txtView_code.format(attributes=attributes_code)


def button_code(widget):
    txtView_code = "<Button\n{attributes}/>"
    attribute_list = list()
    attribute_list.extend(get_basic_widget_code(widget))
    attribute_list.extend(get_width_height_code("wrap_content", "wrap_content"))
    attribute_list.append(get_text_code("Button"))
    attributes_code = "\n".join(attribute_list)
    return txtView_code.format(attributes=attributes_code)


def edittext_code(widget):
    txtView_code = "<EditText\n{attributes}/>"
    attribute_list = list()
    attribute_list.extend(get_basic_widget_code(widget))
    attribute_list.extend(get_width_height_code("wrap_content", "wrap_content"))
    attribute_list.append(get_text_code("EditText"))
    attributes_code = "\n".join(attribute_list)
    return txtView_code.format(attributes=attributes_code)


def imageview_code(widget):
    imgView_code = "<ImageView\n{attributes}/>"
    attribute_list = list()
    attribute_list.extend(get_basic_widget_code(widget))
    attribute_list.extend(get_width_height_code("wrap_content", "wrap_content"))
    attributes_code = "\n".join(attribute_list)
    return imgView_code.format(attributes=attributes_code)


def recycler_code(widget):
    recycler_code = "<androidx.recyclerview.widget.RecyclerView\n{attributes}/>"
    attribute_list = list()
    attribute_list.extend(get_basic_widget_code(widget))
    attribute_list.extend(get_width_height_code("match_parent", "wrap_content"))
    attributes_code = "\n".join(attribute_list)
    select_suitable_item_for_recycler(widget)
    recycler_item = widget["item"]
    widget_id = widget["id"]
    item_name = "item_{name}"
    genearate_recycler_item(recycler_item, item_name.format(name=widget_id.lower()))
    return recycler_code.format(attributes=attributes_code)


def select_suitable_item_for_recycler(recycler):
    items = recycler["content"]
    if len(items) > 0:
        values_list = list(items.values())
        recycler["item"] = values_list[0]


def genearate_recycler_item(widget, item_name):
    item_code = "{xml}\n{content}"
    file_name = "{name}.xml"
    content_code = ""

    if widget["class"] == 13:
        content_code = cardview_code(widget, True)
    else:
        content_code = child_constraint_layout_code(widget, True)

    code = item_code.format(xml=xml_tag, content=content_code)
    create_layout_file(file_name=file_name.format(name=item_name), code=code)


def constraint_layout_code(widget, with_namespace=True):
    LevelAlgo.set_positions_for_container(widget)
    cl_code = "{xml}\n<androidx.constraintlayout.widget.ConstraintLayout\n{attributes}>\n{content}\n</androidx.constraintlayout.widget.ConstraintLayout>"
    content_list = list()
    attribute_list = list()
    if with_namespace:
        attribute_list.append(android_namespace)
        attribute_list.append(app_namespace)

    content_dict = widget["content"]
    for key in content_dict:
        child_widget = content_dict[key]
        child_widget_code = get_code_by_class(child_widget)
        content_list.append(child_widget_code)

    attribute_list.extend(get_basic_widget_code(widget))
    attribute_list.extend(get_width_height_code("match_parent", "match_parent"))
    attribute_code = "\n".join(attribute_list)
    content_code = "\n".join(content_list)
    return cl_code.format(xml=xml_tag, attributes=attribute_code, content=content_code)


def cardview_code(widget, with_namespace=False):
    LevelAlgo.set_positions_for_container(widget)
    cardView_code = "<androidx.cardview.widget.CardView\n{attributes}>\n{content}\n</androidx.cardview.widget.CardView>"
    content_list = list()
    attribute_list = list()
    if with_namespace:
        attribute_list.append(android_namespace)
        attribute_list.append(app_namespace)

    attribute_list.extend(get_basic_widget_code(widget))
    attribute_list.extend(get_width_height_code("wrap_content", "wrap_content"))
    attribute_list.append(get_margin_code(10))
    attribute_code = "\n".join(attribute_list)
    content_code = child_constraint_layout_code(widget)

    return cardView_code.format(attributes=attribute_code, content=content_code)


def get_basic_widget_code(widget):
    basic_code = list()
    widget_id = widget["id"]
    if "position" in widget:
        position = widget["position"]
        basic_code.extend(get_position_code(position))
    basic_code.append(get_id_code(widget_id))
    basic_code.append(get_margin_code(default_margin))
    return basic_code


def get_id_code(widget_id):
    code = 'android:id="{new_id}"'
    return code.format(new_id=get_new_id(widget_id))


def get_position_code(position_dict):
    top_to_top = 'app:layout_constraintTop_toTopOf="{id}"'
    start_to_start = 'app:layout_constraintStart_toStartOf="{id}"'
    top_to_bottom = 'app:layout_constraintTop_toBottomOf="{id}"'
    start_to_end = 'app:layout_constraintStart_toEndOf="{id}"'
    bottom_to_bottom = 'app:layout_constraintBottom_toBottomOf="{id}"'
    bottom_to_top = 'app:layout_constraintBottom_toTopOf="{id}"'
    end_to_end = 'app:layout_constraintEnd_toEndOf="{id}"'
    position_list = list()

    for key in position_dict:
        value = position_dict[key]
        if key == "top":
            if value == "parent":
                ttt = top_to_top.format(id=value)
                position_list.append(ttt)
            else:
                ttb = top_to_bottom.format(id=get_id(value))
                position_list.append(ttb)
        elif key == "start":
            if value == "parent":
                sts = start_to_start.format(id=value)
                position_list.append(sts)
            else:
                ste = start_to_end.format(id=get_id(value))
                position_list.append(ste)
                ttt = top_to_top.format(id=get_id(value))
                position_list.append(ttt)
                btb = bottom_to_bottom.format(id=get_id(value))
                position_list.append(btb)
        elif key == "bottom":
            if value == "parent":
                btb = bottom_to_bottom.format(id=value)
                position_list.append(btb)
            else:
                btt = bottom_to_top.format(id=get_id(value))
                position_list.append(btt)
        elif key == "end":
            if value == "parent":
                ete = end_to_end.format(id=value)
                position_list.append(ete)

    return position_list


def get_text_code(text_value):
    code = 'android:text="{text}"'
    return code.format(text=text_value)


def get_width_height_code(width, height):
    code_list = list()
    width_code = 'android:layout_width="{width_txt}"'
    height_code = 'android:layout_height="{height_txt}"'
    code_list.append(width_code.format(width_txt=width))
    code_list.append(height_code.format(height_txt=height))
    return code_list


def get_id(widget_id):
    id_prefix = "@id/"
    return id_prefix + widget_id


def get_new_id(widget_id):
    id_prefix = "@+id/"
    return id_prefix + widget_id


def get_margin_code(margin):
    margin_code = 'android:layout_margin="{value}dp"'
    return margin_code.format(value=margin)
