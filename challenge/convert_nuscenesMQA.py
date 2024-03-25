import csv
import json
from nuscenes.nuscenes import NuScenes
import re


nusc = NuScenes(version='v1.0-trainval', dataroot='./data/nuscenes', verbose=True) 
# 创建一个映射以跟踪已经分配的ID  
id_map = {} 
 

# These two functions should be implemented according to your dataset access patterns
def get_image_paths_and_scene(sample_token):
    # This function should return a list of image paths for the given sample_token
    # Replace the following example paths with the actual logic to obtain relevant paths
    sample = nusc.get('sample', sample_token)
    front_image_path = nusc.get('sample_data', sample['data']['CAM_FRONT'])['filename'] 
    fl_image_path = nusc.get('sample_data', sample['data']['CAM_FRONT_LEFT'])['filename']
    fr_image_path = nusc.get('sample_data', sample['data']['CAM_FRONT_RIGHT'])['filename']
    back_image_path = nusc.get('sample_data', sample['data']['CAM_BACK'])['filename']
    bl_image_path = nusc.get('sample_data', sample['data']['CAM_BACK_LEFT'])['filename']
    br_image_path = nusc.get('sample_data', sample['data']['CAM_BACK_RIGHT'])['filename']
    scene_token = sample['scene_token']


    return   front_image_path,fl_image_path,fr_image_path,back_image_path,bl_image_path,br_image_path,scene_token
    


def convert_csv_to_json(csv_filepath):
    data = []  # List to store the converted data
    
    # Open the CSV file and read each row
    with open(csv_filepath, newline='', encoding='utf-8') as csvfile:
        csvreader = csv.reader(csvfile)
        print("### Original file loaded")
        next(csvreader, None)  # Skip the header row if there is one
        for row in csvreader:
            line_num, sample_token, question, answer, _ = row  # Assuming four columns; ignore question_type
            front_image_path,fl_image_path,fr_image_path,back_image_path,bl_image_path,br_image_path,scene_token = get_image_paths_and_scene(sample_token)

            sample_id=None
            if sample_token in id_map:  
                id_map[sample_token] += 1
                sample_id = scene_token + "_" + sample_token + "_" + str(id_map[sample_token])
            else:  
                # id = len(id_map) + 1  
                id_map[sample_token] = 1  
                sample_id = scene_token + "_" + sample_token + "_1"


            filtered_question = re.sub(r'<[^>]*>', '', question)
            filtered_answer = re.sub(r'<[^>]*>', '', answer)

            """
            Example:
            Source:  In the <cam>front left</cam>, <target><cnt>2</cnt> <obj>bikes</obj></target> are detected.
            Convert: In the front left, 2 bikes are detected.
            """


            # entry = {
            #     "id": sample_id,
            #     "image": image_paths,
            #     "conversations": [
            #         {"from": "human", "value": filtered_question},
            #         {"from": "gpt", "value": "<image>\n" + filtered_answer}
            #     ]
            # }
            entry={        
            "id": sample_id,        
            "image": [front_image_path,fl_image_path,fr_image_path,back_image_path,bl_image_path,br_image_path       
            ],      
                "conversations": [
                    {"from": "human", "value": filtered_question},
                    {"from": "gpt", "value": "<image>\n" + filtered_answer}
                ] 
            }
            
            data.append(entry)
    
    # Write the JSON output
    # with open(json_filepath, 'w', encoding='utf-8') as jsonfile:
    #     json.dump(data, jsonfile, ensure_ascii=False, indent=4)
    with open(output_file_path, "w", encoding="utf-8") as output_file:  
        json.dump(data, output_file, indent=4)   

# Example usage
# csv_file_path = 'val.csv'
# "./nuScenes-MQA/df_train_mqa.json"  and "./nuScenes-MQA/df_val_mqa.json" 
file_path = "./nuScenes-MQA/df_train_mqa.json" 
output_file_path = "processed_nuscenesMQA_train.json" 
convert_csv_to_json(file_path)