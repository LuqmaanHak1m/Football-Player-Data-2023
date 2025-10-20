import pandas as pd
import numpy as np
import datetime as dt
import re

def clean_columns(val):
    if pd.isnull(val) or str(val) == "-":
        return np.nan
    return val    

def calculate_age(dob, ref_date):
    if pd.isna(dob):
        return None
    return (ref_date - dob).days // 365

def clean_currency(val):
    if pd.isnull(val) or val == "Not for Sale":
        return np.nan
    
    val = str(val).replace('$', '').replace(',', '').strip()
    try:
        return float(val)
    except:
        return np.nan
    
def clean_weight(val):
    if pd.isnull(val):
        return np.nan
    # Remove any currency symbols or commas
    val = str(val).replace('kg', '').strip()
    try:
        return float(val)
    except:
        return np.nan
    
def height_to_cm(height):
    if pd.isnull(height):
        return np.nan
    
    # Remove spaces and handle strings like 5'6", 5'6, etc.
    height = str(height).strip().replace('"', '').replace(' ', '')
    
    # Match pattern like 5'6
    match = re.match(r"^(\d+)'(\d+)?$", height)
    if match:
        feet = int(match.group(1))
        inches = int(match.group(2)) if match.group(2) else 0
        total_cm = round((feet * 12 + inches) * 2.54, 1)
        return total_cm
    
    return np.nan  

def multi_indexing(player_data: pd.DataFrame) -> pd.DataFrame:
    column_groups = {
        'General': [
            'UID', 'Name', 'Rec', 'DOB', 'Inf', 'Club', 'Based', 'Nat',
            'Height', 'Weight', 'Age', 'Position', 'Transfer Value',
            'Preferred Foot', 'Left Foot', 'Right Foot'
        ],
        'Matches': [
            'Imp M', 'Caps', 'AT Apps', 'AT Gls', 'AT Lge Apps', 'AT Lge Gls',
            'Team', 'Yth Apps', 'Yth Gls'
        ],
        'Physical': [
            'Acc', 'Str', 'Sta', 'Pac', 'Nat.1', 'Jum', 'Bal', 'Agi'
        ],
        'Mental': [
            'Wor', 'Vis', 'Tea', 'OtB', 'Ldr', 'Fla', 'Cnt', 'Cmp', 'Bra', 'Ant',
            'Agg', 'Dec', 'Det', 'Pos'
        ],
        'Goalkeeping': [
            'Thr', 'TRO', 'Ref', 'Pun', '1v1', 'Kic', 'Han', 'Ecc', 'Cmd', 'Aer', 'Com'
        ],
        'Technical': [
            'Tec', 'Tck', 'Pen', 'Pas', 'Mar', 'L Th', 'Lon', 'Hea', 'Fre',
            'Fir', 'Fin', 'Dri', 'Cro', 'Cor'
        ],
        'Other': [
            'Vers', 'Temp', 'Spor', 'Prof', 'Pres', 'Loy', 'Dirt', 'Amb', 'Ada', 'Cons'
        ],
        'Injury': [
            'Rc Injury', 'Inj Pr'
        ],
        'Media': [
            'Media Description', 'Media Handling', 'Cont'
        ]
    }

    # --- Flatten the mapping into a list of tuples for MultiIndex ---
    multi_cols = []
    for category, cols in column_groups.items():
        for col in cols:
            multi_cols.append((category, col))

    # --- Create the MultiIndex ---
    multi_index = pd.MultiIndex.from_tuples(multi_cols)

    # --- Align with existing columns in player_data ---
    # Keep only columns that actually exist in your DataFrame
    valid_cols = [col for _, col in multi_cols if col in player_data.columns]

    # Rebuild the filtered MultiIndex based on existing columns
    filtered_multi_cols = [(grp, col) for grp, col in multi_cols if col in player_data.columns]
    filtered_index = pd.MultiIndex.from_tuples(filtered_multi_cols)

    # --- Reorder and apply the MultiIndex ---
    player_data = player_data[valid_cols]
    player_data.columns = filtered_index

    return player_data


def transform(player_data: pd.DataFrame) -> pd.DataFrame:
    player_data.columns = player_data.columns.str.strip()

    for column in player_data.columns:
        player_data[column] = player_data[column].apply(clean_columns)


    # Only process DOB if it exists
    if 'DOB' in player_data.columns:
        # Only modify if DOB is not already datetime
        if not np.issubdtype(player_data['DOB'].to_numpy().dtype, np.datetime64):
            # Step 1: Extract the date part (everything before the space)
            player_data['Date'] = player_data['DOB'].astype(str).str.extract(r'(^[\d/]+)')

            # Step 2: Convert to datetime safely
            player_data['DOB'] = pd.to_datetime(player_data['Date'], format='%d/%m/%Y', errors='coerce')


    # Compute age (only for valid DOBs)
    if 'DOB' in player_data.columns:
        today = dt.datetime.strptime("01/01/2022", '%d/%m/%Y')

        # Apply the function to each row
        player_data['Age'] = player_data['DOB'].apply(lambda dob: calculate_age(dob, today))


    if 'Transfer Value' in player_data.columns:
        player_data['Transfer Value Clean'] = player_data['Transfer Value'].apply(clean_currency)


    if 'Weight' in player_data.columns:
        player_data['Weight'] = player_data['Weight'].apply(clean_weight)


    # Apply conversion
    if 'Height' in player_data.columns:
        player_data['Height'] = player_data['Height'].apply(height_to_cm)



    list_of_unwanted_fields = ["Unnamed: 0","Rec","Date", "Transfer Value"]

    for unwanted_field in list_of_unwanted_fields:

        if unwanted_field in player_data.columns:

            player_data.drop(columns=[unwanted_field], inplace=True)

    # Remove duplicate rows
    player_data.drop_duplicates(inplace=True)

    player_data = multi_indexing(player_data)

    return player_data