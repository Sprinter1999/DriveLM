import json 
import os 
from nuscenes.nuscenes import NuScenes
import csv
 
# need to modify
nusc = NuScenes(version='v1.0-trainval', dataroot='./data/nuscenes', verbose=True)
csv_filepath = "./nuScenes-MQA/df_train_mqa.csv"
 

   
# 创建一个映射以跟踪已经分配的ID 
# id_map = {} 
# processed_data = []
result_data = {} 

with open(csv_filepath, newline='', encoding='utf-8') as csvfile:
    csvreader = csv.reader(csvfile)
    print("### Original file loaded")
    next(csvreader, None)  # Skip the header row if there is one
    for row in csvreader:
        if "val" in csv_filepath:
            sample_token, question, answer, _ = row  # Assuming four columns; ignore question_type
        else:
            line, sample_token, question, answer, _ = row

        question = "<image>\n" + question
   
        sample = nusc.get('sample', sample_token) 
    
        scene_token = sample['scene_token']
        # image_path_front = sample['data']['CAM_FRONT']
        prefix = "../nuscenes/" #../nuscenes/samples/CAM_FRONT_LEFT/n00
        front_image_path = prefix + nusc.get('sample_data', sample['data']['CAM_FRONT'])['filename']
        fl_image_path = prefix + nusc.get('sample_data', sample['data']['CAM_FRONT_LEFT'])['filename']
        fr_image_path = prefix + nusc.get('sample_data', sample['data']['CAM_FRONT_RIGHT'])['filename']
        back_image_path = prefix + nusc.get('sample_data', sample['data']['CAM_BACK'])['filename']
        bl_image_path = prefix + nusc.get('sample_data', sample['data']['CAM_BACK_LEFT'])['filename']
        br_image_path = prefix + nusc.get('sample_data', sample['data']['CAM_BACK_RIGHT'])['filename']
    
        
        times = None
        # 如果已经为该sample_token分配了ID，则重用该ID，否则创建一个新的ID, 整体的id结构为 scenetoken_sample_token_X
        # if sample_token in id_map: 
        #     id_map[sample_token] += 1
        #     sample_id = scene_token +"_"+ sample_token + "_" + str(id_map[sample_token])
        # else: 
        #     # id = len(id_map) + 1 
        #     id_map[sample_token] = 1 
        #     sample_id = scene_token +"_"+sample_token + "_1"
        

        # 如果scene_token在result_data中已经存在，追加sample_token；否则创建scene_token对应的数据结构  
        if scene_token in result_data:  
            if sample_token not in result_data[scene_token]["keyframes"]:  
                result_data[scene_token]["keyframes"][sample_token] = {  
                    "QA": {  
                        "perception": [  
                            {"Q": question, "A": answer, "C": None, "con_up": None, "con_down": None,  "cluster": None, "layer": None, "tag": [0]}  
                        ]  
                    },  
                    "image_paths": {  
                        "CAM_FRONT": front_image_path,  
                        "CAM_FRONT_LEFT": fl_image_path,  
                        "CAM_FRONT_RIGHT": fr_image_path,  
                        "CAM_BACK": back_image_path,
                        "CAM_BACK_LEFT": bl_image_path,  
                        "CAM_BACK_RIGHT": br_image_path    
                    }  
                }  
        else:  
            result_data[scene_token] = {  
                "keyframes": {  
                    sample_token: {  
                        "QA": {  
                            "perception": [  
                            {"Q": question, "A": answer, "C": None, "con_up": None, "con_down": None,  "cluster": None, "layer": None, "tag": [0]}  
                            ]  
                        },  
                        "image_paths": {  
                            "CAM_FRONT": front_image_path,  
                            "CAM_FRONT_LEFT": fl_image_path,  
                            "CAM_FRONT_RIGHT": fr_image_path,  
                            "CAM_BACK": back_image_path,
                            "CAM_BACK_LEFT": bl_image_path,  
                            "CAM_BACK_RIGHT": br_image_path     
                        }  
                    }  
                }  
            }  
   
# 输出处理后的JSON数据 
#print(processed_data)
#print(json.dumps(processed_data, indent=4))
 
# 输出处理后的JSON数据到文件,train and val
output_file_path = "processed_nuscenesMQA_val_V2_eval.json" 
# output_file_path = "processed_nuscenesqa_train_V2_eval.json" 
# with open(output_file_path, "w", encoding="utf-8") as output_file: 
#     json.dump(processed_data, output_file, indent=4)  
with open(output_file_path, "w") as outfile:  
    json.dump(result_data, outfile, indent=4) 