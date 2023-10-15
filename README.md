# Startup 🚀
1. Create a virtual environment `python -m venv pdfbotenv`
2. Activate it: 
   - Windows:`.\pdfbotenv\Scripts\activate`
   - Mac: `source pdfbotenv/bin/activate`
3. Install the required dependencies `pip install -r requirements.txt -i <url>`, where the url is one of the following list:

   阿里云 http://mirrors.aliyun.com/pypi/simple/

   中国科技大学 https://pypi.mirrors.ustc.edu.cn/simple/

   豆瓣(douban) http://pypi.douban.com/simple/

   清华大学 https://pypi.tuna.tsinghua.edu.cn/simple/

   中国科学技术大学 http://pypi.mirrors.ustc.edu.cn/simple/
即  pip install --upgrade pip -i https://pypi.tuna.tsinghua.edu.cn/simple/

   pip install 包名 -i http://pypi.douban.com/simple/ --trusted-host pypi.douban.com

4. Add your OpenAI APIKey to a file called "api_key.txt" by pasting it there.
5. Add your PDF to Source_PDF/
6. Start the app `streamlit run app.py` 
