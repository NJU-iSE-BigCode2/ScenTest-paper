# Here are some configuration items

####################################################################################################################################
# Information that must be configured
# The change value sets the knowledge graph of which function point it is, and it must be one of the SimilarTXTConfig values in this folder
graph_type = 'login'

####################################################################################################################################
# Here is the configuration information needed to generate the knowledge graph
# The directory where the original report is stored (the set value and the path of all files in this path must not contain Chinese characters)
original_data_path = '../Data/Original'
# The temporary file storage location after the text is disassembled and the control extraction and OCR analysis of the picture is completed. Chinese characters shall not appear in the same path
analyze_data_path = '../Data/Analyze'
# Combining the broken text and image information, the code creates a folder in the following folder named runtime to store the associated temporary files
connect_data_path = '../Data/Result/'
# This folder is the time folder generated by CONNECT_DATA_Path, which is set up to upload the analysis results report to the Knowledge Graph database
generate_data_path = '../Data/Result/login/'
# If you want to add to a previously recognized graph, you need to set this value to the folder of the original graph, otherwise set it to ' '
generate_supply_path='../Data/Result/login/'
# This value defines the OCR of different controls and is considered similar when similarity >= OCR_similarity. For example, this value can determine that "Login/Register" is similar to "Register Now"
ocr_similarity = 0.95
# Changing the value defines the operation of different controls, and similarity is considered when the similarity is >=opt_similarity. For example, changing the value can judge that "input" and "fill in" are similar
opt_similarity = 0.98
# It is difficult for the code recognized by the control to recognize whether the text box is a TextView or an EditView
# So it's assumed that controls that operate on "input" or a synonym for text entered by the user are set to EditView
# This is how similar the synonym for input is to the word input
# If you reach the value operation_input_Similarity, which indicates that the operation is an input, you directly set the component type to EditView
operation_input_similarity = 0.95
# For different Content, the ratio of similar Content is set here
rate_for_similar_content = 0.9
# For different contents, the value is set to be considered the same and no additional Content is added
rate_for_same_content = 0.99

####################################################################################################################################
# Here is the configuration information needed to search the knowledge graph
# The sum of the following three values must be 1 to represent the proportion of control type similarity, content similarity, and OCR text similarity between the node node in the knowledge graph and the Component node passed over
node_com_wid_sim_rate = 0.02
node_com_cnt_sim_rate = 0.90
node_com_ocr_sim_rate = 0.08
# Below are the validity thresholds for which a component is considered to be operationalized
valid_component_threshold = 0.75
# The sum of the following three values must be 1, which respectively represents the proportion of type similarity, content similarity, and OCR text similarity between nodes in the knowledge graph and the configured controls that need to be paid attention to
node_layout_wid_sim_rate = 0.02
node_layout_cnt_sim_rate = 0.80
node_layout_ocr_sim_rate = 0.18
# Below are the validity thresholds for which a component is considered to be configured
valid_layout_threshold = 0.8

