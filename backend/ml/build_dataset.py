import pandas as pd

# Load datasets
resume_df = pd.read_csv("Resume.csv")
job_df = pd.read_csv("job_dataset.csv")

# Print columns (IMPORTANT)
print("Resume columns:", resume_df.columns)
print("Job columns:", job_df.columns)

# 👉 CHANGE THESE BASED ON OUTPUT
resume_col = resume_df.columns[0]
job_col = job_df.columns[0]

data = []

# Create dataset
for i in range(500):

    resume_text = str(resume_df.iloc[i][resume_col])

    # Matching pair
    job_text = str(job_df.iloc[i % len(job_df)][job_col])
    data.append([resume_text, job_text, 1])

    # Non-matching pair
    random_job = str(job_df.sample(1)[job_col].values[0])
    data.append([resume_text, random_job, 0])

# Create final dataset
final_df = pd.DataFrame(data, columns=["resume", "job", "label"])

# Save
final_df.to_csv("final_dataset.csv", index=False)

print("✅ Dataset created successfully!")