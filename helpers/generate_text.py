# Function to retrieve the quantity for an item from the table:
def retrieve_quantity_from_table(df, item, year):

    """Function to retrieve the quantity for a specific item from the SCR table.
    Args:
        df (pd.DataFrame): DataFrame containing the SCR report data.            
        item (str): The item to retrieve the quantity for.
        year (int): The year column to retrieve the quantity from.

    Returns:
        float: The quantity for the specified item and year.
    """
    
    # Retrieve the quantity for the item from the table:
    quantity = df.loc[df['€m'] == item, year].values[0]

    return quantity

# Function to generate the wording for the movements in the report::
def wording_scr_movement(df, previous_year, current_year, unit):

    """Function to generate wording for the movements in the Total SCR.
    
    Args:
        df (pd.DataFrame): DataFrame containing the SCR report data.            
        previous_year (int): Previous year for comparison.
        current_year (int): Current year for comparison.
        unit (str): Unit to append to the quantities (e.g., 'm' for million).
    Returns:
        str: Wording describing the movements in the Total SCR.
    """
    
    # Calculate current and previous quantities and movement based on period:
    quantity_previous  = retrieve_quantity_from_table(df, 'Total SCR', previous_year)
    quantity_current   = retrieve_quantity_from_table(df, 'Total SCR', current_year)  
    quantity_movement  = quantity_current - quantity_previous

    # Round quantities:  
    quantity_previous  = round(quantity_previous, 1)  
    quantity_current   = round(quantity_current, 1)
    quantity_movement  = round(quantity_movement, 1)

    # Calculate the SCR components with the largest and smallest movement:
    scr_components = ['Market Risk', 'Counterparty Default Risk', 'Life Risk', 'Health Risk', 'Diversification Benefit', 'Operational Risk', 'Deferred Tax Adjustment']
    max_movement = df.loc[df['€m'].isin(scr_components), 'Movement'].max()
    min_movement = -df.loc[df['€m'].isin(scr_components), 'Movement'].min()
    
    # Retrieve the component with the largest and smallest movement:
    filtered_df = df[df['€m'].isin(scr_components)]
    max_movement_index = filtered_df['Movement'].idxmax()
    min_movement_index = filtered_df['Movement'].idxmin()
    component_with_max_movement = df.at[max_movement_index, '€m']
    component_with_min_movement = df.at[min_movement_index, '€m']

    if quantity_movement == 0:
        return f"The Total SCR is unchanged since the previous year at {quantity_previous}{unit}."
    elif quantity_movement > 0:
        return f"The largest contributor to the increase in the Total SCR by €{quantity_movement}{unit} is the increase in €{max_movement}{unit} by {component_with_max_movement} risk."
    elif quantity_movement < 0:
        return f"The largest contributor to the decrease in the Total SCR by €{quantity_movement}{unit} is the decrease in €{min_movement}{unit} by {component_with_min_movement} risk."
    else:
        return f"Invalid data in SCR table."

# Function to generate the wording for the movements in the report::
def wording_percentage_movement(df, item, previous_year, current_year, unit):
    
    """Function to generate wording for the percentage movements of a specific item.
    
    Args:
        df (pd.DataFrame): DataFrame containing the SCR report data.    
        item (str): The item to generate wording for.
        previous_year (int): Previous year for comparison.  
        current_year (int): Current year for comparison.
        unit (str): Unit to append to the quantities (e.g., 'm' for million).
    Returns:
        str: Wording describing the movements in the Total SCR.
    """

    # Retrieve the quantities for the item from the table:
    quantity_previous = round(retrieve_quantity_from_table(df, item, previous_year), 1)
    quanitity_current = round(retrieve_quantity_from_table(df, item, current_year), 1)

    # Calculate the percentage movement:
    if quantity_previous == 0:
        quanitity_movement_percentage = 0
    else:
        quanitity_movement_percentage = round((quanitity_current/quantity_previous - 1) * 100, 1)

    if quanitity_movement_percentage == 0:
        return f"The {item} unchanged since the previous year at €{quantity_previous}{unit}."
    elif quanitity_movement_percentage > 0:
        return f"The {item} increased by {quanitity_movement_percentage}% from €{quantity_previous}{unit} to €{quanitity_current}{unit} since the previous year."
    elif quanitity_movement_percentage < 0:
        return f"The {item} decreased by {-quanitity_movement_percentage}% €{quantity_previous}{unit} to €{quanitity_current}{unit} since the previous year."
    else:
        return f"Invalid data in SCR table."

