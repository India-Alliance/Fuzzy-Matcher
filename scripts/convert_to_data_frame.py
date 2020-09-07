import pandas as pd


def convert_to_data_frame(matched_names, uploaded_names):
    actual_name = []
    confidence = []
    index_no = []
    for i in matched_names:
        actual_name.append(i[0])
        confidence.append(i[1])
        index_no.append(i[2])

    return pd.DataFrame({'Uploaded Name': uploaded_names,
                         'Matched Names': actual_name,
                         'Confidence': confidence,
                         'Index Number': index_no})
