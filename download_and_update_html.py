import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import argparse

def download_resource(url, save_path, proxies=None):
    """ 下载资源并保存到指定路径 """
    try:
        response = requests.get(url, proxies=proxies)
        response.raise_for_status()  # 检查请求是否成功
        with open(save_path, 'wb') as file:
            file.write(response.content)
        return True
    except requests.RequestException as e:
        print(f"Failed to download {url}: {e}")
        return False

def update_html_links(html_content, base_url, output_dir, input_html_file, proxies=None):
    """ 更新HTML中的CSS和JS链接为本地路径 """
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # 处理CSS文件
    for link in soup.find_all('link', href=True):
        if link['href'].endswith('.css'):
            css_url = urljoin(base_url, link['href'])
            css_name = os.path.basename(urlparse(css_url).path)
            css_path = os.path.join(output_dir, css_name)
            if download_resource(css_url, css_path, proxies):
                link['href'] = os.path.relpath(css_path, start=os.path.dirname(input_html_file))
    
    # 处理JS文件
    for script in soup.find_all('script', src=True):
        if script['src'].endswith('.js'):
            js_url = urljoin(base_url, script['src'])
            js_name = os.path.basename(urlparse(js_url).path)
            js_path = os.path.join(output_dir, js_name)
            if download_resource(js_url, js_path, proxies):
                script['src'] = os.path.relpath(js_path, start=os.path.dirname(input_html_file))
    
    return str(soup)

def main():
    # 解析命令行参数
    parser = argparse.ArgumentParser(description="Download and update HTML resources.")
    parser.add_argument("input_html_file", help="Path to the input HTML file")
    parser.add_argument("--base-url", default="http://example.com/", help="Base URL for relative paths")
    parser.add_argument("--http-proxy", help="HTTP proxy server (e.g., http://proxy.example.com:8080)")
    parser.add_argument("--https-proxy", help="HTTPS proxy server (e.g., https://proxy.example.com:8080)")
    args = parser.parse_args()

    # 输入的HTML文件路径
    input_html_file = args.input_html_file
    
    # 根据输入HTML文件路径确定输出目录
    output_dir = os.path.join(os.path.dirname(input_html_file), 'local')
    
    # 基础URL，用于构建绝对URL
    base_url = args.base_url
    
    # HTTP代理设置
    proxies = {}
    if args.http_proxy:
        proxies['http'] = args.http_proxy
    if args.https_proxy:
        proxies['https'] = args.https_proxy

    # 读取原始HTML文件
    with open(input_html_file, 'r', encoding='utf-8') as file:
        html_content = file.read()

    # 创建输出目录
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # 更新HTML中的链接并下载资源
    updated_html_content = update_html_links(html_content, base_url, output_dir, input_html_file, proxies)

    # 将更新后的HTML内容写回文件
    output_html_file = os.path.join(os.path.dirname(input_html_file), 'index_local.html')
    with open(output_html_file, 'w', encoding='utf-8') as file:
        file.write(updated_html_content)

    print("Resources have been downloaded and HTML has been updated.")

if __name__ == '__main__':
    main()