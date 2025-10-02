from fpdf import FPDF

#Defining pdf class with format:
class PDF(FPDF):
    def header(self):
        self.set_font("Arial", "B", 14)
        self.cell(0, 10, "Accident Scene Damage Report", ln=True, align="C")
        self.ln(10)

    def add_vehicle_damage_report(self, vehicle_id, damage_summary, damage_list):
        self.set_font("Arial", "B", 12)
        self.cell(0, 10, f"Vehicle ID: {vehicle_id}", ln=True)

        self.set_font("Arial", "", 11)
        self.multi_cell(0, 10, f"Summary: {damage_summary}")
        self.ln(3)

        if damage_list:
            self.set_font("Arial", "B", 11)
            self.cell(0, 10, "Detected Damaged Parts:", ln=True)
            self.set_font("Arial", "", 11)
            for part, damage_type, severity in damage_list:
                self.cell(0, 10, f"- {part}: {damage_type} (Severity: {severity})", ln=True)
        else:
            self.cell(0, 10, "No damages detected.", ln=True)
        self.ln(5)

#Function to generate the pdf repot
def generate_pdf_report(output_path, accident_report_data):
  pdf = PDF()
  pdf.add_page()

  for vehicle in accident_report_data:
    pdf.add_vehicle_damage_report(
            vehicle_id=vehicle["vehicle_id"],
            damage_summary=vehicle["summary"],
            damage_list=vehicle.get("damaged_parts", [])
        )
    pdf.output(output_path)
    print(f"PDF report generated successfully at: {output_path}")

#Sample accidnet data(load from a file or input)
accident_data = [
    {
        "vehicle_id": "Car A",
        "summary": "Car A sustained damage to multiple areas including the front bumper and headlights.",
        "damaged_parts": [
            ("Front bumper", "crack", "high"),
            ("Left headlight", "shattered", "medium")
        ]
    },
    {
        "vehicle_id": "Car B",
        "summary": "Minor damage detected on the rear bumper.",
        "damaged_parts": [
            ("Rear bumper", "dent", "low")
        ]
    }
]
#path to where the pdf is saved 
output_file = "../data/reports/accident_damage_report.pdf"
#genrate the pdf
generate_pdf_report(output_file, accident_data)

