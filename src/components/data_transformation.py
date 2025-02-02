import pandas as pd
from src.loggers import logging
from datetime import datetime



class DataQuality:
    def __init__(self, df,output_cleaned_path, output_failed_path):
        # Initialize with dataframe and output file path (for storing mismatched data)
        self.df = df
        self.output_clean_path = output_cleaned_path
        self.output_failed_path = output_failed_path
        self.failed_data = pd.DataFrame()  # Store all the failed rows



    def record_failed_data(self, failed_rows):
        """Append failed rows to the failed_data DataFrame, ensuring no duplicates."""
        # Check for duplicates between new failed rows and already stored failed data
        if not failed_rows.empty:
            self.failed_data = pd.concat([self.failed_data, failed_rows]).drop_duplicates()


    def check_unique_uid(self):
        """Ensure UID is unique and not null."""
        failed = self.df[self.df["uid"].isnull() | self.df["uid"].duplicated()]
        if not failed.empty:
            logging.error(f"Duplicate or null UID found: {failed[['uid', 'farmer_name']]}")
            self.failed_data = pd.concat([self.failed_data, failed])

    def check_mandatory_fields(self):
        """Ensure mandatory fields are not null."""
        mandatory_fields = ["uid", "farmer_name", "program_year"]
        missing_values = self.df[mandatory_fields].isnull().sum()
        missing_fields = missing_values[missing_values > 0]
        if not missing_fields.empty:
            logging.error(f"Mandatory Fields Missing: {missing_fields}")
            missing_data = self.df[self.df[mandatory_fields].isnull().any(axis=1)]
            self.failed_data = pd.concat([self.failed_data, missing_data])

    def check_program_year(self):
        """Ensure program year is a valid year."""
        invalid_years = self.df[~self.df["program_year"].astype(str).str.match(r"^\d{4}$")]
        if not invalid_years.empty:
            logging.error(f"Invalid program year format found: {invalid_years['program_year'].unique()}")
            self.failed_data = pd.concat([self.failed_data, invalid_years])

    def check_land_area(self):
        """Ensure land area values are positive and consistent."""
        failed = self.df[(self.df["total_land_area_acre"] <= 0) |
                         (self.df["area_f4f_acre"] > self.df["total_land_area_acre"])]
        if not failed.empty:
            logging.error(f"Land area inconsistencies found: {failed[['farmer_name', 'total_land_area_acre']]}")
            self.failed_data = pd.concat([self.failed_data, failed])

    def check_yes_no_columns(self):
        """Ensure specific columns contain only 'Yes' or 'No'."""
        yes_no_columns = [
            "kml_uploaded", "contract uploaded", "land_record_uploaded", "cc_training_uploaded",
            "soil_sample_collected", "drone_ortho_taken", "farmer_payment_collected", "baseline_survey"
        ]
        
        for col in yes_no_columns:
            if col in self.df.columns:
                invalid_rows = self.df[~self.df[col].isin(["Yes", "No"])]
                if not invalid_rows.empty:
                    logging.error(f"Invalid values found in column '{col}': {invalid_rows[col].unique()}")
                    self.failed_data = pd.concat([self.failed_data, invalid_rows])

    def check_district_block(self):
        """Ensure 'District' and 'Block' values are from a predefined valid list."""
        valid_districts = ['A', 'B']  
        valid_blocks = ['p', 'q', 'r', 's']  

        # Identify invalid District values
        invalid_districts = self.df[~self.df["District"].isin(valid_districts)]
        if not invalid_districts.empty:
            logging.error(f"Invalid District values found:\n{invalid_districts[['District', 'Block']]}")
            self.failed_data = pd.concat([self.failed_data, invalid_districts])

        # Identify invalid Block values
        invalid_blocks = self.df[~self.df["Block"].isin(valid_blocks)]
        if not invalid_blocks.empty:
            logging.error(f"Invalid Block values found:\n{invalid_blocks[['District', 'Block']]}")
            self.failed_data = pd.concat([self.failed_data, invalid_blocks])

    

    def check_date_columns(self):
        """Check for invalid date formats and logically incorrect dates. Allow NaN but remove invalid ones."""
        date_columns = [
            "farmer_payment_date", "contract_date", "plantation_date", "cc_training_date"
        ]

        for col in date_columns:
            if col in self.df.columns:
                invalid_rows = []
                
                for index, value in self.df[col].items():
                    if pd.isna(value):  # Allow NaN values
                        continue

                    try:
                        # Attempt to parse the date, assuming a common format (DD-MMM-YYYY or DD-MM-YY)
                        parsed_date = datetime.strptime(str(value), "%d-%b-%Y")  # Example: 31-Jul-2023
                    except ValueError:
                        try:
                            parsed_date = datetime.strptime(str(value), "%d-%m-%y")  # Example: 07-03-23
                        except ValueError:
                            invalid_rows.append(index)
                            continue  # Move to the next value

                    # **Additional Logical Check:** Ensure the parsed date actually exists
                    day, month, year = parsed_date.day, parsed_date.month, parsed_date.year
                    try:
                        datetime(year, month, day)  # This will raise an error if the date doesn't exist
                    except ValueError:
                        invalid_rows.append(index)

                if invalid_rows:
                    logging.error(f"Invalid date detected in '{col}': Rows {invalid_rows}")
                    self.failed_data = pd.concat([self.failed_data, self.df.loc[invalid_rows]])






    def check_payment_validity(self):
        """Ensure payment is collected before contract signing."""
        failed = self.df[(self.df["farmer_payment_collected"] == "No") & (self.df["contract uploaded"] == "Yes")]
        if not failed.empty:
            logging.error(f"Contract uploaded but payment not collected: {failed[['farmer_name']]}")
            self.failed_data = pd.concat([self.failed_data, failed])

    def check_trees_planted(self):
        """Ensure number of trees planted is within 350-450."""
        failed = self.df[(self.df["trees_planted"] < 350) | (self.df["trees_planted"] > 450)]
        if not failed.empty:
            logging.error(f"Invalid trees planted count: {failed[['farmer_name', 'trees_planted']]}")
            self.failed_data = pd.concat([self.failed_data, failed])
    

    def check_species_distribution(self):
        """Ensure species-wise distribution adds up to trees planted."""
        species_cols = [
                        "mango_native", "mango_grafted_kesar", "lemon_sai_sharbati", "sitaphal_native", 
                        "sitaphal_golden", "sitaphal _balanagar", "awala", "awala_grafted", "peru", 
                        "peru_sardar", "chincha", "chincha_grafted", "Jamun", "Jamun_bhardoli", 
                        "chikku", "orange", "mosambi", "dalimb", "ramphal", "drumstick_Koimb", 
                        "bamboo", "karwand", "arjun", "katesawar", "karanj", "kaduneem", "kanchan", 
                        "kadamb", "bhendi", "shirish", "ain", "pimpal", "vad", "tamhan", "waval", 
                        "palas", "babhul", "bakul"
                    ]
        self.df["total_species_distributed"] = self.df[species_cols].sum(axis=1)
        failed = self.df[self.df["total_species_distributed"] != self.df["trees_planted"]]
        if not failed.empty:
            logging.error(f"Species count mismatch: {failed[['farmer_name', 'total_species_distributed', 'trees_planted']]}")
            self.failed_data = pd.concat([self.failed_data, failed])

    def save_failed_data(self):
        """Save the rows that failed the quality checks into a separate table or file and remove them from clean data."""
        if not self.failed_data.empty:
            # Save failed data
            self.failed_data = self.failed_data.drop_duplicates(subset=["uid"])
            self.failed_data.to_csv(self.output_failed_path, index=False)
            logging.info(f"Failed data saved to {self.output_failed_path}")

            # Remove failed records from the original dataset
            num_failed = len(self.failed_data)
            logging.info(f"Removed {num_failed} invalid records from the clean dataset.")

    def save_clean_data(self):
        """Save the clean data after removing the failed records."""
        clean_data = self.df
        # Remove failed records from the clean dataset
        # clean_data = self.df.drop(self.failed_data.index)
        clean_data.to_csv(self.output_clean_path, index=False)
        logging.info(f"Clean data saved to {self.output_clean_path}")


    def run_all_checks(self):
        """Run all quality checks and log errors."""
        logging.info("Starting data quality checks...")
        self.check_unique_uid()
        self.check_mandatory_fields()
        self.check_program_year()
        self.check_district_block()
        self.check_date_columns()
        self.check_land_area()
        self.check_yes_no_columns()
        self.check_payment_validity()
        self.check_trees_planted()
        self.check_species_distribution()
        self.save_failed_data()  # Save the failed data after running checks
        self.save_clean_data()
        logging.info("Data quality checks completed.")

# Usage
if __name__ == "__main__":
    input_data = pd.read_csv("artifacts/data.csv") # Input file
    output_failed_path = "artifacts/failed_data.csv"
    output_file_path = "artifacts/cleaned_data.csv"  # Output file for failed data
    dq_checker = DataQuality(input_data,output_file_path, output_failed_path)
    dq_checker.run_all_checks()
