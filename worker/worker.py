import scida_py as scida
import scida_rest_api

class Worker:
    """Assign items to age groups"""
    def __init__(self):
        """Initialize the worker"""
        self.age_cohort_label = None
        self.age_label = scida.tag("0010", "1010")
        self.cohorts = {
            "toddler": (0, 2),
            "preschooler": (3, 4),
            "school-age": (5, 12),
            "teen": (13, 18),
            "young-adult": (19, 39),
            "middle-aged": (40, 64),
            "senior": (65, 85),
            "old": (86, 1500),
        }

    def configure(self, agent_id, agent_name, _agentVersion, scida_api_base):
        """Create age-cohort label if it does not exists"""
        if scida_api_base:
            scida_rest_api.Configuration.get_default().host = scida_api_base

        self.age_cohort_label = scida.label_by_id("age-cohort-test")
        if not self.age_cohort_label.exists():
            self.age_cohort_label = scida.create_new_label(
                "age-cohort-test", "Age cohort Test", "Describes the age cohort of the subject(testing)"
            )

    def work(self, item_id, dataset_id, _execution_id):
        """Assign items to the the specific age cohorts"""
        dataset = scida.dataset_by_id(dataset_id)
        item = dataset.load_item(item_id)
        age = item.own_value(self.age_label)
        if age is not None:
            age_years = 0
            if age.endswith("Y"):
                age_years = int(age[:-1])
            for cohort, (start, end) in self.cohorts.items():
                if start <= age_years <= end:
                    item.upsert_attribute_value(self.age_cohort_label, cohort)
                    break
