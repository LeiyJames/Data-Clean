import pandas as pd
import re

def clean_data(input_file, output_file):
    # Read the CSV file
    df = pd.read_csv(input_file)
    
    # Fix column name typo and reorder columns
    df.rename(columns={'emial': 'email'}, inplace=True)
    df = df[['name', 'email', 'phone', 'address']]  # Enforce column order
    
    # Remove rows with empty, WhatsApp, or Messenger in email field
    def is_valid_email(email):
        if pd.isna(email):
            return False
        email = str(email).lower().strip()
        # Exclude WhatsApp/Messenger entries
        if 'whatsapp' in email or 'messenger' in email:
            return False
        # Basic email format check
        return '@' in email and '.' in email.split('@')[-1]
    
    df = df[df['email'].apply(is_valid_email)]
    
    # Clean addresses - remove extra whitespace only
    def clean_address(address):
        if pd.isna(address):
            return ''
        # Remove extra spaces and normalize commas
        cleaned = ' '.join(str(address).split())
        cleaned = re.sub(r',\s+,', ', ', cleaned)
        return cleaned
    
    df['address'] = df['address'].apply(clean_address)
    
    # Save cleaned data to new CSV
    df.to_csv(output_file, index=False)
    print(f"Cleaned data saved to {output_file}")
    print(f"Original rows: {len(pd.read_csv(input_file))}, Cleaned rows: {len(df)}")

# Usage
input_csv = 'Cebu_Travel_1.csv'
output_csv = 'Cebu_Travel_Cleaned_Final.csv'
clean_data(input_csv, output_csv)