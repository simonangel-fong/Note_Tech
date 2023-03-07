# Javascript - 类FileReader

[回到JavaScript](../js_index.md)

## 目录

- [实例:读取excel文件](#实例读取excel文件)
- [实例:读取本地MP3](#实例读取本地mp3)

## 实例:读取excel文件

- HTML代码

```html

<!-- 
  type: file,则input元素变成文件选取器;
  accept: 指定选取的文件类型
  multiple: 是否可接受多个值的文件
 -->
<input id="file_picker" 
  type="file" 
  value="upload file" 
  class="form-control" 
  accept="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"/>

```

- JavaScript代码

```javascript

// 引用库
<script type="text/javascript" src="https://cdn.staticfile.org/xlsx/0.10.0/xlsx.core.min.js"></script>

  // 当文件选取器改变时, 读取excel文件 
  $("#file_picker").change(function(e){
    var file = e.target.files[0];

    var reader = new FileReader();    //  新建FileReader实例
    reader.addEventListener('loadend',load_excel);      //  定义事件，当加载完毕时，执行指定函数
    
    if(file){     //当选取了文件时
      reader.readAsBinaryString(file);      //以二进制读取字符串的方式读取file, 触发事件.
    }
  });
  
  // 自定义函数，加载excel数据到表格
  function load_excel(event){

    // 以二进制形式读取工作簿
    var workbook = XLSX.read(event.target.result,{type:'binary'});
    var name = workbook.SheetNames[0];    //获取工作表

    if(workbook.Sheets.hasOwnProperty(name)){
        var data = XLSX.utils.sheet_to_json(workbook.Sheets[name]);     //获取工作表中使用过的单元格数据
        $("#table_import").bootstrapTable("load", data);
    }

  }

  // 重置文件选取器，将其value属性设置为""
   $("#file_picker").val("");

```

[回到目录](#目录)

***

### 实例:读取本地MP3

- HTML代码

```html
<!-- 文件选择器 -->
<div class="media col-md-4 p-4">
    <input id="file" type="file" class="form-control" />
</div>

<!-- audio标签，用于控制播放 -->
<div class="media col-md-6 p-4">
    <audio id="audio"  controls>
        <source src="" type="audio/mpeg">
    </audio>
</div>
```

>代码说明：
> - 文件选择组件: `input`便签的`type`属性设置为`file`。
> - 音频播放组件: `audio`标签
>   - `controls`属性: 显示控制组件;
>   - `source`标签: 用于指定数据来源;
>     - `src`属性: 数据来源; 
>     - `type`属性: 设定为`audio/mpeg`,只接受音频格式

- JavaScript代码

```javascript
//  捕获播放组件
var audio = document.getElementById("audio");
  
//  事件: 当文件选择器value改变时
$("#file").change(function (e) {
  //获取选择的文件信息
  var file = e.target.files[0];

  //  新建FileReader实例
  var reader = new FileReader();    

  // 设定事件: 当reader实例加载数据时触发
  reader.addEventListener('load', function () {
    var data = reader.result    //获取reader数据
    audio.setAttribute("src",data)    //设定src属性值为读取的数据

  }, false)

  // 触发事件
  if (file) {     //当选取了文件时
    reader.readAsDataURL(file);      //以二进制读取字符串的方式读取file, 触发事件.
  }
});

```

[回到目录](#目录)

***

[回到JavaScript](../js_index.md)
