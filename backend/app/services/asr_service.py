import base64
from app.core.config import settings


async def transcribe_audio(audio_content: bytes) -> str:
    """Transcribe audio content to text using ASR service"""
    try:
        # 打印调试信息
        print(f"音频文件大小: {len(audio_content)} 字节")
        
        # 使用 OpenAI 兼容模式调用阿里云的语音识别服务
        from openai import OpenAI
        
        client = OpenAI(
            api_key=settings.ASR_API_KEY,
            base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
        )
        
        completion = client.chat.completions.create(
            model=settings.ASR_MODEL,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "input_audio",
                            "input_audio": {
                                "data": f"data:audio/wav;base64,{base64.b64encode(audio_content).decode('utf-8')}"
                            }
                        }
                    ]
                }
            ],
            stream=False,
            extra_body={
                "asr_options": {
                    "enable_itn": False
                }
            }
        )
        
        # 打印响应信息
        print(f"响应内容: {completion}")
        
        # 处理返回结果
        transcription = completion.choices[0].message.content
        return transcription
    except Exception as e:
        # 打印异常信息
        print(f"异常信息: {str(e)}")
        raise Exception(f"服务调用失败: {str(e)}")
