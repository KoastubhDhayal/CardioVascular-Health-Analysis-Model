import pandas as pd
def calculate_sound_sleep(row):
    MIN_SLEEP_DURATION = 7  
    MIN_SLEEP_EFFICIENCY = 0.8  
    MAX_AWAKENINGS = 2  
    MIN_REM_SLEEP_PERCENTAGE = 20  

    sleep_duration = row['Sleep duration']
    sleep_efficiency = row['Sleep efficiency']
    awakenings = row['Awakenings']
    rem_sleep_percentage = row['REM sleep percentage']

    if (sleep_duration >= MIN_SLEEP_DURATION and
        sleep_efficiency >= MIN_SLEEP_EFFICIENCY and
        awakenings <= MAX_AWAKENINGS and
        rem_sleep_percentage >= MIN_REM_SLEEP_PERCENTAGE):
        return 1 
    else:
        return 0 

def calculate_bmi(row):
    try:
        weight = row['weight'] 
        height = row['height'] / 100  
        if pd.notnull(weight) and pd.notnull(height) and height > 0:
            return weight / (height ** 2)
        else:
            return None
    except KeyError:
        return None 

file_path = r'C:\Users\Vaishnavi\OneDrive\Desktop\sem 5\de\DE_MiniProject\data_filled.csv'

df = pd.read_csv(file_path)

df['sound_sleep'] = df.apply(calculate_sound_sleep, axis=1)
df['BMI'] = df.apply(calculate_bmi, axis=1)


def score_age(age):
    return max(0, min(100, (100 - age)))

def score_bmi(BMI):
    if 18.5 <= BMI <= 24.9:
        return 100
    elif BMI < 18.5:
        return 100 - ((18.5 - BMI) * 10)
    else:
        return max(0, 100 - ((BMI - 24.9) * 10))

def score_sound_sleep(sound_sleep):
    return 100 if sound_sleep == 1 else 0

def score_smoking(smoking_status):
    return 100 if smoking_status == 0 else 0

def score_exercise(exercise_frequency):
    return min(100, (exercise_frequency / 7) * 100)

def score_caffeine_alcohol(caffeine_consumption, alcohol_consumption):
    if caffeine_consumption <= 100 and alcohol_consumption <= 1:
        return 100
    elif caffeine_consumption <= 200 and alcohol_consumption <= 2:
        return 80
    else:
        return 60

def calculate_cardio_impact(row):
    age_score = score_age(row['Age'])
    bmi_score = score_bmi(row['BMI'])
    sound_sleep_score = score_sound_sleep(row['sound_sleep'])
    smoking_score = score_smoking(row['Smoking status'])
    exercise_score = score_exercise(row['Exercise frequency'])
    caffeine_alcohol_score = score_caffeine_alcohol(row['Caffeine consumption'], row['Alcohol consumption'])
    
    cardio_impact = (
        age_score +
        bmi_score +
        sound_sleep_score +
        smoking_score +
        exercise_score +
        caffeine_alcohol_score
    ) / 6
    
    return cardio_impact

df['cardio_impact'] = df.apply(calculate_cardio_impact, axis=1)

new_file_path = r'C:\Users\Vaishnavi\OneDrive\Desktop\sem 5\de\DE_MiniProject\data_updated.csv'
df.to_csv(new_file_path, index=False)

print(f"Updated file saved to {new_file_path}")
