import pandas as pd

# 1. Loading raw data
print('Loading raw data...')
df = pd.read_excel('data/raw/Data_FLOW_survey.xlsx', sheet_name='Tabelle1')
print(f' Loaded {len(df)} rows and {len(df.columns)} columns')

# 2. rename group labels for better readability
print('\nRenaming group labels...')
group_labels = {
    'Treatment': 'treat',
    'Control1': 'ctr1',
    'Control2': 'ctr2',
}
df['group'] = df['group'].map(group_labels)
print(f' Groups now: {df["group"].unique()}')

# 3. Check and standardise gender values
print('\nChecking gender values...') 
print(f' Unique values: {df["gender"].unique()}')
# title case standardisation just in case
df['gender'] = df['gender'].str.title()

# 4. Add completed_followup flag
print('\nAdding followup flags...')
df['completed_followup'] = df['complete'] == 3
print(f' Completed followup: {df["completed_followup"].sum()} participants')

# 5. Calculate change scores (change = posttest - pretest)
print('\nCalculating change scores...')
metrics = [
    'knowledge_score',
    'attitude',
    'awareness',
    'skills',
    'personal_efficacy',
    'collective_efficacy',
    'behavioral_control',
    'personal_norms',
    'nature_rel',
    'interest',
    'past_behavior1',
    'past_behavior2',
    'plan_behavior1',
    'plan_behavior2',
]

for metric in metrics:
    pre = f'{metric}.1'  # pretest column
    post = f'{metric}.2'  # posttest column
    change = f'{metric}_change'  # new change score column
    if pre in df.columns and post in df.columns:
        df[change] = df[post] - df[pre]
        print(f' ✓ {change}')

# 6. Save cleaned dataset
print('\nSaving clean dataset...')
df.to_csv('data/flow_clean.csv', index=False)
print(f' ✓ Saved {len(df)} rows to data/flow_clean.csv')

# 7. Sanity check
print('\nSanity check on clean data')
clean = pd.read_csv('data/flow_clean.csv')
print(f' Shape: {clean.shape}')
print(f' Change score columns: {[c for c in clean.columns if "change" in c]}')
print('\nDone!')
                    

