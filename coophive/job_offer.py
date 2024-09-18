"""Define the JobOffer class which extends DataAttribute."""

from coophive.data_attribute import DataAttribute

job_offer_attributes = {
    "owner",
    "target_buyer",
    "created_at",
    "timeout",
    "CPU",
    "GPU",
    "RAM",
    "module",
    "prices",
    "instruction_count",
    "verification_method",
    "mediators",
    "benefit_to_buyer",
}


class JobOffer(DataAttribute):
    """Represents a job-offer object that inherits from DataAttribute."""

    def __init__(self):
        """Initializes a JobOffer object."""
        super().__init__()
        self.data_attributes = {attribute: 0 for attribute in job_offer_attributes}
        self.data_attributes["T_accept"] = self.calculate_T_accept()
        self.data_attributes["T_reject"] = self.calculate_T_reject()

    def calculate_T_accept(self):
        """Placeholder logic for T_accept."""
        return self.data_attributes.get("benefit_to_buyer", 0) * 1.05

    def calculate_T_reject(self):
        """Placeholder logic for T_reject."""
        return self.data_attributes.get("benefit_to_buyer", 0) * 0.95
