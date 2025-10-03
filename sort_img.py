import os
import shutil
import json
from PIL import Image

def get_aspect_ratio_folder(width, height):
    """根据宽高比确定应放入的文件夹名称"""
    # 常见宽高比定义
    aspect_ratios = {
        (16, 9): "16_9",
        (9, 16): "9_16",
        (4, 3): "4_3",
        (3, 4): "3_4",
        (3, 2): "3_2",
        (2, 3): "2_3",
        (1, 1): "1_1",
        (21, 9): "21_9",
        (9, 21): "9_21"
    }
    
    # 计算最大公约数以简化比例
    def gcd(a, b):
        return a if b == 0 else gcd(b, a % b)
    
    d = gcd(width, height)
    simplified_ratio = (width // d, height // d)
    
    # 容差率，用于匹配近似比例
    tolerance = 0.05
    target_folder = None
    
    # 查找精确或近似的标准比例
    for standard_ratio, folder_name in aspect_ratios.items():
        standard_value = standard_ratio[0] / standard_ratio[1]
        current_value = simplified_ratio[0] / simplified_ratio[1]
        
        if abs(standard_value - current_value) < tolerance:
            return folder_name
    
    # 如果没有找到匹配的标准比例，返回简化后的实际比例
    return f"{simplified_ratio[0]}_{simplified_ratio[1]}"


def main():
    folder = input("请输入文件夹路径：").strip()
    folderto = input("请输入目标文件夹路径：").strip()
    
    # 检查源文件夹是否存在
    if not os.path.exists(folder):
        print(f"错误：文件夹 '{folder}' 不存在！")
        return
    
    if not os.path.isdir(folder):
        print(f"错误：'{folder}' 不是一个有效的文件夹！")
        return
    
    # 创建目标文件夹（如果不存在）
    if not os.path.exists(folderto):
        try:
            os.makedirs(folderto)
        except Exception as e:
            print(f"错误：无法创建目标文件夹 '{folderto}': {e}")
            return
    
    if not os.path.isdir(folderto):
        print(f"错误：'{folderto}' 不是一个有效的文件夹！")
        return
    
    # 支持的图片格式
    image_extensions = ('.jpg', '.jpeg', '.png', '.bmp', '.gif', '.tiff', '.webp')
    
    # 获取文件夹中的所有文件
    try:
        files = os.listdir(folder)
    except PermissionError:
        print(f"错误：没有权限访问文件夹 '{folder}'")
        return
    
    # 统计信息
    processed_count = 0
    error_count = 0
    
    # 存储整理后的文件信息
    organized_files = {}
    
    print("开始处理图片...")
    
    # 遍历文件
    for file in files:
        file_path = os.path.join(folder, file)
        
        # 只处理图片文件
        if os.path.isfile(file_path) and file.lower().endswith(image_extensions):
            try:
                # 打开图片获取尺寸，使用显式关闭确保文件句柄被释放
                img = Image.open(file_path)
                width, height = img.size
                img.close()  # 显式关闭文件句柄
                
                # 确定目标文件夹
                target_folder_name = get_aspect_ratio_folder(width, height)
                target_folder_path = os.path.join(folderto, target_folder_name)
                
                # 确保目标文件夹存在
                if not os.path.exists(target_folder_path):
                    os.makedirs(target_folder_path)
                
                # 移动文件
                target_file_path = os.path.join(target_folder_path, file)
                
                # 检查目标文件是否已存在
                if os.path.exists(target_file_path):
                    base_name, ext = os.path.splitext(file)
                    counter = 1
                    while os.path.exists(os.path.join(target_folder_path, f"{base_name}_{counter}{ext}")):
                        counter += 1
                    target_file_path = os.path.join(target_folder_path, f"{base_name}_{counter}{ext}")
                
                # 更安全的文件移动方式
                try:
                    shutil.move(file_path, target_file_path)
                except PermissionError:
                    # 如果直接移动失败，尝试先复制再删除
                    shutil.copy2(file_path, target_file_path)
                    os.remove(file_path)
                
                print(f"已移动 '{file}' ({width}x{height}) 到 '{target_folder_name}' 文件夹")
                processed_count += 1
                
                # 记录整理后的文件信息
                if target_folder_name not in organized_files:
                    organized_files[target_folder_name] = []
                organized_files[target_folder_name].append({
                    "name": file,
                    "size": [width, height],  # 使用列表而不是元组，更便于JSON序列化
                    "path": os.path.join(folderto, target_folder_name, os.path.basename(target_file_path)).replace("\\", "/")  # 统一使用正斜杠
                })
                
            except Exception as e:
                print(f"处理文件 '{file}' 时出错: {e}")
                error_count += 1
    
    # 将整理后的文件列表写入 imgs.json（在目标文件夹中）
    try:
        json_path = os.path.join(folderto, "imgs.json")
        with open(json_path, "w", encoding="utf-8") as json_file:
            json.dump(organized_files, json_file, ensure_ascii=False, indent=2)
        print(f"已将整理后的文件列表写入 {json_path}")
    except Exception as e:
        print(f"写入 imgs.json 时出错: {e}")
    
    print(f"\n处理完成！成功处理 {processed_count} 个文件，{error_count} 个文件出错。")


if __name__ == "__main__":
    main()