# Function to generate the wording for the movements in the report::
def wording_percentage_point_movement(df, item, previous_year, current_year):

    """Function to generate wording for the percentage point movements of a specific item.
    
    Args:
        df (pd.DataFrame): DataFrame containing the SCR report data.    
        item (str): The item to generate wording for.
        previous_year (int): Previous year for comparison.  
        current_year (int): Current year for comparison.    
    Returns:
        str: Wording describing the movements in the Total SCR.
    """

    # Retrieve the quantities for the item from the table:
    percentage_previous = retrieve_quantity_from_table(df, item, previous_year)
    percentage_current  = retrieve_quantity_from_table(df, item, current_year)

    # Calculate the percentage movement:
    movement_percentage_point = round(percentage_current - percentage_previous, 3)

    # Rounding: 
    percentage_previous       = round(percentage_previous * 100, 1)
    percentage_current        = round(percentage_current * 100, 1)
    movement_percentage_point = round(movement_percentage_point * 100, 1)

    # Generate the wording for the movement in percentage points:
    if movement_percentage_point == 0:
        return f"The {item} is unchanged since the previous year at {percentage_previous}%."
    elif movement_percentage_point > 0:
        return f"The {item} increased by {movement_percentage_point}% from {percentage_previous}% to {percentage_current}% since the previous year."
    elif movement_percentage_point < 0:
        return f"The {item} decreased by {-movement_percentage_point}% from {percentage_previous}% to {percentage_current}% since the previous year."
    else:
        return f"Invalid data in SCR table."

# Function to generate the wording for the target solvency ratio:
def wording_target_solvency(target_solvency_ratio, solvency_ratio_current):

    """Function to generate wording for the target solvency ratio comparison.
    Args:
        target_solvency_ratio (float): Target solvency ratio (as a decimal, e.g., 1.25 for 125%).
        solvency_ratio_current (float): Current solvency ratio (as a decimal, e.g., 1.30 for 130%).
    Returns:
        str: Wording describing the comparison between current and target solvency ratio.
    """

    # Rounding:
    target_solvency_ratio = round(target_solvency_ratio * 100, 1)
    solvency_ratio_current = round(solvency_ratio_current * 100, 1)

    if solvency_ratio_current < target_solvency_ratio:
        return f"The Company's solvency ratio of {solvency_ratio_current}% is below its target of {target_solvency_ratio}%."
    elif solvency_ratio_current == target_solvency_ratio:
        return f"The Company's solvency ratio of {solvency_ratio_current}% is equal its the target of {target_solvency_ratio}%."
    elif solvency_ratio_current > target_solvency_ratio:
        return f"The Company's solvency ratio of {solvency_ratio_current}% is above its target of {target_solvency_ratio}%."
    else:
        return f"Invalid data in SCR table."
    

# Generate wording for BSCR movements using Python code:
def wording_bscr_movements(df, quantity, previous_year, current_year):

    """Function to generate wording for the BSCR movements.
    
    Args:
        df (pd.DataFrame): DataFrame containing the SCR report data.    
        quantity (str): 'amount' or 'percentage'.   
        previous_year (int): Previous year for comparison.
        current_year (int): Current year for comparison.    
    Returns:
        str: Wording describing the movements in the BSCR.
    """

    # Select only the first 4 rows to include the BSCR modules:
    df_bscr = df.head(4)

    # Compute the percentage contribution of each value to the total
    df_bscr_percentage = df_bscr.copy()  # Copy to keep the same structure
    df_bscr_percentage[current_year] = df_bscr[current_year] / df_bscr[current_year].sum()
    df_bscr_percentage[previous_year] = df_bscr[previous_year] / df_bscr[previous_year].sum()

    if quantity == 'amount':
        df_bscr_analysed = df_bscr
        description = ''
    else:
        df_bscr_analysed = df_bscr_percentage
        description = 'proportion of '

    # Initialize lists to store results
    increased = []
    decreased = []

    # Loop through each row in the subset to compare the current and previous year values
    for _, row in df_bscr_analysed.iterrows():
        category = row['€m']
        current = row[current_year]
        previous = row[previous_year]

        # Compare current and previous year capital values
        if current > previous:
            increased.append(category)
        elif current < previous:
            decreased.append(category)

    # Generate the response
    if increased and not decreased:
        return f"The {description} BSCR increased for all risk categories since the previous year."
    elif decreased and not increased:
        return f"The {description} BSCR decreased for all risk categories since the previous year."
    else:
        # Generate a sentence with a more detailed breakdown
        increase_str = ", ".join(increased)
        decrease_str = ", ".join(decreased)
        return f"The {description}{increase_str} BSCR increased over the year but {description}{decrease_str} BSCR decreased."
