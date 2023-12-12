from models.t_shirt_size_chart import t_shirt_size_chart_ratio, t_shirt_size_chart_length
from sizing.crawler import build_t_shirt_key_points, get_ratios_for_tshirt, get_actual_length_for_tshirt
from sizing.sizing_pre_processing import get_corner_coordinates_for_tshirt, correct_class_for_sleeves
from sizing.yolo_model_prediction import model_json_prediction_for_sizing_issue
import streamlit as st

def calculate_lengths_for_image(t_shirt_img):
    predictions = model_json_prediction_for_sizing_issue(t_shirt_img)
    predictions = get_corner_coordinates_for_tshirt(predictions)
    corrected_predictions = correct_class_for_sleeves(predictions)
    chest_length, shoulder_length, tshirt_length = get_actual_length_for_tshirt(
        corrected_predictions)
    return chest_length, shoulder_length, tshirt_length

def get_context_based_upon_lengths(chest_length, shoulder_length, tshirt_length):

    tshirt_size = ["S", "M", "L", "XL", "XXL"]

    for size in tshirt_size:
        if t_shirt_size_chart_length[size]['chest'][0] < chest_length < t_shirt_size_chart_length[size]['chest'][1]:
            context += f"Tshirt's Chest length {chest_length} cm is within  range of {chest_min} cm  and {chest_max}cm. So, correct size for tshirt should be {size} "
        if t_shirt_size_chart_length[size]['chest'][0] < chest_length < t_shirt_size_chart_length[size]['chest'][1]:
            context += f"Tshirt's Chest length {chest_length} cm is within  range of {chest_min} cm  and {chest_max}cm. So, correct size for tshirt should be {size} "
        if t_shirt_size_chart_length[size]['chest'][0] < chest_length < t_shirt_size_chart_length[size]['chest'][1]:
            context += f"Tshirt's Chest length {chest_length} cm is within  range of {chest_min} cm  and {chest_max}cm. So, correct size for tshirt should be {size} "




    # chest_min, chest_max,chest_threshold_min, chest_threshold_max = t_shirt_size_chart_length[tshirt_size]['chest'][0], \
    #     t_shirt_size_chart_length[tshirt_size]['chest'][1],t_shirt_size_chart_length[tshirt_size]['chest'][2],t_shirt_size_chart_length[tshirt_size]['chest'][3]
    # shoulder_min, shoulder_max, shoulder_threshold_min, shoulder_threshold_max = t_shirt_size_chart_length[tshirt_size]['shoulder'][0], \
    #     t_shirt_size_chart_length[tshirt_size]['shoulder'][1], t_shirt_size_chart_length[tshirt_size]['shoulder'][2], t_shirt_size_chart_length[tshirt_size]['shoulder'][3]
    # tshirt_min, tshirt_max, tshirt_threshold_min, tshirt_threshold_max = t_shirt_size_chart_length[tshirt_size]['tshirt'][0], \
    #    t_shirt_size_chart_length[tshirt_size]['tshirt'][1],t_shirt_size_chart_length[tshirt_size]['tshirt'][2], t_shirt_size_chart_length[tshirt_size]['tshirt'][3]

    context_pre = (
        'Here is the information available for a tshirt regarding its sizing. Also compulsorily please in the response provide'
        ' actual values along with min and  max values possible. Also if the actual values are in border range'
        'take that into consideration while resolving query')
    context = ''
    if chest_min <= chest_length <= chest_max:
        context += f"Tshirt's Chest length {chest_length} cm is within expected range of {chest_min} cm  and {chest_max}cm. "
    elif chest_length < chest_min:
        if chest_length > chest_threshold_min:
            context += f"Although Tshirt's Chest length {chest_length}  cm is below expected range of {chest_min} cm  and {chest_max}cm, still it seems to be acceptable value. "

        else:
            context += f"Tshirt's Chest length {chest_length}  cm is below expected range of {chest_min} cm  and {chest_max}cm. "
    elif chest_length > chest_max:
        if chest_length < chest_threshold_max:
            context += f"Although Tshirt's Chest length {chest_length}  cm is above  expected range of {chest_min} cm  and {chest_max}cm, still it seems to be acceptable value. "
        else:
            context += f"Tshirt's Chest length {chest_length} cm is greater than expected range of {chest_min} cm  and {chest_max}cm.  "

    if shoulder_min <= shoulder_length <= shoulder_max:
        context += f"Tshirt's Shoulder length {shoulder_length} cm is within expected range  of {shoulder_min} cm and {shoulder_max} cm. "
    elif shoulder_length < shoulder_min:
        if shoulder_length > shoulder_threshold_min:
            context += f"Although Tshirt's Shoulder length {shoulder_length}  cm is below expected range of {shoulder_min} cm  and {shoulder_max}cm, still it seems to be acceptable value. "
        else:
            context += f"Tshirt's Shoulder length {shoulder_length} cm is lesser than expected range of {shoulder_min} cm and {shoulder_max} cm . "
    elif shoulder_length > shoulder_max:
        if shoulder_length < shoulder_threshold_max:
            context += f"Although Tshirt's Shoulder length {shoulder_length}  cm is above  expected range of {shoulder_min} cm  and {shoulder_max} cm, still it seems to be acceptable value. "
        else:
            context += f"Tshirt's Shoulder length {shoulder_length} cm is greater than expected range of {shoulder_max}cm and {shoulder_max} cm. "

    if tshirt_min <= tshirt_length <= tshirt_max:
        context += f"Tshirt's  length {tshirt_length} cm is within expected range  of {tshirt_min} cm and {tshirt_max} cm. "
    elif tshirt_length < tshirt_min:
        if tshirt_length < tshirt_threshold_min:
            context += f"Although Tshirt's  length {tshirt_length}  cm is below  expected range of {tshirt_min} cm  and {tshirt_max} cm, still it seems to be acceptable value. "
        else:
            context += f"Tshirt's  length {tshirt_length} cm is lesser than expected range of {tshirt_min}cm and {tshirt_max} cm. "
    elif tshirt_length > tshirt_max:
        if tshirt_length < tshirt_threshold_max:
            context += f"Although Tshirt's  length {tshirt_length}  cm is above  expected range of {tshirt_min} cm  and {tshirt_max} cm, still it seems to be acceptable value. "
        else:
            context += f"Tshirt's  length {tshirt_length} cm is greater than expected range of {tshirt_max}cm and {tshirt_max} cm. "

    st.write(context)
    final = context_pre + context
    return final



