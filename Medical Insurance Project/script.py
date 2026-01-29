import csv

class MedicalInsuranceAnalyst:
    def __init__(self, csv_file):
        # Initialize lists
        self.ages = []
        self.sexes = []
        self.bmis = []
        self.num_children = []
        self.smoker_statuses = []
        self.regions = []
        self.insurance_charges = []
        
        # Load data immediately
        self.load_data(csv_file)

    def load_data(self, csv_file):
        # The try block starts here
        try:
            with open(csv_file) as insurance_file:
                reader = csv.DictReader(insurance_file)
                for row in reader:
                    self.ages.append(int(row['age']))
                    self.sexes.append(row['sex'])
                    self.bmis.append(float(row['bmi']))
                    self.num_children.append(int(row['children']))
                    self.smoker_statuses.append(row['smoker'])
                    self.regions.append(row['region'])
                    self.insurance_charges.append(float(row['charges']))
            print("Data successfully loaded.\n")
        except FileNotFoundError:
            # This except must align perfectly with the try above
            print(f"Error: The file {csv_file} was not found.")

    def analyze_ages(self):
        total_age = sum(self.ages)
        average_age = total_age / len(self.ages)
        print(f"Average Patient Age: {average_age:.2f} years")

    def analyze_sexes(self):
        females = self.sexes.count('female')
        males = self.sexes.count('male')
        print(f"Gender Distribution: {females} females, {males} males")

    def analyze_regions(self):
        unique_regions = []
        for region in self.regions:
            if region not in unique_regions:
                unique_regions.append(region)
        southeast_count = self.regions.count('southeast')
        total_people = len(self.regions)
        print(f"Southeast Representation: {southeast_count} patients ({southeast_count/total_people*100:.2f}%)")

    def analyze_charges(self):
        total_charges = sum(self.insurance_charges)
        average_charge = total_charges / len(self.insurance_charges)
        print(f"Average Yearly Insurance Cost: ${average_charge:.2f}")

    def analyze_smoker_liability(self):
        total_smoker_cost = 0
        smoker_count = 0
        total_non_smoker_cost = 0
        non_smoker_count = 0

        for i in range(len(self.smoker_statuses)):
            if self.smoker_statuses[i] == 'yes':
                total_smoker_cost += self.insurance_charges[i]
                smoker_count += 1
            else:
                total_non_smoker_cost += self.insurance_charges[i]
                non_smoker_count += 1
        
        avg_smoker = total_smoker_cost / smoker_count
        avg_non_smoker = total_non_smoker_cost / non_smoker_count
        print(f"Smoker Liability: ${avg_smoker - avg_non_smoker:.2f}")

# --- Execution Block ---
if __name__ == "__main__":
    analyst = MedicalInsuranceAnalyst('insurance.csv')
    analyst.analyze_ages()
    analyst.analyze_sexes()
    analyst.analyze_regions()
    analyst.analyze_charges()
    analyst.analyze_smoker_liability()
    

        

        