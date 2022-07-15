# Django - View: StreamingHttpResponse

[返回Django首页](../django_index.md)

## 目录

- [实例:播放视频](#实例播放视频)

***

## 实例:播放视频

- 思路：
  - 前段：
    1. 使用`video`标签;
    2. 设置`src`属性为指定的url.
  - 后端：
    1. 获取`request.META`的`HTTP_RANGE`值,获取当前需要的;
    2. 整理当前提取的起止字节和响应的长度;
    3. 使用`yeild`迭代读取视频文件;
    4. 生成`StreamingHttpResponse`实例,设置状态是`206`;
    5. 设置响应`header`.

- Html

```html
    <video id="video"  controls>
        <!-- <source src="/media/video/video_test.mp4" type="video/mp4"> -->
        <source src="" type="video/mp4">
    </video>
```

- view_py

```python
import os,re
from django.http import StreamingHttpResponse
from ArgusHome import settings

def music_test_streaming(request):

    file_name = "video_test.mp4"
    file_path = os.path.join(settings.MEDIA_ROOT,'video',file_name)
    file_size = os.path.getsize(file_path)

    req_range = request.META["HTTP_RANGE"]      #获取请求表头header的RANGE,通常是"bytes=0-"
    range_re = re.compile(r'bytes\s*=\s*(\d+)\s*-\s*(\d*)', re.I)       #创建正则规则
    range_match = range_re.match(req_range)            #进行正则的匹配
    start_byte, end_byte = range_match.groups()        #获取将匹配的值，分别是请求的开始和结束字节
    
    start_byte = int(start_byte) if start_byte else 0       #如果start_byte不为空，则等于该值的整数类型;如果是空，即第一次请求,则为0
    #设置返回响应的长度；如果start_byte与文件大小file_size之差大于或等于8m，即每片响应体最大体积，则取值为8m; 否则取值为他们的差
    chunk_size = 1024 * 1024 * 8
    content_length = chunk_size if file_size - start_byte >= chunk_size else file_size - start_byte
    end_byte = start_byte + content_length - 1    # 设置结束的字节数为start_byte + content_length 
    
    #设置响应，使用streamingHttpResonse类
    #status必须是206，则响应头显示是partial content。效果是video的进度条能拖动。如果是默认值200，则进度条不能拖动
    response = StreamingHttpResponse(file_iterator(file_path,start_byte,content_length),status=206)
    response["content-type"] = "application/octet-stream"
    response["accept-ranges"] = "bytes"
    response['content-length'] = str(content_length)
    #response的content-range是必须的，否则video组件会一直下载，不会断点播放
    response['content-range'] = 'bytes %s-%s/%s' % (start_byte, end_byte, file_size)
    return response

#streaming时，必须使用yield迭代读取，如果只是使用open读取，则会一直读取全部数据。
def file_iterator(path,start_byte,content_length):
    with open(path, "rb") as f:
        f.seek(start_byte)
        remaining = content_length
        while True:         #使用while循环，一直执行读取，当读取值为空时，跳出break
            bytes_length = min(content_length, 1024 * 8)
            data = f.read(bytes_length)
            if not data:        #如果本次循环读取文件数据为空时，跳出
                break
            if remaining:
                remaining -= len(data)      #每次循环，将remaining减少
            yield data          #迭代器


```

[回到目录](#目录)

***
