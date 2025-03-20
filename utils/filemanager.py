import requests
import os


def get_project_root():
    """
    获取项目根路径
    """
    current_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.abspath(os.path.join(current_dir, "../"))


def download_file(url, save_path):
    """
    从指定的 URL 下载文件并保存到本地路径。

    :param url: 文件的网络地址
    :param save_path: 本地保存路径
    """
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()  # 检查请求是否成功

        with open(save_path, "wb") as file:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:  # 避免写入空内容
                    file.write(chunk)

        print(f"文件已成功下载到: {save_path}")
    except requests.RequestException as e:
        print(f"下载文件失败: {e}")


# 示例用法
if __name__ == "__main__":
    file_url = "https://example.com/path/to/file.txt"  # 替换为实际文件 URL
    local_path = "downloaded_file.txt"  # 替换为本地保存路径
    download_file(file_url, local_path)
