from textx import metamodel_for_language
data_dsl_mm = metamodel_for_language('vizz')

model = data_dsl_mm.model_from_file('sales.vizz')