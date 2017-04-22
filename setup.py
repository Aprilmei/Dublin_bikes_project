from setuptools import setup

setup(name="DublinBike",
      version="0.2",
      description="Dublin Bike ",
      url="",
      author="Mei Fangxue",
      author_email="sanchiyou@msn.cn",
      licence="GPL3",
      packages=['flaskr'],
      entry_points={
          'console_scripts':['flaskr=flaskr.flaskr:main']
          }
      #Github  https://github.com/Aprilmei/Assignment3.git
      )
