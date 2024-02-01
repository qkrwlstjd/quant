import os
import sys



os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'quantProject.settings')  # 'your_project'는 실제 프로젝트 이름으로 변경해야 합니다.
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
import django
django.setup()
from scripts.script import main_script
if __name__ == "__main__":
    # 이곳에서 Django 앱과 모델을 사용하여 원하는 작업 수행

    main_script()
    pass

