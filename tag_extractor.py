import requests
from flask import Blueprint, request, jsonify
from bs4 import BeautifulSoup
import yaml
from googletrans import Translator

# 从yaml文件加载配置
def load_config(yaml_file):
    with open(yaml_file, 'r') as file:
        return yaml.safe_load(file)

config = load_config('config.yaml')

def translate_with_google(texts, from_lang='auto', to_lang='zh-cn'):
    """
    使用Google翻译API翻译文本列表。
    
    Args:
        texts: 要翻译的文本或文本列表
        from_lang: 源语言代码，默认为'auto'（自动检测）
        to_lang: 目标语言代码，默认为'zh-cn'（简体中文）
        
    Returns:
        翻译后的文本列表，如果翻译失败则返回None
    """
    # 确保translator实例是本地创建的而不是全局的
    translator = Translator()
    
    try:
        if not texts:  # 处理空输入
            return []
            
        if isinstance(texts, list):
            # 批量翻译，逐个处理以避免JSON解析错误
            results = []
            for text in texts:
                if not text:  # 处理列表中的空元素
                    results.append("")
                    continue
                    
                try:
                    translation = translator.translate(text, src=from_lang, dest=to_lang)
                    results.append(translation.text if translation and hasattr(translation, 'text') else text)
                except Exception as e:
                    print(f"单个文本翻译出错: {e}")
                    results.append(text)  # 出错则保留原始文本
            return results
        else:
            # 单个文本翻译
            if not texts:  # 处理空字符串
                return [""]
                
            translation = translator.translate(texts, src=from_lang, dest=to_lang)
            if translation and hasattr(translation, 'text'):
                return [translation.text]
            return [texts]  # 如果翻译结果不符合预期，返回原文本
            
    except ValueError as e:
        # 处理无效目标语言错误
        print(f"Google翻译API参数错误: {e}")
        # 尝试其他语言代码格式
        if 'zh' in to_lang and 'invalid destination language' in str(e):
            try:
                # 尝试使用其他可能的中文代码
                for zh_code in ['zh-cn', 'zh-CN', 'zh-TW', 'zh-tw', 'zh']:
                    try:
                        return translate_with_google(texts, from_lang, zh_code)
                    except:
                        continue
            except Exception as e2:
                print(f"尝试其他中文代码也失败: {e2}")
        return None
    except Exception as e:
        print(f"Google翻译API请求失败: {e}")
        return None

def translate_texts(texts, from_lang='auto', to_lang='zh-cn'):
    """
    使用Google翻译API翻译文本列表。
    如果失败，则返回未翻译的原始文本。
    
    Args:
        texts: 要翻译的文本或文本列表
        from_lang: 源语言代码，默认为'auto'（自动检测）
        to_lang: 目标语言代码，默认为'zh-cn'（简体中文）
        
    Returns:
        翻译后的文本列表
    """
    # 确保texts不为None
    if texts is None:
        return []
        
    # 使用Google翻译API
    translated_texts = translate_with_google(texts, from_lang, to_lang)
    if translated_texts is not None:
        return translated_texts

    # 如果谷歌翻译失败，返回原始文本
    if isinstance(texts, list):
        return texts
    return [texts] if texts else []

# 创建蓝图
tag_extractorbp = Blueprint('tag_extractor', __name__)

@tag_extractorbp.route('/extract_tags', methods=['GET'])
def extract_tags():
    # 从请求参数中获取URL
    url = request.args.get('url')
    if not url:
        return jsonify({"error": "Missing URL parameter"}), 400

    # 发送GET请求到指定的URL
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.RequestException as e:
        return jsonify({"error": str(e)}), 500

    # 解析HTML内容
    soup = BeautifulSoup(response.content, 'html.parser')

    # 提取所需的数据并翻译
    tags = []
    tag_names = []
    for li in soup.select('[data-tag-name]'):  # 选择所有具有 data-tag-name 属性的元素
        # 提取标签名，并将下划线替换为空格
        tag_name = li.get('data-tag-name').replace('_', ' ')
        tag_names.append(tag_name)
        tag_info = {
            'tag_name': tag_name,
            'is_deprecated': li.get('data-is-deprecated') == 'true',
            'links': [a.text.strip() for a in li.find_all('a')],
            'post_count': li.find('span', class_='post-count').get('title') if li.find('span', class_='post-count') else None
        }
        tags.append(tag_info)
    
    # 只有当有标签名需要翻译时才执行翻译
    if tag_names:
        translated_tag_names = translate_texts(tag_names)
        
        # 将翻译后的标签名添加到标签信息中
        for i, tag in enumerate(tags):
            if i < len(translated_tag_names):
                tag['translated_tag_name'] = translated_tag_names[i]
            else:
                tag['translated_tag_name'] = tag['tag_name']  # 如果翻译结果缺失，使用原始文本
    else:
        for tag in tags:
            tag['translated_tag_name'] = tag['tag_name']

    # 将提取和翻译的数据组装为JSON格式返回
    return jsonify(tags)

@tag_extractorbp.route('/Tagtranslate', methods=['POST'])
def translate():
    data = request.get_json()
    texts = data.get('texts')
    if not texts:
        return jsonify({"error": "Missing texts parameter"}), 400

    translated_texts = translate_texts(texts)
    return jsonify({"translated_texts": translated_texts})