import json  
import os  
from nuscenes.nuscenes import NuScenes

# need to modify
nusc = NuScenes(version='v1.0-trainval', dataroot='/data/sets/nuscenes', verbose=True) 


# 读取原始JSON文件, val比较小，先尝试val
file_path = "nuscenes_val.json"  
with open(file_path, "r", encoding="utf-8") as file:  
    data = json.load(file)  
  
# 创建一个映射以跟踪已经分配的ID  
id_map = {}  
processed_data = []  
  
# 处理数据  
for item in data["questions"]:  
    sample_token = item["sample_token"]  
    question = item["question"]  
    answer = "<image>\n" + item["answer"]  # 在answer前添加前缀"<image>\n" 
    sample_id = None

    # get samo
    sample = nusc.get('sample', sample_token)  

    scene_token = sample['scene_token']
    # image_path_front = sample['data']['CAM_FRONT']  
    front_image_path = nusc.get('sample_data', sample['data']['CAM_FRONT'])['filename'] 
    fl_image_path = nusc.get('sample_data', sample['data']['CAM_FRONT_LEFT'])['filename']
    fr_image_path = nusc.get('sample_data', sample['data']['CAM_FRONT_RIGHT'])['filename']
    back_image_path = nusc.get('sample_data', sample['data']['CAM_BACK'])['filename']
    bl_image_path = nusc.get('sample_data', sample['data']['CAM_BACK_LEFT'])['filename']
    br_image_path = nusc.get('sample_data', sample['data']['CAM_BACK_RIGHT'])['filename']

    
    times = None
    # 如果已经为该sample_token分配了ID，则重用该ID，否则创建一个新的ID, 整体的id结构为 sample_token_X
    if sample_token in id_map:  
        id_map[sample_token] += 1
        sample_id = sample_token + "_" + str(id_map[sample_token])
    else:  
        # id = len(id_map) + 1  
        id_map[sample_token] = 1  
        sample_id = sample_token + "_1"
    

    # 添加处理后的数据
    processed_data.append
    ({      
        "id": sample_id,      
        "image": [{    
            "CAM_FRONT": front_image_path,      
            "CAM_FRONT_LEFT": fl_image_path,      
            "CAM_FRONT_RIGHT": fr_image_path,      
            "CAM_BACK": back_image_path,      
            "CAM_BACK_LEFT": bl_image_path,      
            "CAM_BACK_RIGHT": br_image_path      
        }],    
        "conversations": [    
            {  
                "from": "human",  
                "value": question  
            },  
            {  
                "from": "gpt",  
                "value": answer  
            }  
        ]    
    })    
  
# 输出处理后的JSON数据  
# print(json.dumps(processed_data, indent=4)) 

# 输出处理后的JSON数据到文件  
output_file_path = "processed_nuscenesqa_val.json"  
with open(output_file_path, "w", encoding="utf-8") as output_file:  
    json.dump(processed_data, output_file, indent=4)   