<center>
    <font size=6>RIFF 格式解析</font>
</center>



## 1. RIFF 格式由来

RIFF：(Resource Interchange File Format) 资源互换文件格式，是一种把资料储存在被标记的区块(tagged chunks) 中的档案格式 (meta-format)。RIFF 文件是 windows 环境下大部分多媒体文件遵循的一种文件结构，RIFF 文件所包含的数据类型由该文件的扩展名来标识，能以 RIFF 文件存储的数据包括：音频视频交错格式数据 (.AVI)，波形格式数据 (.WAV)，位图格式数据 (.RDI)， MIDI 格式数据(.RMI)，调色板格式 (.PAL)，多媒体电影 (.RMN)，动画光标 (.ANI) 和其它RIFF文件 (.BND)。



## 2. RIFF 组成结构

RIFF 格式组成类似于树形结构，主要由 FOURCC, CHUNK，LIST 组成。



### 2.1 CHUNK

CHUNK 是组成 RIFF 文件的基本单元，它的基本结构如下:

```c
struct chunk {
	uint32_t id;         // 块标识符
    uint32_t size; 	     // 块大小
    uint8_t  data[size]; // 块内容
};


id 由 4 个 ASCII 字符组成，用于识别块中包含的数据，如："RIFF", "LIST", "fmt", "data", "WAV", "AVI" ......，由于这种文件结构最初是由 Microsoft 和 IBM 为 PC 机所定义, RIFF 文件是按照小端字节顺序写入的。
size 表示 data 域的数据长度。
data 所包含的数据是以 word 为单位排列的，如果长度是奇数，则在最后添加一个空 (NULL) 字符。
    
Note: 如果 id 为 "RIFF" 或 "LIST", 则 data 域则包含 SUB_CHUNK。   
```



### 2.2 LIST

LIST 数据块结构如下：

 ```c
struct list {
	uint32_t list_size;             // List 大小
    uint32_t list_type;             // List 类型
    uint8_t  list_data[list_size];  // List 数据
};

Note: list_data 是该 LIST 的数据内容，由 CHUNK 和 SUB_LIST 组成，它们的个数和组成次序可以是不确定的。
 ```



### 2.3 FOURCC

一个 FOURCC (four character code) 是占用 4 个字节的数据，一般表示 4 个 ASCII 字符。在 "RIFF" 文件格式中，块的起始标识等信息都是使用 FOURCC 表示的，如 "fmt", "data", "wav"......。



## 3. WAV 文件格式解析

一个标准的 WAV 文件组织格式如下所示：

![](E:\learn_pyaudio\Snipaste_2020-12-18_14-12-57.png)



### 3.1 解析示例

![](E:\learn_pyaudio\Snipaste_2020-12-18_15-21-39.png)



上图是一个 WAV 文件：

52494646： ASCII 码对应为 "RIFF"，表示这是符合 RIFF 格式的文件。

24700D00：文件大小，小端方式，大小为 0x000D7024 字节。

57415645：ASCII 码对应为 "WAVE", 表示这是个 WAV 格式的文件， WAV 文件必须包含 "fmt" 和  "data" 两个 SUB_CHUNK。

666D7420：ASCII 码对应为 "fmt", WAV 文件的  SUB_CHUNK。

10000000："fmt" 的大小，小端方式，大小为 0x00000010 字节，若采用 PCM 编码，则该长度为 16 字节。

0100：若文件采用PCM编码，则 AudioFormat=1，AudioFormat 代表不同压缩方式。详见注1。

0200：声道数，Mono (单声道) = 1, Stereo (双声道) = 2。

44AC0000：采样率，小端方式，大小为 0x0000AC44 = 44100 Hz。

10B10200：比特速率，小端方式，大小为 0x0002B110 =  44100 * 16 * 2 = 1411200 bps。

0400：对齐，小端方式，0x0004 表示 4 字节对齐。

1000：采样位深，即每个采样点需要的位数，小端方式，0x0010 = 16 bit。

64617461：ASCII 码对应为 "data", WAV 文件的  SUB_CHUNK。

00700D00：数据大小，小端方式，大小为 0x000D7000 字节。

xx..xx：数据。



注1：

| 值     | 含义                     |
| ------ | ------------------------ |
| 0x0000 | Unknow                   |
| 0x0001 | PCM / Uncompressed       |
| 0x0002 | Microsoft ADPCM          |
| 0x0006 | ITU G.711 a-law          |
| 0x0007 | ITU G.711 Au-law         |
| 0x0011 | IMA ADPCM                |
| 0x0016 | ITU G.723 ADPCM (Yamaha) |
| 0x0031 | GSM 6.10                 |
| 0x0040 | ITU G.721 ADPCM          |
| 0x0050 | MPEG                     |
| 0xFFFF | Experimental             |