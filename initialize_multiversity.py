from multiversity.multicare_dataset import MedicalDatasetCreator

mdc = MedicalDatasetCreator(directory = 'medical_datasets')

filters = [{'field': 'min_age', 'string_list': ['18']},
           {'field': 'gender', 'string_list': ['Male']},
           {'field': 'case_strings', 'string_list': ['tumor', 'cancer', 'carcinoma'], 'operator': 'any'},
           {'field': 'caption', 'string_list': ['metastasis', 'tumor', 'mass'], 'operator': 'any'},
           {'field': 'label', 'string_list': ['mri', 'head']}]


mdc.create_dataset(dataset_name = 'male_brain_tumor_dataset', filter_list = filters, dataset_type = 'multimodal')

mdc.display_example()
