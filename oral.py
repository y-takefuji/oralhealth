import pandas as pd
import matplotlib.pyplot as plt

# Load the CSV file
df = pd.read_csv('BRFSS__Table_of_Oral_Health_20240917.csv')

# Print unique 'Topic' values and allow user to select one by number
topics = df['Topic'].unique()
print("Select a 'Topic' by number:")
for i, topic in enumerate(topics):
    print(f"{i}: {topic}")
topic_index = int(input("Enter the number corresponding to the 'Topic': "))
selected_topic = topics[topic_index]

# Filter the dataframe by the selected topic
df_topic = df[df['Topic'] == selected_topic]

# Print unique 'Break_Out_Category' values and allow user to select one by number
break_out_categories = df_topic['Break_Out_Category'].unique()
print("Select a 'Break_Out_Category' by number:")
for i, category in enumerate(break_out_categories):
    print(f"{i}: {category}")
category_index = int(input("Enter the number corresponding to the 'Break_Out_Category': "))
selected_category = break_out_categories[category_index]

# Filter the dataframe by the selected break out category
df_category = df_topic[df_topic['Break_Out_Category'] == selected_category]

# Get unique 'Break_Out' values
break_outs = df_category['Break_Out'].unique()[:8]  # Limit to 8 distinct lines

# Plot the data
linestyles = ['-', '--', '-.', ':']
widths = [1, 2]
plt.figure(figsize=(10, 6))

result_data = []

for i, break_out in enumerate(break_outs):
    df_break_out = df_category[df_category['Break_Out'] == break_out]
    mean_values = df_break_out.groupby('Year')['Data_value'].mean()
    total_sample_size = df_break_out['Sample_Size'].sum()
    linestyle = linestyles[i % len(linestyles)]
    width = widths[(i // len(linestyles)) % len(widths)]
    plt.plot(mean_values.index, mean_values.values, label=f"{break_out} (n={total_sample_size})", linestyle=linestyle, linewidth=width, color='black')
    
    # Append result data for CSV
    result_data.append({
        'Break_Out': break_out,
        'Total_Sample_Size': total_sample_size,
        'Mean_Values': mean_values.values
    })

plt.xlabel('Year')
plt.ylabel('Mean Data Value')
plt.title(f'Mean Data Values for {selected_category} in {selected_topic}')
plt.legend()

# Replace "/" with "_" in filenames
safe_category = selected_category.replace('/', '_')
safe_topic = selected_topic.replace('/', '_')

# Save plot as PNG file with selected category and topic in the filename
png_filename = f'result_plot_{safe_category}_{safe_topic}.png'.replace(' ', '_')
plt.savefig(png_filename)
plt.show()

# Save result data to CSV file with selected category and topic in the filename
result_df = pd.DataFrame(result_data)
csv_filename = f'result_data_{safe_category}_{safe_topic}.csv'.replace(' ', '_')
result_df.to_csv(csv_filename, index=False)

